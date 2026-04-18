# Hermes Agent 文件 Skill（自動同步版）

> [!IMPORTANT]
> ### 🤖 AI 助手安裝指引 / Instructions for AI Agent Installation
>
> **繁體中文：** 如果使用者提供此倉庫網址並要求你「安裝」或「設定」此技能服務，請遵循以下步驟：
> 1.  **請用 Git checkout 安裝，不要只複製資料夾**：執行 `git clone https://github.com/tbdavid2019/hermes-agent-docs-skill.git <skill-directory>`。如果只是把檔案複製進某個受管目錄，之後更新通常不會成立。
> 2.  **優先使用安裝器腳本**：如果環境允許執行 shell，接著執行 `bash <skill-directory>/scripts/install-skill.sh <skill-directory>`。這會確保安裝結果維持為 git checkout，之後重跑同一支腳本就會變成 `git pull --ff-only`。
> 3.  **載入技能**：讀取 `SKILL.md` 以了解此技能的專業工作流程與知識範圍。
> 4.  **初始化環境**：確認你已具備存取完整 Hermes Agent 官方文檔的能力。**每當需要查詢特定功能或維護指引時，請優先參考 `references/index.md`。**
> 5.  **一般使用時不要執行維護腳本**：安裝 or 使用此 skill 的意思是 clone 或複製資料夾，並讀取 `SKILL.md`。**除非使用者明確要求你更新這個 repo 本身，否則不要執行 `scripts/sync-docs.sh`、`scripts/generate_index.py` 或其他維護腳本。**
> 6.  **硬性要求**：如果你沒有在最終安裝目錄執行 `scripts/install-skill.sh`，就不算安裝完成。不要只做 clone、copy、mv 就宣稱成功。
>
> **English:** If you are an AI assistant, please follow the steps: Clone the repo, run `scripts/install-skill.sh`, read `SKILL.md`, and use `references/index.md` as your primary entry point. Do not run internal sync scripts unless asked.

---

[English](README.md) | 繁體中文

## 這是什麼？

本 Skill 專為 AI 編碼助手設計（如 Gemini CLI, Claude 或 Codex）。安裝後，AI 助手即可深入了解 **Hermes Agent**，並協助你處理：

- **安裝與設定** — 在 Linux、WSL2 或 Termux 上安裝 Hermes Agent。
- **故障排除** — 診斷 `hermes: command not found` 或模型上下文窗口（64k context）被拒絕等錯誤。
- **配置管理** — 管理 OpenRouter、Ollama 及其他服務商的 API 金鑰。
- **Agent Loop 與 SOUL.md** — 深入理解內部架構與人格（Personality）設定。
- **Messaging Gateway** — 配置 Telegram、Discord 等通訊軟體整合。
- **開發者指南** — 協助新增 Provider、工具或擴充 CLI 功能。

## Skill 結構

```
hermes-agent-docs-skill/
├── SKILL.md                     # 主要入口（專家級工作流程與診斷邏輯）
├── scripts/
│   ├── sync-docs.sh             # 同步引擎 — 從上游拉取最新文件
│   └── generate_index.py        # 索引生成器 — 自動產出 references/index.md
├── .github/
│   └── workflows/
│       └── auto-sync.yml        # GitHub Action — 每日 04:00 UTC 自動同步
└── references/                  # 最新 Markdown 文件（知識庫）
    ├── getting-started/         # 安裝、快速入門、更新
    ├── user-guide/              # 配置、設定檔、功能、通訊
    ├── developer-guide/         # 架構、Agent Loop、擴充 CLI
    ├── guides/                  # 使用案例：Soul, MCP, 語音模式, 外掛
    ├── reference/               # CLI 指令、技能目錄、FAQ
    └── index.md                 # 自動生成的文檔索引
```

## AI Agent 安裝指南

### 適用於 Gemini CLI / Antigravity

將 Skill 資料夾複製到你的本地 Skills 目錄：

