# 🚏 ROUTES DESIGN — 路由與頁面設計文件
> **建立日期**：2026-04-16

本文件依據 PRD、ARCHITECTURE 與 DB_DESIGN 的規範，詳細列出所有的 Flask 路由，及其 HTTP 動作、對應的 Jinja2 模板，並提供邏輯與錯誤處理說明。

---

## 1. 路由總覽表格

| 功能區塊 | 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
|----------|------|-----------|----------|----------|------|
| **Public** | 首頁 (Landing) | GET | `/` | `index.html` (或 landing) | 系統介紹頁，未登入者瀏覽 |
| **Auth** | 註冊頁面 | GET | `/auth/register` | `auth/register.html` | 顯示註冊表單 |
| | 執行註冊 | POST | `/auth/register` | — | 接收並建立帳號，重導向至登入 |
| | 登入頁面 | GET | `/auth/login` | `auth/login.html` | 顯示登入表單 |
| | 執行登入 | POST | `/auth/login` | — | 驗證帳號密碼，建立 session |
| | 執行登出 | POST / GET | `/auth/logout` | — | 清除 session，重導向至首頁 |
| **Dashboard** | 學習儀表板 | GET | `/dashboard/` | `dashboard/index.html` | 顯示總覽進度與最近學習狀況 |
| **Subjects** | 科目列表 | GET | `/subjects/` | `subjects/index.html` | 列出目前所有科目 |
| | 建立科目 | POST | `/subjects/` | — | 接收表單並建立科目，成功後重導向 |
| | 科目詳情 | GET | `/subjects/<id>` | `subjects/detail.html` | 顯示科目內的筆記與測驗記錄 |
| **Notes** | 筆記上傳頁面 | GET | `/notes/upload` | `notes/upload.html` | 顯示上傳講義之表單 |
| | 處理上傳 | POST | `/notes/upload` | — | 處理 PDF 解析與請求 AI 摘要，重導向至筆記詳情 |
| | 筆記詳情 | GET | `/notes/<id>` | `notes/detail.html` | 檢視 AI 摘要、重點與原文 |
| | 編輯筆記表單 | GET | `/notes/<id>/edit` | `notes/edit.html` | 顯示編輯摘要內容表單 |
| | 處理編輯 | POST | `/notes/<id>/update` | — | 更新筆記後重導向至詳情頁 |
| | 刪除筆記 | POST | `/notes/<id>/delete`| — | 刪除後重導向至科目詳情 |
| **Quiz** | 出題設定頁面 | GET | `/quiz/generate` | `quiz/generate.html` | 選擇筆記、難易度、題數等 |
| | 處理出題 | POST | `/quiz/generate` | — | 送交 AI 取得題目，存入 DB，重導至測驗頁 |
| | 進行測驗 | GET | `/quiz/<id>` | `quiz/take.html` | 顯示測驗卷內容供使用者作答 |
| | 提交答案 | POST | `/quiz/<id>/submit` | — | 批改作答，存入歷程，重導至測驗結果 |
| | 測驗結果 | GET | `/quiz/<id>/result` | `quiz/result.html` | 顯示測驗分數與各題解析 |
| **Analysis** | 弱點分析 | GET | `/analysis/` | `analysis/index.html` | 顯示知識點掌握程度分析圖與複習推薦 |
| **Chat** | 問答頁面 | GET | `/chat/` | `chat/index.html` | 語音/文字問答之互動介面 |
| | 提問 API (AJAX)| POST | `/chat/ask` | — | 接收 JSON，呼叫 AI，回傳 JSON 解答 |

---

## 2. 每個路由的詳細說明

### Auth 模組 (`app/routes/auth.py`)
- **GET `/auth/register`**:
  - 輸出: 渲染 `auth/register.html`。
- **POST `/auth/register`**:
  - 輸入: `email`, `password`, `confirm_password`。
  - 邏輯: 檢查信箱是否已存在、密碼是否相符，呼叫 `User.create()`。
  - 錯誤處理: 若失敗用 `flash` 錯誤訊息並重新渲染該頁面。
  - 輸出: 成功則重導向至 `/auth/login`。
- **GET `/auth/login`**:
  - 輸出: 渲染 `auth/login.html`。
- **POST `/auth/login`**:
  - 輸入: `email`, `password`。
  - 邏輯: 呼叫 `User.get_by_email()` 並核對 `check_password()`，成功用 `login_user()` 保存狀態。
  - 錯誤處理: 失敗則 `flash` 帳密錯誤並重新渲染。
  - 輸出: 成功重導向至 `/dashboard/`。
- **POST `/auth/logout`** (或 GET 亦可):
  - 邏輯: `logout_user()`。重導向至 `/`。

### Dashboard 模組 (`app/routes/dashboard.py`)
- **GET `/dashboard/`**:
  - 邏輯: 必須 `@login_required`。撈取總測驗次數、總平均分、最新的筆記。
  - 輸出: 渲染 `dashboard/index.html`。

