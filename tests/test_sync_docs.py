import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def run(command: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        command,
        cwd=cwd,
        check=False,
        text=True,
        capture_output=True,
    )


def create_upstream(repository: Path, complete: bool) -> str:
    docs_dir = repository / "website" / "docs"
    docs_dir.mkdir(parents=True)
    paths = ["getting-started/installation.md"]
    if complete:
        paths.extend(
            [
                "integrations/providers.md",
                "reference/faq.md",
                "user-guide/configuration.md",
                "user-guide/messaging/index.md",
            ]
        )
    for relative_path in paths:
        path = docs_dir / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"# {path.stem}\n", encoding="utf-8")
    (docs_dir / "user-stories.mdx").write_text("# Stories\n", encoding="utf-8")

    run(["git", "init", "-b", "main"], cwd=repository)
    run(["git", "add", "."], cwd=repository)
    result = run(
        [
            "git",
            "-c",
            "user.name=Fixture",
            "-c",
            "user.email=fixture@example.invalid",
            "commit",
            "-m",
            "fixture upstream",
        ],
        cwd=repository,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr)
    return run(["git", "rev-parse", "HEAD"], cwd=repository).stdout.strip()


def create_skill_repository(repository: Path) -> None:
    (repository / "scripts").mkdir(parents=True)
    for script_name in (
        "generate_index.py",
        "sync-docs.sh",
        "validate_repository.py",
    ):
        shutil.copy2(
            REPOSITORY_ROOT / "scripts" / script_name,
            repository / "scripts" / script_name,
        )
    (repository / "SKILL.md").write_text(
        "---\n"
        "name: hermes-agent-docs-skill\n"
        'description: "Guides Hermes support. Use when Hermes needs help."\n'
        "---\n",
        encoding="utf-8",
    )
    references_dir = repository / "references"
    references_dir.mkdir()
    (references_dir / "stale.md").write_text("# Stale\n", encoding="utf-8")


class SyncDocsTests(unittest.TestCase):
    def test_sync_replaces_mirror_only_after_validation_and_records_source(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            upstream = temp_path / "upstream"
            expected_commit = create_upstream(upstream, complete=True)
            skill_root = temp_path / "hermes-agent-docs-skill"
            create_skill_repository(skill_root)

            result = run(
                [
                    "bash",
                    str(skill_root / "scripts" / "sync-docs.sh"),
                    "--repository",
                    str(upstream),
                    "--minimum-documents",
                    "1",
                ],
                cwd=skill_root,
            )

            self.assertEqual(0, result.returncode, result.stderr)
            self.assertFalse((skill_root / "references" / "stale.md").exists())
            self.assertTrue(
                (skill_root / "references" / "user-guide/messaging/index.md").is_file()
            )
            source = (skill_root / "references" / "SOURCE.md").read_text(
                encoding="utf-8"
            )
            self.assertIn(expected_commit, source)
            self.assertIn("Repository validation passed", result.stdout)

    def test_invalid_upstream_does_not_destroy_existing_mirror(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            upstream = temp_path / "upstream"
            create_upstream(upstream, complete=False)
            skill_root = temp_path / "hermes-agent-docs-skill"
            create_skill_repository(skill_root)

            result = run(
                [
                    "bash",
                    str(skill_root / "scripts" / "sync-docs.sh"),
                    "--repository",
                    str(upstream),
                    "--minimum-documents",
                    "1",
                ],
                cwd=skill_root,
            )

            self.assertNotEqual(0, result.returncode)
            self.assertTrue((skill_root / "references" / "stale.md").is_file())

    def test_failed_final_validation_removes_new_mirror_when_no_previous_copy_exists(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            upstream = temp_path / "upstream"
            create_upstream(upstream, complete=True)
            skill_root = temp_path / "hermes-agent-docs-skill"
            create_skill_repository(skill_root)
            shutil.rmtree(skill_root / "references")
            (skill_root / "SKILL.md").write_text(
                "---\n"
                "name: wrong-directory-name\n"
                'description: "Guides Hermes. Use when Hermes needs help."\n'
                "---\n",
                encoding="utf-8",
            )

            result = run(
                [
                    "bash",
                    str(skill_root / "scripts" / "sync-docs.sh"),
                    "--repository",
                    str(upstream),
                    "--minimum-documents",
                    "1",
                ],
                cwd=skill_root,
            )

            self.assertNotEqual(0, result.returncode)
            self.assertFalse((skill_root / "references").exists())


if __name__ == "__main__":
    unittest.main()
