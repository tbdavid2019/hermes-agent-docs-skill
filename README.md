# Hermes Agent Documentation Skill (Auto-Sync Version)

> [!IMPORTANT]
> ### 🤖 AI Agent Installation Guide / AI 助手安裝指引
>
> This repository is a **Self-Contained Agent Skill**. If you are an AI assistant tasked to "install" or "setup" this skill, follow these exact steps:
> 1.  **Clone**: `git clone https://github.com/tbdavid2019/hermes-agent-docs-skill.git`
> 2.  **Verify**: Ensure the files `SKILL.md` and `references/index.md` are present.
> 3.  **Bootstrap**: Read `SKILL.md` to load the expert workflows.
> 4.  **Sync**: Run `git pull` frequently to stay updated with official docs.
> 5.  **Context**: You now have deep knowledge of Hermes Agent. **Always check `references/index.md` before answering troubleshooting queries.**

---

[繁體中文](README_TW.md) | English

## What is This?

This is an Agent Skill designed for AI coding assistants (Gemini CLI, Claude, Codex, etc.). It provides deep knowledge of **Hermes Agent** through an auto-synced documentation engine.

- **Installation & Setup** — Linux, WSL2, or Termux.
- **Troubleshooting** — `hermes: command not found`, 64k context limits, etc.
- **Configuration** — OpenRouter, Ollama, API keys, and Profiles.
- **Architecture** — Agent Loop, SOUL.md, and Personality settings.
- **Integrations** — Messaging Gateway (Telegram, Discord, etc.).

## Skill Structure

```
hermes-agent-docs-skill/
├── SKILL.md                     # Skill Metadata & Expert Workflows
├── package.json                 # Skill Manifest
├── LICENSE                      # AGPL-3.0 License
├── scripts/
│   ├── sync-docs.sh             # Sync Engine — pulls from upstream
│   └── generate_index.py        # Indexer — generates references/index.md
├── .github/
│   └── workflows/
│       └── auto-sync.yml        # GitHub Action — Daily sync
└── references/                  # Knowledge Base (Indexed Markdown)
    ├── getting-started/
    ├── user-guide/
    ├── developer-guide/
    ├── guides/
    ├── reference/
    └── index.md                 # Documentation Index (Consult This First)
```

## Setup

```bash
# Clone this repo
git clone https://github.com/tbdavid2019/hermes-agent-docs-skill.git

# Load into your agent
# Read SKILL.md for workflow definitions
```

## Usage Examples

| Query | AI Action |
|---|---|
| "Help me install Hermes Agent" | Consults `getting-started/installation.md` |
| "Context window error?" | Explains the 64k token requirement from `quickstart.md` |
| "Configure API key" | Provides `hermes config set ...` command |
| "Messaging setup" | Guides through the Gateway configuration |

## Updating the Documentation

The `references/` folder is synced from [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent).

```bash
sh scripts/sync-docs.sh
python3 scripts/generate_index.py
```

GitHub Action runs daily at 04:00 UTC.

## License

[AGPL-3.0](LICENSE) — Derivative works must be open-sourced under the same license.
