#!/usr/bin/env python3
"""Generate a deterministic local index for the mirrored Hermes documentation."""

from __future__ import annotations

import argparse
import re
from collections import defaultdict
from pathlib import Path


DOCUMENT_SUFFIXES = {".md", ".mdx"}
FRONTMATTER_TITLE = re.compile(r"^title:\s*[\"']?(.*?)[\"']?\s*$")


def get_title(file_path: Path) -> str:
    """Return frontmatter title, first Markdown heading, or the file name."""
    try:
        lines = file_path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError):
        return file_path.name

    if lines and lines[0].strip() == "---":
        for line in lines[1:]:
            if line.strip() == "---":
                break
            match = FRONTMATTER_TITLE.match(line.strip())
            if match:
                return match.group(1).strip()

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#"):
            title = stripped.lstrip("#").strip()
            if title:
                return title

    return file_path.name


def _section_title(relative_directory: Path) -> str:
    if relative_directory == Path("."):
        return "Root"
    return " / ".join(part.replace("-", " ").title() for part in relative_directory.parts)


def generate_index(docs_dir: str | Path, output_file: str | Path) -> None:
    """Index every Markdown/MDX source except the generated output itself."""
    docs_path = Path(docs_dir).resolve()
    output_path = Path(output_file).resolve()
    grouped_files: dict[Path, list[Path]] = defaultdict(list)

    for file_path in sorted(docs_path.rglob("*")):
        if not file_path.is_file() or file_path.suffix.lower() not in DOCUMENT_SUFFIXES:
            continue
        if file_path.resolve() == output_path:
            continue
        grouped_files[file_path.parent.relative_to(docs_path)].append(file_path)

    content = [
        "# Hermes Agent Documentation Index",
        "",
        "This complete index is generated deterministically from the mirrored official "
        "documentation. Start with `catalog.md` for task routing, then use this file "
        "only when a document is not listed there.",
        "",
    ]

    for relative_directory in sorted(grouped_files, key=lambda path: path.as_posix()):
        content.extend([f"## {_section_title(relative_directory)}", ""])
        for file_path in sorted(grouped_files[relative_directory], key=lambda path: path.name):
            relative_file = file_path.relative_to(docs_path).as_posix()
            content.append(f"*   [{get_title(file_path)}]({relative_file})")
        content.append("")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(content), encoding="utf-8")
    print(f"Index generated: {output_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--docs-dir", default="references")
    parser.add_argument("--output", default="references/index.md")
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    generate_index(arguments.docs_dir, arguments.output)
