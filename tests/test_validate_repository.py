import importlib.util
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPOSITORY_ROOT / "scripts" / "validate_repository.py"
MODULE_SPEC = importlib.util.spec_from_file_location("validate_repository", MODULE_PATH)
validate_repository_module = importlib.util.module_from_spec(MODULE_SPEC)
assert MODULE_SPEC.loader is not None
MODULE_SPEC.loader.exec_module(validate_repository_module)


class ValidateRepositoryTests(unittest.TestCase):
    def test_index_validation_reports_unindexed_markdown_and_mdx(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            references_dir = Path(temp_dir) / "references"
            (references_dir / "nested").mkdir(parents=True)
            (references_dir / "nested" / "index.md").write_text(
                "# Nested\n", encoding="utf-8"
            )
            (references_dir / "story.mdx").write_text("# Story\n", encoding="utf-8")
            (references_dir / "index.md").write_text(
                "# Index\n\n* [Nested](nested/index.md)\n",
                encoding="utf-8",
            )

            issues = validate_repository_module.validate_index(references_dir)

            self.assertEqual(["index is missing document: story.mdx"], issues)

    def test_index_validation_accepts_every_document_format(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            references_dir = Path(temp_dir) / "references"
            (references_dir / "nested").mkdir(parents=True)
            (references_dir / "nested" / "index.md").write_text(
                "# Nested\n", encoding="utf-8"
            )
            (references_dir / "story.mdx").write_text("# Story\n", encoding="utf-8")
            (references_dir / "index.md").write_text(
                "# Index\n\n"
                "* [Nested](nested/index.md)\n"
                "* [Story](story.mdx)\n",
                encoding="utf-8",
            )

            issues = validate_repository_module.validate_index(references_dir)

            self.assertEqual([], issues)

    def test_skill_name_must_match_install_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repository_root = Path(temp_dir) / "hermes-agent-docs-skill"
            repository_root.mkdir()
            (repository_root / "SKILL.md").write_text(
                "---\nname: hermes-agent-docs\n"
                'description: "Use when troubleshooting Hermes."\n---\n',
                encoding="utf-8",
            )

            issues = validate_repository_module.validate_skill_metadata(repository_root)

            self.assertEqual(
                [
                    "SKILL.md name 'hermes-agent-docs' does not match directory "
                    "'hermes-agent-docs-skill'"
                ],
                issues,
            )

    def test_source_metadata_requires_commit_and_sync_time(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            references_dir = Path(temp_dir) / "references"
            references_dir.mkdir()
            (references_dir / "SOURCE.md").write_text(
                "# Source Metadata\n\n"
                "- Repository: https://github.com/NousResearch/hermes-agent\n",
                encoding="utf-8",
            )

            issues = validate_repository_module.validate_source_metadata(references_dir)

            self.assertEqual(
                [
                    "SOURCE.md is missing Source commit metadata",
                    "SOURCE.md is missing Synced at metadata",
                ],
                issues,
            )


if __name__ == "__main__":
    unittest.main()
