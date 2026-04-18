# Hermes Agent Documentation Skill (Auto-Sync Version)

> [!IMPORTANT]
> ### 🤖 Instructions for AI Agent Installation / AI 助手安裝指引
>
> **English:** If a user provides you with this repository URL and asks you to "install" or "setup" this skill, follow these steps:
> 1.  **Install as a Git Checkout, Not a Copied Folder**: Run `git clone https://github.com/tbdavid2019/hermes-agent-docs-skill.git <skill-directory>`. Do not copy the files into a managed skills folder if you expect updates to work.
> 2.  **Prefer the Installer Script**: If shell execution is available, run `bash <skill-directory>/scripts/install-skill.sh <skill-directory>`. This keeps the installed skill as a git checkout and turns later re-runs into `git pull --ff-only`.
> 3.  **Load Skill Metadata**: Read `SKILL.md` to understand the specialized workflows and knowledge contained here.
> 4.  **Initialize Context**: Acknowledge that you now have access to the comprehensive Hermes Agent documentation. **Always consult `references/index.md` first to locate specific documentation files.**
> 5.  **Do Not Run Maintenance Scripts During Normal Use**: Installing or using this skill means cloning/copying it and reading `SKILL.md`. **Do not run `scripts/sync-docs.sh`, `scripts/generate_index.py`, or other repo-maintenance scripts unless the user explicitly asks to refresh this repository itself.**
> 6.  **Hard Requirement**: If you did not run `scripts/install-skill.sh` in the final installed directory, the installation is incomplete. Do not claim success after only cloning, copying, or moving files.
>
> **繁體中文：** 如果使用者提供此倉庫網址並要求你「安裝」或「設定」此技能服務，請遵循以下步驟：
> 1.  **請用 Git checkout 安裝，不要只複製資料夾**：執行 `git clone https://github.com/tbdavid2019/hermes-agent-docs-skill.git <skill-directory>`。如果只是把檔案複製進某個受管目錄，之後更新通常不會成立。
> 2.  **優先使用安裝器腳本**：如果環境允許執行 shell，接著執行 `bash <skill-directory>/scripts/install-skill.sh <skill-directory>`。這會確保安裝結果維持為 git checkout，之後重跑同一支腳本就會變成 `git pull --ff-only`。
> 3.  **載入技能**：讀取 `SKILL.md` 以了解此技能的專業工作流程與知識範圍。
> 4.  **初始化環境**：確認你已具備存取完整 Hermes Agent 官方文檔的能力。**每當需要查詢特定功能或維護指引時，請優先參考 `references/index.md`。**
> 5.  **一般使用時不要執行維護腳本**：安裝 or 使用此 skill 的意思是 clone 或複製資料夾，並讀取 `SKILL.md`。**除非使用者明確要求你更新這個 repo 本身，否則不要執行 `scripts/sync-docs.sh`、`scripts/generate_index.py` 或其他維護腳本。**
> 6.  **硬性要求**：如果你沒有在最終安裝目錄執行 `scripts/install-skill.sh`，就不算安裝完成。不要只做 clone、copy、mv 就宣稱成功。

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
