# Systex Mini Hybrid-RAG Demo — 檔案導覽

以下為專案各檔案的用途說明與功能關係圖，方便快速理解整體流程。

## 功能關係圖（端到端資料流）
使用者瀏覽器
  │
  │ `frontend/app/components/Chat.tsx`（Next.js）：取得 `/chat/dev-token`、發送 SSE `/chat/stream?q=...`
  │
  └──SSE→ FastAPI `app/main.py` 路由 `/chat/stream`
          │
          ├─ CORS middleware
          ├─ 依賴：`core/auth.py` 解析 JWT → `core/rbac.py` 驗角色 → `core/tenant.py` 取 tenant
          ├─ 檢查：`core/security.py` 偵測 prompt injection
          ├─ 檢索：`rag/hybrid.py`
          │     ├─ `rag/vector_store.py`（TF-IDF 模擬向量） ← `db/seed.py` 的 `DOCS`
          │     ├─ `rag/sql_retriever.py`（SQL 查詢） ← `db/models.py` + `db/seed.py`
          │     └─ `rag/graph_retriever.py`（圖擴展） ← `db/seed.py` 的 `GRAPH`
          ├─ 組上下文：`rag/context_builder.py`
          ├─ 產答：`rag/llm_gateway.py`（mock 或 OpenAI，依 `core/config.py`）
          ├─ 引用整理：`rag/citations.py`
          └─ 寫入稽核：`db/init_db.py`/`SessionLocal` + `db/models.py` 的 `AuditLog`
          │
          └→ SSE 回傳 meta/chunk/done → `Chat.tsx` 渲染答案與引用

## 檔案用途
- 根目錄
  - `README.md`：本說明文件。
  - `docker-compose.yml`：定義 `backend`（FastAPI）與 `frontend`（Next.js）服務、環境變數與掛載。
- `backend/`
  - `Dockerfile`：建立 FastAPI 映像並啟動 `uvicorn`（對應 docker-compose 覆寫指令）。
  - `requirements.txt`：Python 依賴（FastAPI、SQLAlchemy、OpenAI SDK 等）。
  - `app/main.py`：建立 FastAPI 應用、設定 CORS、啟動時初始化/seed DB、掛載 `/chat` 路由。
  - `app/api/chat.py`：`/chat/dev-token` 與 SSE `/chat/stream` 端點；執行檢索、LLM 回答、稽核寫入並串流回前端。
  - `app/core/auth.py`：JWT 解碼/驗證；`issue_dev_token` 提供本地測試用 token。
  - `app/core/config.py`：讀取環境設定（llm_provider、openai_api_key、DB URL、JWT secret）。
  - `app/core/logging.py`：簡易 trace span 工具（目前僅示範）。
  - `app/core/rbac.py`：角色驗證依賴，限制角色存取。
  - `app/core/security.py`：Prompt injection 偵測與輸出清理。
  - `app/core/tenant.py`：從使用者宣告取得租戶資訊。
  - `app/db/init_db.py`：建立 SQLAlchemy engine/session，初始化資料表。
  - `app/db/models.py`：資料模型 `AuditLog`（稽核）、`Customer`、`Order`。
  - `app/db/seed.py`：啟動時灌入示範資料；同時提供向量檢索 `DOCS` 與圖資料 `GRAPH`。
  - `app/rag/hybrid.py`：協調向量/SQL/圖三種檢索並排序結果。
  - `app/rag/vector_store.py`：以簡化 TF-IDF 進行向量類比檢索。
  - `app/rag/sql_retriever.py`：以條件判斷產生 SQL 查詢（示範 NL→SQL）。
  - `app/rag/graph_retriever.py`：依問題中的實體回傳鄰接關係。
  - `app/rag/context_builder.py`：去重並裁剪檢索結果，生成 LLM 上下文。
  - `app/rag/llm_gateway.py`：根據設定呼叫 mock 回答或 OpenAI Responses API，並估算 token。
  - `app/rag/citations.py`：將檢索結果整理成前端引用格式。
- `frontend/`
  - `Dockerfile`：建立 Next.js 開發映像，預設跑 `npm run dev`。
  - `package.json` / `package-lock.json`：前端依賴與腳本。
  - `tsconfig.json` / `next.config.js` / `next-env.d.ts`：TypeScript 與 Next.js 設定。
  - `app/layout.tsx`：全域 HTML 樣板與 metadata。
  - `app/page.tsx`：首頁，掛載聊天元件。
  - `app/components/Chat.tsx`：聊天 UI；取得測試 token、以 SSE 呼叫 `/chat/stream`，並渲染 meta/答案/引用與示範提問。

## 快速啟動（Docker）
```bash
docker compose up --build
```
如需使用 OpenAI，請在 `docker-compose.yml` 開啟 `LLM_PROVIDER=openai` 並提供 `OPENAI_API_KEY`。
