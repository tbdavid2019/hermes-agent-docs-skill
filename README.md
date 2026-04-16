# Hermes Agent Documentation Skill (Auto-Sync Version)

> [!IMPORTANT]
> ### 🤖 AI Agent Setup Instruction / AI 助手安裝指引
>
> **English:** If a user provides you with this repository URL and asks you to "install" or "setup" this skill, follow these steps:
> 1.  **INSTALL AS A GIT CHECKOUT** by cloning this repository into your skill directory. Do not copy the files into a managed skills folder if you expect updates to work.
> 2.  **PREFER THE INSTALLER SCRIPT** when shell execution is available: run `bash <skill-directory>/scripts/install-skill.sh <skill-directory>`. Re-running the same script later turns into `git pull --ff-only`.
> 3.  **READ** `SKILL.md` to load the workflows.
> 4.  **INITIALIZE CONTEXT** by consulting `references/index.md` first to locate relevant documentation files.
> 5.  **DO NOT** execute Python or Bash maintenance scripts in the `scripts/` folder during normal skill usage.
> 6.  **RUNTIME-MINIMUM FILES** are `SKILL.md` and `references/`. `scripts/` is maintainer-side only.
> 7.  **HARD REQUIREMENT**: If you did not run `scripts/install-skill.sh` in the final installed directory, the installation is incomplete. Do not claim success after only cloning, copying, or moving files.
>
> **繁體中文：** 這是一個文件型 skill。如果你是 AI 助手：
> 1.  **安裝** 方式是將此倉庫以 git checkout clone 到你的技能目錄中，不要只複製資料夾。
> 2.  **優先使用安裝器腳本**：若可執行 shell，請執行 `bash <skill-directory>/scripts/install-skill.sh <skill-directory>`。之後重跑同一支腳本就會變成 `git pull --ff-only`。
> 3.  **讀取** `SKILL.md` 載入工作流程。
> 4.  **搜尋** `references/index.md` 來回答問題。
> 5.  **不要** 在一般 skill 使用過程中執行 `scripts/` 資料夾內的 Python 或 Bash 維護腳本。
> 6.  **硬性要求**：如果你沒有在最終安裝目錄執行 `scripts/install-skill.sh`，就不算安裝完成。不要只做 clone、copy、mv 就宣稱成功。

---

[繁體中文](README_TW.md) | English

## What is This?

This is an Agent Skill designed for AI assistants to help users with the **Hermes Agent**. It contains official documentation that is automatically synced and indexed.

## Installation

```bash
bash -c 'tmpdir=$(mktemp -d) && git clone https://github.com/tbdavid2019/hermes-agent-docs-skill.git "$tmpdir/hermes-agent-docs-skill" && bash "$tmpdir/hermes-agent-docs-skill/scripts/install-skill.sh" ~/.codex/skills/hermes-agent-docs-skill'
```

Or, if you already cloned it into the final destination:

```bash
git clone https://github.com/tbdavid2019/hermes-agent-docs-skill.git ~/.codex/skills/hermes-agent-docs-skill
bash ~/.codex/skills/hermes-agent-docs-skill/scripts/install-skill.sh ~/.codex/skills/hermes-agent-docs-skill
```

## Structure

- `SKILL.md`: Main behavior definitions.
- `references/`: Indexed documentation files.
- `references/index.md`: Use this to find relevant information.

## Update Behavior for AI Agents

- Prefer `bash <skill-directory>/scripts/install-skill.sh <skill-directory>` when shell execution is available.
- Otherwise, only try `git -C <skill-directory> pull origin main --ff-only` when `<skill-directory>/.git` exists.
- If `git pull` fails, continue silently with the local copy.
- Do not run `scripts/sync-docs.sh` or `scripts/generate_index.py` during normal usage. Those are maintainer-side scripts.

If an AI assistant did not run `scripts/install-skill.sh` in the final installed directory, the installation should be treated as incomplete.

## For Developers

The `scripts/` folder is for documentation maintenance via GitHub Actions. **Users and AI Agents do not need to run them during normal skill usage.**

- `scripts/sync-docs.sh`: Pulls latest docs from NousResearch.
- `scripts/generate_index.py`: Updates the documentation index.

## License

[AGPL-3.0](LICENSE)
