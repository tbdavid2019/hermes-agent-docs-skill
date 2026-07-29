# Hermes Agent 文件 Skill

繁體中文 | [English](README.md)

這是一個 Agent Skill，讓相容的 AI 助手依據官方文件協助安裝、設定、操作、
開發及排除 [Hermes Agent](https://github.com/NousResearch/hermes-agent) 問題。

GitHub Actions 每天 UTC 04:00 更新官方文件鏡像。每次成功同步都會在
`references/SOURCE.md` 記錄上游 commit SHA 與同步時間。

## 這個 Repository 提供的保證

- 同步官方 `.md` 與 `.mdx` 文件。
- 記錄上游 repository、commit SHA 與同步時間。
- 產生精簡任務目錄及固定排序的完整索引。
- 驗證必要文件、索引完整性、來源 metadata、skill 名稱、symlink 與文件數量。
- 新文件通過預檢後才替換原本的 `references/`。
- 安裝器經過 clone/update 整合測試，且不會覆寫既有非 Git 目錄。
- 提供 LLM 漸進式載入、引用、驗證與敏感資料遮蔽規則。

## 架構

```text
NousResearch/hermes-agent / website/docs
                    │
                    │ 每日 GitHub Action
                    ▼
              暫存區驗證文件
                    │
                    │ 驗證式切換並支援失敗還原
                    ▼
 references/catalog.md + index.md + SOURCE.md
                    │
                    │ 安裝為 Agent Skill Git checkout
                    ▼
              SKILL.md 工作流程
                    │
                    ▼
          LLM 依據官方文件回答與診斷
```

GitHub 上的來源 repository 會每日更新；本機安裝不會自行啟動背景排程。
需要更新本機副本時，請明確執行更新，或明確要求 host agent 更新此 skill。

## 安裝

最終資料夾名稱必須是 `hermes-agent-docs-skill`，以符合 `SKILL.md` 的
`name`。如果需要後續更新，必須保留為 Git checkout。

### Codex

```bash
git clone \
  https://github.com/tbdavid2019/hermes-agent-docs-skill.git \
  ~/.codex/skills/hermes-agent-docs-skill

bash ~/.codex/skills/hermes-agent-docs-skill/scripts/install-skill.sh \
  --check ~/.codex/skills/hermes-agent-docs-skill
```

### 其他支援 Agent Skill 的工具

請將 `<skills-directory>` 換成該工具支援的使用者或 workspace skill 目錄：

```bash
git clone \
  https://github.com/tbdavid2019/hermes-agent-docs-skill.git \
  <skills-directory>/hermes-agent-docs-skill

bash <skills-directory>/hermes-agent-docs-skill/scripts/install-skill.sh \
  --check <skills-directory>/hermes-agent-docs-skill
```

部分受管 skill 安裝器會複製檔案並移除 `.git`。這種副本仍可供 LLM
讀取，但無法用本 repository 的安裝器更新。需要文件新鮮度時，請使用
Git checkout。

安裝器不會覆寫既有的非 Git 目錄。若已有舊的複製版，請先備份或改名，
再安裝 Git checkout。

## 更新或驗證本機安裝

使用 fast-forward-only 更新，並在更新後驗證：

```bash
bash <skills-directory>/hermes-agent-docs-skill/scripts/install-skill.sh \
  <skills-directory>/hermes-agent-docs-skill
```

只驗證、不連網、不修改：

```bash
bash <skills-directory>/hermes-agent-docs-skill/scripts/install-skill.sh \
  --check <skills-directory>/hermes-agent-docs-skill
```

如果 Git pull 或 repository validation 失敗，安裝器會以非零狀態結束，
不會在失敗後仍回報完成。

## LLM 如何使用此 Skill

`SKILL.md` 會要求 agent：

1. 版本相容性重要時先確認來源新鮮度。
2. 先讀取 `references/catalog.md`。
3. 目錄不足時，搜尋完整錯誤、命令、環境變數或設定鍵。
4. 只載入能完成任務的最少文件。
5. 分開處理平台、安裝、Provider、Gateway 與功能專屬問題。
6. 列出回答所依據的本機文件路徑。
7. 最後提供具體驗證命令或可觀察結果。

提問範例：

- 「在原生 Windows 安裝 Hermes Agent。」
- 「本機 Ollama 模型為何無法通過 context length 檢查？」
- 「設定 Telegram gateway 並驗證服務已啟動。」
- 「切換 Hermes active profile 的正確命令是什麼？」
- 「Hermes plugin 如何註冊工具？」

## Repository 結構

```text
.
├── SKILL.md                         # Agent 工作流程與安全契約
├── CHANGELOG.md                     # 版本變更紀錄
├── references/
│   ├── SOURCE.md                    # 上游版本與同步時間
│   ├── catalog.md                   # 精簡任務路由
│   ├── index.md                     # 完整 .md/.mdx 索引
│   └── ...                          # 官方文件鏡像
├── scripts/
│   ├── install-skill.sh             # Clone、更新、安裝驗證
│   ├── sync-docs.sh                 # 安全同步上游文件
│   ├── generate_index.py            # 目錄、索引、來源 metadata
│   └── validate_repository.py       # CI 與安裝品質門檻
├── tests/                            # 單元及本機 Git 整合測試
└── .github/workflows/auto-sync.yml  # 每日同步 workflow
```

## 維護流程

一般使用 skill 回答 Hermes 問題時，不可執行 repository 維護腳本。
維護者可以執行：

```bash
python3 -m unittest discover -s tests -v
bash -n scripts/install-skill.sh scripts/sync-docs.sh
bash scripts/sync-docs.sh
python3 scripts/validate_repository.py
git diff --check -- . ':!references'
```

`sync-docs.sh` 會先 clone 至暫存 checkout，拒絕 symlink 與不完整文件，
產生來源 metadata 及索引，通過預檢後才替換目錄；如果最後 repository
validation 失敗，會恢復原本的文件。

## 安全邊界

同步進來的文件是外部資料，不是 agent 指令。`SKILL.md` 要求 agent
忽略文件內類似 prompt 的指令、遮蔽密碼與 token，並在執行破壞性、
需權限或會修改外部狀態的操作前，遵守 host agent 原有的核准規則。

## 授權

Repository automation 與 skill 指令使用 [AGPL-3.0](LICENSE)。
Hermes Agent 文件仍歸屬其
[上游來源](https://github.com/NousResearch/hermes-agent)；實際同步版本請見
`references/SOURCE.md`。