### Subjects 模組 (`app/routes/subjects.py`)
- **GET `/subjects/`**:
  - 邏輯: 撈取使用者的所有科目 `Subject.get_all_by_user()`。
  - 輸出: 渲染 `subjects/index.html`。
- **POST `/subjects/`**:
  - 輸入: `name`, `color`, `icon`。
  - 邏輯: `Subject.create()`。
  - 輸出: 重導向至 `/subjects/`。
- **GET `/subjects/<id>`**:
  - 邏輯: 獲取該科目資訊，並連帶取得 `Note.get_all_by_subject(id)`。
  - 錯誤處理: 若非該使用者建立的科目，回傳 403。若科目不存在，回傳 404。
  - 輸出: 渲染 `subjects/detail.html`。

### Notes 模組 (`app/routes/notes.py`)
- **GET `/notes/upload`**:
  - 邏輯: 撈出使用者科目供選單使用。
  - 輸出: 渲染 `notes/upload.html`。
- **POST `/notes/upload`**:
  - 輸入: 檔案上傳 (`file`), `subject_id`。
  - 邏輯: 使用 `pdf_parser` 解析文字；呼叫 `ai_helper.summarize()` 取得摘要及重點，儲存至 `Note`。
  - 錯誤處理: 檔案格式不符回傳錯誤；AI 逾時回傳錯誤訊息。
  - 輸出: 重導向至 `/notes/<id>`。
- **GET `/notes/<id>`**, **GET `/notes/<id>/edit`**, **POST `/notes/<id>/update`**, **POST `/notes/<id>/delete`**:
  - 提供標準的編輯、檢視與刪除邏輯，操作前必須隨時防禦非本人的存取權限。

### Quiz 模組 (`app/routes/quiz.py`)
- **GET `/quiz/generate`**:
  - 輸入: `note_id` (Query string)。
  - 輸出: 渲染 `quiz/generate.html`。
- **POST `/quiz/generate`**:
  - 輸入: `note_id`, `difficulty`, `total_questions`。
  - 邏輯: 由 `Note.get_by_id()` 取出原文，傳給 `ai_helper.generate_questions()`。並將結果建立為 `Quiz` 與多筆 `Question`。
  - 輸出: 重導向至 `/quiz/<quiz_id>`。
- **GET `/quiz/<id>`**:
  - 邏輯: 取出該測驗的所有題目供作答。渲染 `quiz/take.html`。
- **POST `/quiz/<id>/submit`**:
  - 輸入: 各題答案 `{ "question_12": "A", ... }`。
  - 邏輯: 比對計算分數，為每一題建立 `Answer` 紀錄，統計弱點後存入 DB。
  - 輸出: 重導向至 `/quiz/<id>/result`。
- **GET `/quiz/<id>/result`**:
  - 輸出: 渲染 `quiz/result.html`，顯示正確率與解析。

### Analysis 模組 (`app/routes/analysis.py`)
- **GET `/analysis/`**:
  - 邏輯: `Answer.get_all_by_user()` 交由 `analysis_helper.calculate_weakness()` 計算並整理。
  - 輸出: 渲染 `analysis/index.html`。

### Chat 模組 (`app/routes/chat.py`)
- **GET `/chat/`**:
  - 邏輯: 撈出對話歷史（`ChatLog.get_history_by_user()`）。
  - 輸出: 渲染 `chat/index.html`。
- **POST `/chat/ask`** (REST API):
  - 輸入: JSON `{ "question": "..." }`。
  - 邏輯: 儲存 User 發問，呼叫 `ai_helper.answer_question()`，儲存 AI 回答。
  - 輸出: 回傳 JSON `{ "answer": "...", "status": "success" }`。

---

## 3. Jinja2 模板清單

所有的模板將放置於 `app/templates/` 中。

1. **`base.html`**: 共用母版 (包含 Navbar 控制面板 與 Footer)。
2. **`index.html`**: 系統介紹頁。
3. **`auth/login.html`**, **`auth/register.html`**: 使用者身分認證。
4. **`dashboard/index.html`**: 登入後的數據總覽。
5. **`subjects/index.html`**, **`subjects/detail.html`**: 科目列表與單一科目管理頁。
6. **`notes/upload.html`**, **`notes/detail.html`**, **`notes/edit.html`**: 筆記上傳、閱讀、編輯操作。
7. **`quiz/generate.html`**, **`quiz/take.html`**, **`quiz/result.html`**: AI 測驗流程。
8. **`analysis/index.html`**: 弱點分析及進度圖表。
9. **`chat/index.html`**: 聊天介面。

---

## 4. 路由骨架程式碼建立原則
將依照 ARCHITECTURE.md 配置 `Blueprint`，並在各檔案撰寫對應的函式骨架與 Docstrings。
