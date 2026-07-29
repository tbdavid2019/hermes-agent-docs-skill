#!/usr/bin/env python3
"""Validate the skill, mirrored documentation, and generated navigation files."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


DOCUMENT_SUFFIXES = {".md", ".mdx"}
GENERATED_INDEX = Path("index.md")
INDEX_LINK = re.compile(r"\]\(([^)#?]+\.(?:md|mdx))\)")
REQUIRED_PATHS = (
    Path("SKILL.md"),
    Path("references/catalog.md"),
    Path("references/index.md"),
    Path("references/SOURCE.md"),
    Path("references/getting-started/installation.md"),
    Path("references/integrations/providers.md"),
    Path("references/reference/faq.md"),
    Path("references/user-guide/configuration.md"),
    Path("references/user-guide/messaging/index.md"),
)


def _frontmatter_value(skill_file: Path, key: str) -> str | None:
    try:
        lines = skill_file.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError):
        return None
    if not lines or lines[0].strip() != "---":
        return None
    prefix = f"{key}:"
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if line.startswith(prefix):
            return line.removeprefix(prefix).strip().strip("\"'")
    return None


def validate_skill_metadata(repository_root: str | Path) -> list[str]:
    root = Path(repository_root)
    skill_file = root / "SKILL.md"
    if not skill_file.is_file():
        return ["SKILL.md is missing"]

    issues: list[str] = []
    name = _frontmatter_value(skill_file, "name")
    description = _frontmatter_value(skill_file, "description")
    if not name:
        issues.append("SKILL.md frontmatter is missing name")
    elif name != root.name:
        issues.append(
            f"SKILL.md name '{name}' does not match directory '{root.name}'"
        )
    if not description:
        issues.append("SKILL.md frontmatter is missing description")
    elif "use when" not in description.lower():
        issues.append("SKILL.md description must include explicit 'Use when' triggers")
    elif len(description) > 1024:
        issues.append("SKILL.md description exceeds 1024 characters")
    return issues


def _document_paths(references_dir: Path) -> set[str]:
    paths: set[str] = set()
    for path in references_dir.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in DOCUMENT_SUFFIXES:
            continue
        relative_path = path.relative_to(references_dir)
        if relative_path == GENERATED_INDEX:
            continue
        paths.add(relative_path.as_posix())
    return paths


def _index_paths(index_file: Path) -> set[str]:
    try:
        content = index_file.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return set()
    return {match.group(1) for match in INDEX_LINK.finditer(content)}


def validate_index(references_dir: str | Path) -> list[str]:
    references_path = Path(references_dir)
    index_file = references_path / GENERATED_INDEX
    if not index_file.is_file():
        return ["references/index.md is missing"]

    expected = _document_paths(references_path)
    indexed = _index_paths(index_file)
    issues = [
        f"index is missing document: {path}"
        for path in sorted(expected - indexed)
    ]
    issues.extend(
        f"index links to missing document: {path}"
        for path in sorted(indexed - expected)
    )
    return issues


def validate_source_metadata(references_dir: str | Path) -> list[str]:
    source_file = Path(references_dir) / "SOURCE.md"
    if not source_file.is_file():
        return ["references/SOURCE.md is missing"]
    content = source_file.read_text(encoding="utf-8")
    issues: list[str] = []
    if not re.search(r"^- Source commit: `[0-9a-f]{40}`$", content, re.MULTILINE):
        issues.append("SOURCE.md is missing Source commit metadata")
    if not re.search(r"^- Synced at: `[^`]+`$", content, re.MULTILINE):
        issues.append("SOURCE.md is missing Synced at metadata")
    return issues


def validate_repository(
    repository_root: str | Path,
    minimum_documents: int = 100,
) -> list[str]:
    root = Path(repository_root).resolve()
    references_dir = root / "references"
    issues = [
        f"required path is missing: {path.as_posix()}"
        for path in REQUIRED_PATHS
        if not (root / path).is_file()
    ]

    if references_dir.is_dir():
        document_count = len(_document_paths(references_dir))
        if document_count < minimum_documents:
            issues.append(
                f"document count {document_count} is below minimum {minimum_documents}"
            )
        symlinks = sorted(
            path.relative_to(root).as_posix()
            for path in references_dir.rglob("*")
            if path.is_symlink()
        )
        issues.extend(f"symlink is not allowed in mirror: {path}" for path in symlinks)
        issues.extend(validate_index(references_dir))
        issues.extend(validate_source_metadata(references_dir))

    issues.extend(validate_skill_metadata(root))
    return issues


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", default=".")
    parser.add_argument("--minimum-documents", type=int, default=100)
    return parser.parse_args()


def main() -> int:
    arguments = parse_args()
    issues = validate_repository(
        arguments.repository_root,
        minimum_documents=arguments.minimum_documents,
    )
    if issues:
        print("Repository validation failed:", file=sys.stderr)
        for issue in issues:
            print(f"- {issue}", file=sys.stderr)
        return 1
    print("Repository validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
