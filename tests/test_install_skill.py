import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
INSTALLER = REPOSITORY_ROOT / "scripts" / "install-skill.sh"
VALIDATOR = REPOSITORY_ROOT / "scripts" / "validate_repository.py"


def run(command: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        command,
        cwd=cwd,
        check=False,
        text=True,
        capture_output=True,
    )


def write_fixture_repository(repository: Path) -> None:
    repository.mkdir()
    (repository / "scripts").mkdir()
    shutil.copy2(VALIDATOR, repository / "scripts" / "validate_repository.py")
    (repository / "SKILL.md").write_text(
        "---\n"
        "name: hermes-agent-docs-skill\n"
        'description: "Guides Hermes Agent support. Use when Hermes needs help."\n'
        "---\n"
        "# Fixture Skill\n",
        encoding="utf-8",
    )

    document_paths = [
        "catalog.md",
        "SOURCE.md",
        "getting-started/installation.md",
        "integrations/providers.md",
        "reference/faq.md",
        "user-guide/configuration.md",
        "user-guide/messaging/index.md",
    ]
    references_dir = repository / "references"
    for relative_path in document_paths:
        path = references_dir / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"# {path.stem}\n", encoding="utf-8")

    (references_dir / "SOURCE.md").write_text(
        "# Source Metadata\n\n"
        "- Source commit: `0123456789abcdef0123456789abcdef01234567`\n"
        "- Synced at: `2026-07-29T04:00:00Z`\n",
        encoding="utf-8",
    )
    index_lines = ["# Index", ""]
    index_lines.extend(f"* [{path}]({path})" for path in document_paths)
    (references_dir / "index.md").write_text(
        "\n".join(index_lines) + "\n",
        encoding="utf-8",
    )

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
            "fixture",
        ],
        cwd=repository,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr)


class InstallSkillTests(unittest.TestCase):
    def test_refuses_to_overwrite_existing_non_git_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "hermes-agent-docs-skill"
            target.mkdir()
            sentinel = target / "keep-me.txt"
            sentinel.write_text("user data", encoding="utf-8")

            result = run(["bash", str(INSTALLER), str(target)])

            self.assertNotEqual(0, result.returncode)
            self.assertEqual("user data", sentinel.read_text(encoding="utf-8"))
            self.assertNotIn("Update complete", result.stdout)

    def test_clones_validates_and_fast_forward_updates_installation(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            fixture_repository = temp_path / "fixture-source"
            write_fixture_repository(fixture_repository)
            target = temp_path / "installed" / "hermes-agent-docs-skill"

            install_result = run(
                [
                    "bash",
                    str(INSTALLER),
                    "--repository",
                    str(fixture_repository),
                    "--minimum-documents",
                    "1",
                    str(target),
                ]
            )

            self.assertEqual(0, install_result.returncode, install_result.stderr)
            self.assertTrue((target / ".git").is_dir())
            self.assertIn("Installation verified", install_result.stdout)

            marker = fixture_repository / "updated.txt"
            marker.write_text("new revision", encoding="utf-8")
            run(["git", "add", "updated.txt"], cwd=fixture_repository)
            commit_result = run(
                [
                    "git",
                    "-c",
                    "user.name=Fixture",
                    "-c",
                    "user.email=fixture@example.invalid",
                    "commit",
                    "-m",
                    "update fixture",
                ],
                cwd=fixture_repository,
            )
            self.assertEqual(0, commit_result.returncode, commit_result.stderr)

            update_result = run(
                [
                    "bash",
                    str(INSTALLER),
                    "--repository",
                    str(fixture_repository),
                    "--minimum-documents",
                    "1",
                    str(target),
                ]
            )

            self.assertEqual(0, update_result.returncode, update_result.stderr)
            self.assertEqual(
                "new revision",
                (target / "updated.txt").read_text(encoding="utf-8"),
            )
            self.assertIn("Update verified", update_result.stdout)


if __name__ == "__main__":
    unittest.main()
