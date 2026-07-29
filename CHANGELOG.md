# Changelog

## 2026-07-29

### Breaking

- Changed the Agent Skill frontmatter name from `hermes-agent-docs` to
  `hermes-agent-docs-skill` so it matches the repository and installation
  directory. Existing copied installations should be replaced with a Git
  checkout at a directory named `hermes-agent-docs-skill`.

### Added

- Added `references/SOURCE.md` with the exact Hermes Agent upstream commit and
  sync timestamp.
- Added `references/catalog.md` as a compact LLM task-routing entry point.
- Added repository validation for required files, document count, complete
  `.md`/`.mdx` indexing, source metadata, skill naming, and mirror symlinks.
- Added unit and local Git integration tests for index generation,
  installation/update behavior, safe document synchronization, rollback, and
  repository validation.
- Added installation and maintenance guidance in English and Traditional
  Chinese.

### Changed

- Rebuilt `SKILL.md` around progressive disclosure, platform-aware routing,
  local evidence paths, source freshness, secret redaction, approval boundaries,
  answer verification, rationalizations, and red flags.
- Reworked `install-skill.sh` to clone missing targets, update existing Git
  checkouts with `--ff-only`, validate completed installations, reject detached
  or mismatched checkouts, and refuse to overwrite non-Git directories.
- Reworked `sync-docs.sh` to clone and validate in temporary locations before
  replacing `references/`, reject symlinks and incomplete mirrors, record
  provenance, and restore the previous mirror if final validation fails.
- Updated the daily GitHub Actions workflow with pinned action commits,
  Python 3.12, concurrency control, timeout, maintenance tests, repository
  validation, and an explicit push target.
- Refreshed the documentation mirror from Hermes Agent upstream commit
  `ada389004f73a65250dd27147372c356d09becf7`.

### Fixed

- Fixed the index generator incorrectly excluding every nested file named
  `index.md`.
- Fixed `.mdx` files being absent from the generated documentation index.
- Fixed nondeterministic directory traversal and missing frontmatter titles in
  generated navigation.
- Fixed the installer reporting completion without actually installing or
  successfully updating the skill.
- Removed outdated guidance that treated native Windows as unsupported.
- Removed the incorrect `hermes profile set` example; the mirrored command
  reference uses `hermes profile use`.
- Clarified that the GitHub source mirror updates daily while local installations
  update only when their Git checkout is explicitly refreshed.
