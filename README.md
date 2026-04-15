# Hermes Agent Documentation Skill (Auto-Sync Version)

> [!IMPORTANT]
> ### 🤖 Instructions for AI Agent Installation / AI 助手安裝指引
>
> **English:** If a user provides you with this repository URL and asks you to "install" or "setup" this skill, follow these steps:
> 1.  **Clone the Repository**: Run `git clone https://github.com/tbdavid2019/hermes-agent-docs-skill.git` in the user's working directory.
> 2.  **Load Skill Metadata**: Read `SKILL.md` to understand the specialized workflows and knowledge contained here.
> 3.  **Initialize Context**: Acknowledge that you now have access to the comprehensive Hermes Agent documentation. **Always consult `references/index.md` first to locate specific documentation files.**
>
> **繁體中文：** 如果使用者提供此倉庫網址並要求你「安裝」或「設定」此技能服務，請遵循以下步驟：
> 1.  **複製倉庫**：執行 `git clone https://github.com/tbdavid2019/hermes-agent-docs-skill.git` 將代碼庫下載至本地集。
> 2.  **載入技能**：讀取 `SKILL.md` 以了解此技能的專業工作流程與知識範圍。
> 3.  **初始化環境**：確認你已具備存取完整 Hermes Agent 官方文檔的能力。**每當需要查詢特定功能或維護指引時，請優先參考 `references/index.md`。**

---

[繁體中文](README_TW.md) | English

## What is This?

This is an Agent Skill designed for AI coding assistants (like Gemini CLI, Claude, or Codex). Once installed, the AI assistant gains deep knowledge of the **Hermes Agent** and can help you with:

- **Installation & Setup** — Install Hermes Agent on Linux, WSL2, or Termux.
- **Troubleshooting** — Diagnose errors like `hermes: command not found` or model context window rejection.
- **Configuration** — Manage API keys for OpenRouter, Ollama, and other providers.
- **Agent Loop & SOUL.md** — Understand the internal architecture and personality settings.
- **Messaging Gateway** — Configure Telegram, Discord, and other messaging integrations.
- **Developer Guide** — Help with adding providers, tools, or extending the CLI.

## Skill Structure

```
hermes-agent-docs-skill/
├── SKILL.md                     # Main entry (Expert workflows and diagnostic logic)
├── scripts/
│   ├── sync-docs.sh             # Sync Engine — pulls latest docs from upstream
│   └── generate_index.py        # Indexer — generates references/index.md
├── .github/
│   └── workflows/
│       └── auto-sync.yml        # GitHub Action — daily auto-sync at 04:00 UTC
└── references/                  # Latest Markdown files (The Knowledge Base)
    ├── getting-started/         # Installation, Quickstart, Updates
    ├── user-guide/              # Configuration, Profiles, Features, Messaging
    ├── developer-guide/         # Architecture, Agent Loop, Extending CLI
    ├── guides/                  # Use cases: Soul, MCP, Voice Mode, Plugins
    ├── reference/               # CLI Commands, Skills Catalog, FAQ
    └── index.md                 # Automated Document Index
```

## Setup for AI Agents

### For Gemini CLI / Antigravity

Copy the skill folder to your local skills directory:

```bash
# Clone this repo
git clone https://github.com/tbdavid2019/hermes-agent-docs-skill.git

# Install via Gemini CLI (if applicable)
# gemini skills install ./hermes-agent-docs-skill --scope workspace
```

## Usage Examples

Once installed, just ask naturally:

| What You Say | What the AI Does |
|---|---|
| "Help me install Hermes Agent on WSL2" | Reads `getting-started/installation.md` and guides through the process |
| "Why is my model being rejected?" | Explains the 64,000 token context window requirement from `getting-started/quickstart.md` |
| "Configure OpenRouter API key" | Provides the command `hermes config set OPENROUTER_API_KEY ...` |
| "How does SOUL.md work?" | Deep dives into the Agent Loop and Personality docs |
| "Set up Telegram messaging" | Guides through the Messaging Gateway configuration |

## Updating the Documentation

This skill's `references/` folder is synced from the official [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) repository. To get the latest docs:

```bash
sh scripts/sync-docs.sh
python3 scripts/generate_index.py
```

The GitHub Action runs automatically every day at 04:00 UTC.

## Documentation Source

This skill's knowledge base is built from the official Hermes Agent documentation:
- [Hermes Agent Docs](https://github.com/NousResearch/hermes-agent/tree/main/website/docs)

## License

[MIT](LICENSE) — Hermes Agent documentation is sourced from the official NousResearch/hermes-agent repository.
