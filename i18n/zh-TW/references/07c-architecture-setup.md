# 開發銜接 — ARCHITECTURE.md + setup.sh

## 📄 ARCHITECTURE.md 模板

```markdown
# [產品名稱] — 技術架構

## 目錄結構

[根據技術棧產出對應的目錄結構]

## 資料庫設計

[從 PRD 的 DB Schema 整合，轉為建表 SQL 或 ORM Model 定義]

### ER 關係圖

[Mermaid erDiagram]

### 關鍵 Table 說明

| Table | 說明 | 關鍵欄位 | 索引建議 |
|-------|------|---------|---------|
| | | | |

## API 設計

[根據 User Story 和功能規格，定義 RESTful API endpoints 或 GraphQL schema]

### Endpoints 清單

| 方法 | 路徑 | 說明 | 對應 Task |
|------|------|------|----------|
| GET | /api/v1/[resource] | [說明] | T1.1 |
| POST | /api/v1/[resource] | [說明] | T1.2 |

### 認證方式

[JWT / Session / OAuth 等]

## 第三方服務

| 服務 | 用途 | 對應功能 |
|------|------|---------|
| | | |

## 安全架構

### CORS 配置

| 設定項 | 值 | 說明 |
|--------|---|------|
| 允許的 Origins | [生產域名, localhost:port] | 不使用 wildcard * |
| 允許的 Methods | GET, POST, PUT, DELETE | 依 API 實際需求 |
| 允許的 Headers | Content-Type, Authorization | |
| Credentials | true/false | 依認證方式決定 |

### 安全性 Headers

[根據產品需求，從 references/08-security-checklist.md §5 選擇適用的 Headers]

### Rate Limiting 策略

| 端點類型 | 限制 | 識別方式 |
|---------|------|---------|
| 一般 API | [X] req/min | IP + User ID |
| 登入/註冊 | [X] req/min | IP |
| 檔案上傳 | [X] req/min | User ID |

### 敏感資料處理

- 密鑰管理：[.env + 平台環境變數 / Secrets Manager]
- 日誌規範：不記錄密碼、Token、個人資料
- 資料加密：[傳輸中 TLS / 儲存時加密需求]

> 完整安全性檢查清單見 `references/08-security-checklist.md`
```

---

## 📄 .gitignore 模板

```gitignore
# 環境變數與密鑰
.env
.env.local
.env.*.local
*.pem
*.key

# 產品規劃進度（可能包含敏感商業資訊）
.product-playbook-progress.md
# Product-playbook 開發交接標記（session-local，請勿 commit）
.product-dev-active

# IDE 與作業系統
.idea/
.vscode/
*.swp
.DS_Store
Thumbs.db

# 依賴
node_modules/
__pycache__/
*.pyc
venv/

# 建置產出
dist/
build/
.next/
```

---

## 📄 setup.sh 模板

```bash
#!/bin/bash
# [產品名稱] — 專案初始化腳本
# 使用方式：chmod +x scripts/setup.sh && ./scripts/setup.sh

set -e

echo "🚀 正在初始化 [產品名稱]..."

# ===== 檢查前置條件 =====
command -v [node/python/etc] >/dev/null 2>&1 || { echo "❌ 需要安裝 [runtime]"; exit 1; }

# ===== 安裝依賴 =====
echo "📦 安裝依賴..."
[npm install / pip install -r requirements.txt / etc]

# ===== 環境設定 =====
if [ ! -f .env ]; then
  echo "📝 建立 .env 檔案..."
  cp .env.example .env
  echo "⚠️  請編輯 .env 填入必要的環境變數"
fi

# ===== 資料庫初始化 =====
echo "🗄️  初始化資料庫..."
[migration commands]

echo ""
echo "✅ 初始化完成！"
echo ""
echo "下一步："
echo "  1. 編輯 .env 填入環境變數"
echo "  2. 啟動開發伺服器：[start command]"
echo "  3. 開始開發：claude \"請讀取 CLAUDE.md 和 TASKS.md，開始執行 Phase 1\""
```

---

## 使用者引導文字

### 在 Claude Chat / Cowork 中

產出開發交接包後，顯示以下引導：

```
📦 開發交接包已準備好！包含以下檔案：

  CLAUDE.md        → Claude Code 的專案記憶（產品上下文 + 技術規範）
  TASKS.md         → 開發任務清單（4 個 Phase，共 [N] 個 Task）
  TICKETS.md       → 開票清單（共 [N] 張票，可直接在 Jira/Asana/Linear 開票）
  docs/PRD.md      → 完整 PRD
  docs/ARCHITECTURE.md → 技術架構（DB schema + API + 目錄結構）
  docs/PRODUCT-SPEC.md → 產品規格摘要
  scripts/setup.sh → 一鍵初始化腳本

🔗 如何開始開發：

  1. 下載並解壓到你的專案資料夾
  2. 開啟終端機，進入專案資料夾
  3. 啟動 Claude Code：
     $ claude
  4. 告訴 Claude Code 開始：
     > 請讀取 CLAUDE.md 和 TASKS.md，開始執行 Phase 0

💡 小提示：
  - Claude Code 會自動讀取 CLAUDE.md，所以它已經知道整個產品上下文
  - 每個 Phase 完成後，它會詢問你是否要進入下一個 Phase
  - 如果要調整功能範圍，直接修改 TASKS.md 即可
  - CLAUDE.md 中的「明確不做」清單會防止 Claude Code 做超出範圍的事
```

### 產出前的最終確認

```
在產出開發交接包前，我需要確認幾件事：

1. 技術棧：[已確認 / 需要確認]
2. 產品名稱（用於專案資料夾名稱）：[已確認 / 需要確認]
3. 是否有其他技術限制或偏好？
   - 例如：必須用某個 ORM、需要支援特定瀏覽器、有既有的 CI/CD 等
```
