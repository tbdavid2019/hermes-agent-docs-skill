import importlib.util
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPOSITORY_ROOT / "scripts" / "generate_index.py"
MODULE_SPEC = importlib.util.spec_from_file_location("generate_index", MODULE_PATH)
generate_index_module = importlib.util.module_from_spec(MODULE_SPEC)
assert MODULE_SPEC.loader is not None
MODULE_SPEC.loader.exec_module(generate_index_module)


class GenerateIndexTests(unittest.TestCase):
    def test_indexes_nested_index_files_and_mdx_but_not_generated_output(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            docs_dir = Path(temp_dir) / "references"
            nested_dir = docs_dir / "user-guide" / "messaging"
            nested_dir.mkdir(parents=True)
            (nested_dir / "index.md").write_text(
                "# Messaging Overview\n", encoding="utf-8"
            )
            (docs_dir / "user-stories.mdx").write_text(
                "# User Stories\n", encoding="utf-8"
            )
            output_file = docs_dir / "index.md"

            generate_index_module.generate_index(docs_dir, output_file)

            generated = output_file.read_text(encoding="utf-8")
            self.assertIn(
                "(user-guide/messaging/index.md)",
                generated,
            )
            self.assertIn("(user-stories.mdx)", generated)
            self.assertNotIn("(index.md)", generated)

    def test_uses_frontmatter_title_when_no_markdown_heading_exists(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            docs_dir = Path(temp_dir) / "references"
            docs_dir.mkdir()
            (docs_dir / "frontmatter-only.mdx").write_text(
                "---\ntitle: Frontmatter Title\n---\nBody\n",
                encoding="utf-8",
            )
            output_file = docs_dir / "index.md"

            generate_index_module.generate_index(docs_dir, output_file)

            generated = output_file.read_text(encoding="utf-8")
            self.assertIn("[Frontmatter Title](frontmatter-only.mdx)", generated)

    def test_output_is_deterministically_sorted_by_path(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            docs_dir = Path(temp_dir) / "references"
            (docs_dir / "z-section").mkdir(parents=True)
            (docs_dir / "a-section").mkdir(parents=True)
            (docs_dir / "z-section" / "z.md").write_text("# Z\n", encoding="utf-8")
            (docs_dir / "a-section" / "a.md").write_text("# A\n", encoding="utf-8")
            output_file = docs_dir / "index.md"

            generate_index_module.generate_index(docs_dir, output_file)

            generated = output_file.read_text(encoding="utf-8")
            self.assertLess(
                generated.index("## A Section"),
                generated.index("## Z Section"),
            )


if __name__ == "__main__":
    unittest.main()
