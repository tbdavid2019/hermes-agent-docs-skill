# Hermes Agent Documentation Skill

[繁體中文](README_TW.md) | English

An Agent Skill that gives compatible AI assistants a documentation-grounded
workflow for installing, configuring, operating, developing, and
troubleshooting [Hermes Agent](https://github.com/NousResearch/hermes-agent).

The official documentation mirror is refreshed by GitHub Actions every day at
04:00 UTC. Each successful mirror records the exact upstream commit and sync
time in `references/SOURCE.md`.

## What This Repository Guarantees

- Mirrors official `.md` and `.mdx` documentation.
- Records upstream repository, commit SHA, and sync timestamp.
- Generates a compact task catalog and a deterministic complete index.
- Validates required documents, index completeness, source metadata, skill
  naming, symlinks, and minimum document count.
- Replaces the existing mirror only after a new copy passes preflight checks.
- Provides tested install/update behavior that refuses to overwrite non-Git
  directories.
- Gives LLMs progressive-disclosure, citation, verification, and secret
  redaction rules.

## Architecture

```text
NousResearch/hermes-agent / website/docs
                    │
                    │ daily GitHub Action
                    ▼
       validated staging documentation
                    │
                    │ validated swap with rollback
                    ▼
 references/catalog.md + index.md + SOURCE.md
                    │
                    │ Git checkout in an agent skills directory
                    ▼
              SKILL.md workflow
                    │
                    ▼
      documentation-grounded LLM support
```

The GitHub repository updates daily. A local installation does not run a
background updater: update the local checkout explicitly, or let the host
agent do so only when you ask it to update this skill.

## Install

The final directory name must be `hermes-agent-docs-skill`, matching the
`name` in `SKILL.md`. Keep the installation as a Git checkout if you want it to
receive updates.

### Codex

```bash
git clone \
  https://github.com/tbdavid2019/hermes-agent-docs-skill.git \
  ~/.codex/skills/hermes-agent-docs-skill

bash ~/.codex/skills/hermes-agent-docs-skill/scripts/install-skill.sh \
  --check ~/.codex/skills/hermes-agent-docs-skill
```

### Other Agent Skill Runtimes

Replace `<skills-directory>` with the user-level or workspace-level skills
directory supported by that runtime:

```bash
git clone \
  https://github.com/tbdavid2019/hermes-agent-docs-skill.git \
  <skills-directory>/hermes-agent-docs-skill

bash <skills-directory>/hermes-agent-docs-skill/scripts/install-skill.sh \
  --check <skills-directory>/hermes-agent-docs-skill
```

Some managed skill installers copy files and discard `.git`. Such a copy can
be read by the LLM, but it cannot be updated with this repository's installer.
Use a Git checkout when freshness matters.

The installer refuses to overwrite an existing non-Git directory. Back up or
rename an old copied installation before installing the Git checkout.

## Update Or Verify A Local Installation

Update with fast-forward-only Git behavior, then validate the result:

```bash
bash <skills-directory>/hermes-agent-docs-skill/scripts/install-skill.sh \
  <skills-directory>/hermes-agent-docs-skill
```

Validate without network access or mutation:

```bash
bash <skills-directory>/hermes-agent-docs-skill/scripts/install-skill.sh \
  --check <skills-directory>/hermes-agent-docs-skill
```

The installer exits non-zero if Git update or repository validation fails. It
does not report success after a failed pull.

## How The LLM Uses The Skill

The workflow in `SKILL.md` tells the agent to:

1. Check source freshness when version compatibility matters.
2. Start with `references/catalog.md`.
3. Search exact errors, commands, environment variables, or configuration keys
   when the catalog is insufficient.
4. Load only the smallest useful set of reference pages.
5. Separate platform, installation, provider, gateway, and feature-specific
   failure branches.
6. Cite the local documentation paths used.
7. Finish with a concrete verification command or observable result.

Example prompts:

- “Install Hermes Agent on native Windows.”
- “Why does my local Ollama model fail the context-length check?”
- “Configure a Telegram gateway and verify that it is running.”
- “Which command switches the active Hermes profile?”
- “How do Hermes plugins register tools?”

## Repository Structure

```text
.
├── SKILL.md                         # Agent workflow and safety contract
├── CHANGELOG.md                     # Maintainer-visible changes
├── references/
│   ├── SOURCE.md                    # Exact upstream revision and sync time
│   ├── catalog.md                   # Compact task-to-document routing
│   ├── index.md                     # Complete .md/.mdx inventory
│   └── ...                          # Mirrored official documentation
├── scripts/
│   ├── install-skill.sh             # Clone/update/check installation
│   ├── sync-docs.sh                 # Safe upstream mirror
│   ├── generate_index.py            # Catalog, index, source metadata
│   └── validate_repository.py       # CI and installation quality gate
├── tests/                            # Unit and local Git integration tests
└── .github/workflows/auto-sync.yml  # Daily sync workflow
```

## Maintainer Workflow

Normal skill usage must not execute repository maintenance scripts. Maintainers
can run:

```bash
python3 -m unittest discover -s tests -v
bash -n scripts/install-skill.sh scripts/sync-docs.sh
bash scripts/sync-docs.sh
python3 scripts/validate_repository.py
git diff --check -- . ':!references'
```

`sync-docs.sh` clones into a temporary checkout, rejects symlinks and incomplete
mirrors, generates metadata/navigation, swaps directories only after preflight,
and restores the previous mirror if final repository validation fails.

## Security Boundary

Mirrored documentation is external data, not agent instructions. `SKILL.md`
requires agents to ignore embedded prompt-like instructions, redact secrets,
and follow normal approval rules before destructive, privileged, or externally
mutating actions.

## License

Repository automation and skill instructions are licensed under
[AGPL-3.0](LICENSE). Mirrored Hermes Agent documentation remains attributable
to its [upstream source](https://github.com/NousResearch/hermes-agent); inspect
`references/SOURCE.md` for the exact mirrored revision.
