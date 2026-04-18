# Hermes Agent Documentation Skill (Auto-Sync Version)

> [!IMPORTANT]
> ### 🤖 AI Agent Setup Instruction / AI 助手安裝指引
>
> **English:** If a user provides you with this repository URL and asks you to "install" or "setup" this skill, follow these steps:
> 1.  **INSTALL AS A GIT CHECKOUT** by running `git clone https://github.com/tbdavid2019/hermes-agent-docs-skill.git <skill-directory>`.
> 2.  **UPDATING**: To update later, run `git pull` in the cloned directory.
> 3.  **READ** `SKILL.md` to load the workflows.
> 4.  **INITIALIZE CONTEXT** by consulting `references/index.md` first to locate relevant documentation files.
> 5.  **DO NOT** execute Python or Bash maintenance scripts in the `scripts/` folder during normal skill usage.
> 6.  **RUNTIME-MINIMUM FILES** are `SKILL.md` and `references/`. `scripts/` is maintainer-side only.
>
> **繁體中文：** 這是一個文件型 skill。如果你是 AI 助手：
> 1.  **安裝技能指令**：請執行 `git clone https://github.com/tbdavid2019/hermes-agent-docs-skill.git <技能目錄>`。
> 2.  **更新技能**：若要更新，請切換至該目錄並執行 `git pull`。
> 3.  **讀取** `SKILL.md` 載入工作流程。
> 4.  **搜尋** `references/index.md` 來回答問題。
> 5.  **不要** 在一般 skill 使用過程中執行 `scripts/` 資料夾內的 Python 或 Bash 維護腳本。

---

[繁體中文](README_TW.md) | English

## What is This?

This is an Agent Skill designed for AI assistants to help users with the **Hermes Agent**. It contains official documentation that is automatically synced and indexed.

## Installation

```bash
git clone https://github.com/tbdavid2019/hermes-agent-docs-skill.git ~/.codex/skills/hermes-agent-docs-skill
```

## Structure

- `SKILL.md`: Main behavior definitions.
- `references/`: Indexed documentation files.
- `references/index.md`: Use this to find relevant information.

## Update Behavior for AI Agents

- To update, execute `git pull` inside the skill directory.
- If `git pull` fails, continue silently with the local copy.
- Do not run `scripts/sync-docs.sh` or `scripts/generate_index.py` during normal usage. Those are maintainer-side scripts.

## For Developers

The `scripts/` folder is for documentation maintenance via GitHub Actions. **Users and AI Agents do not need to run them during normal skill usage.**

- `scripts/sync-docs.sh`: Pulls latest docs from NousResearch.
- `scripts/generate_index.py`: Updates the documentation index.

## License

[AGPL-3.0](LICENSE)