```bash
# 複製此倉庫
git clone https://github.com/tbdavid2019/hermes-agent-docs-skill.git

# 使用 Gemini CLI 安裝（如適用）
# gemini skills install ./hermes-agent-docs-skill --scope workspace
```

一般使用這個 skill 時，真正需要的是 `SKILL.md` 與 `references/`。`scripts/` 是維護用，不是回答問題時要執行的步驟。

## 使用範例

安裝後，只需自然地提問：

| 當你說... | AI 會做什麼... |
|---|---|
| 「幫我在 WSL2 上安裝 Hermes Agent」 | 讀取 `getting-started/installation.md` 並引導安裝流程 |
| 「為什麼我的模型會被拒絕？」 | 解釋 `getting-started/quickstart.md` 中提到的 64,000 token 上下文限制 |
| 「設定 OpenRouter API key」 | 提供指令 `hermes config set OPENROUTER_API_KEY ...` |
| 「SOUL.md 是如何運作的？」 | 深入探討 Agent Loop 與 Personality 文件內容 |
| 「設定 Telegram 訊息整合」 | 引導完成 Messaging Gateway 配置 |

## 快速指令參考

```bash
# 狀態與診斷
hermes version                     # 檢查版本
hermes status                      # 檢查當前設定檔與配置
hermes doctor                      # 執行自動診斷套件

# 配置管理
hermes config set <KEY> <VALUE>    # 手動設定配置項
hermes config check                # 驗證當前配置
hermes config migrate              # 將舊版配置遷移至新版

# 模型
hermes model                       # 互動式設定模型提供商
# 註：模型至少需要 64,000 token 的上下文窗口

# 設定檔 (Profiles)
hermes profile list                # 列出所有設定檔
hermes profile set <NAME>          # 切換至指定設定檔
```

## 如何更新文件？

本 Skill 的 `references/` 資料夾從官方 [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) 倉庫同步。以下指令是維護這個 repo 本身時才需要：

```bash
sh scripts/sync-docs.sh
python3 scripts/generate_index.py
```

或在 [GitHub Actions](https://github.com/tbdavid2019/hermes-agent-docs-skill/actions) 頁籤中觸發 **Auto-Sync Documentation** 工作流程。

GitHub Action 每天 UTC 04:00 自動執行，無需手動介入。

## 文件來源

本 Skill 知識庫來自官方 Hermes Agent 文檔：
- [Getting Started](https://github.com/NousResearch/hermes-agent/tree/main/website/docs/getting-started)
- [User Guide](https://github.com/NousResearch/hermes-agent/tree/main/website/docs/user-guide)
- [Developer Guide](https://github.com/NousResearch/hermes-agent/tree/main/website/docs/developer-guide)
- [Reference](https://github.com/NousResearch/hermes-agent/tree/main/website/docs/reference)

## 貢獻

歡迎提交 Issues 和 PR！特別期待以下方面的貢獻：
- `SKILL.md` — Agent 的推理邏輯與診斷流程
- `scripts/sync-docs.sh` — 同步引擎效率優化
- `references/` — 精選文件品質提升

```
┌─────────────────────────────────────────────────┐
│        NousResearch/hermes-agent (官方源頭)      │
│              /website/docs 資料夾每日更新       │
└────────────────────┬────────────────────────────┘
                     │ GitHub Action 每日 04:00 UTC
                     ▼
┌─────────────────────────────────────────────────┐
│    tbdavid2019/hermes-agent-docs-skill          │
│    最新文件永遠保持同步                          │
└────────────────────┬────────────────────────────┘
                     │ 使用者 git clone 一次
                     ▼
┌─────────────────────────────────────────────────┐
│   LLM 本地 Skill (~/.gemini/skills/hermes)     │
│   參考 references/index.md 進行問題修復         │
└─────────────────────────────────────────────────┘
```

## 授權

[AGPL-3.0](LICENSE) — 任何衍生作品均須以相同授權開源。Hermes Agent 文件來源於官方 [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) 倉庫。
