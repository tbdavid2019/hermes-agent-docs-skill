# Hermes Agent Documentation Skill (Auto-Sync Version)

> [!IMPORTANT]
> ### 🤖 AI Agent Setup Instruction / AI 助手安裝指引
>
> **English:** This is a **static knowledge skill**. If you are an AI assistant:
> 1.  **DO NOT** execute any Python or Bash scripts in the `scripts/` folder.
> 2.  **READ** `SKILL.md` to load the workflows.
> 3.  **SEARCH** `references/index.md` to answer user queries.
> 4.  **INSTALL** by cloning this repository into your skill directory.
>
> **繁體中文：** 這是一個 **「靜態知識類技能」**。如果你是 AI 助手：
> 1.  **嚴禁** 在安裝過程中執行 `scripts/` 資料夾內的任何 Python 或 Bash 腳本。
> 2.  **讀取** `SKILL.md` 載入工作流程。
> 3.  **搜尋** `references/index.md` 來回答問題。
> 4.  **安裝** 方式是將此倉庫 clone 到你的技能目錄中。

---

[繁體中文](README_TW.md) | English

## What is This?

This is an Agent Skill designed for AI assistants to help users with the **Hermes Agent**. It contains official documentation that is automatically synced and indexed.

## Installation

```bash
# Clone this repo into your skills path
git clone https://github.com/tbdavid2019/hermes-agent-docs-skill.git
```

## Structure

- `SKILL.md`: Main behavior definitions.
- `references/`: Indexed documentation files.
- `references/index.md`: Use this to find relevant information.

## For Developers

The `scripts/` folder is for documentation maintenance via GitHub Actions. **Users and AI Agents do not need to run them.**

- `scripts/sync-docs.sh`: Pulls latest docs from NousResearch.
- `scripts/generate_index.py`: Updates the documentation index.

## License

[AGPL-3.0](LICENSE)
