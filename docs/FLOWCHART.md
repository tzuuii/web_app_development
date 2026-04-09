# 📊 FLOWCHART — AI 學習助理系統流程圖
> **文件版本**：v1.0  
> **建立日期**：2026-04-09  
> **對應文件**：docs/PRD.md、docs/ARCHITECTURE.md

---

## 1. 使用者流程圖（User Flow）

描述使用者從進入網站到完成各核心功能的完整操作路徑。

```mermaid
flowchart LR
    Start([🌐 使用者開啟網站]) --> A[首頁 Landing Page]
    A --> Auth{已登入？}

    Auth -->|否| B[登入頁 /login]
    Auth -->|否| C[註冊頁 /register]
    C --> B
    B --> D[學習儀表板 /dashboard]
    Auth -->|是| D

    D --> E{選擇功能}

    %% 科目管理
    E -->|管理科目| F[科目列表 /subjects]
    F --> F1[建立新科目]
    F --> F2[進入科目詳情 /subjects/id]
    F2 --> F3[查看該科目筆記與測驗]

    %% 筆記上傳
    E -->|上傳筆記| G[上傳頁 /notes/upload]
    G --> G1[選擇科目 + 上傳 PDF/圖片]
    G1 --> G2[AI 解析與摘要生成]
    G2 --> G3[筆記詳情 /notes/id]
    G3 --> G4{要做什麼？}
    G4 -->|手動編輯| G5[編輯摘要儲存]
    G4 -->|以此出題| H1

    %% AI 測驗
    E -->|AI 測驗| H[出題設定 /quiz/generate]
    H --> H1[選擇筆記 + 題數 + 難度]
    H1 --> H2[AI 生成題目]
    H2 --> H3[進行測驗 /quiz/id]
    H3 --> H4[提交答案]
    H4 --> H5[測驗結果 /quiz/id/result]
    H5 --> H6[查看解析 + 正確率]
    H6 --> I1

    %% 弱點分析
    E -->|弱點分析| I[弱點分析 /analysis]
    I --> I1[查看各科目掌握程度]
    I1 --> I2[強/中/弱 知識點列表]
    I2 --> I3{選擇行動}
    I3 -->|複習弱點筆記| G3
    I3 -->|針對弱點出題| H

    %% 語音問答
    E -->|問答學習| J[問答頁 /chat]
    J --> J1{輸入方式}
    J1 -->|文字輸入| J2[輸入問題]
    J1 -->|語音輸入| J3[錄音 → STT 轉文字]
    J3 --> J2
    J2 --> J4[AI 回答]
    J4 --> J5[儲存對話紀錄]
    J5 --> J1

    %% 登出
    D --> K[登出 /logout]
    K --> A
```

---

## 2. 系統序列圖（Sequence Diagrams）

### 2.1 使用者登入流程

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route\nauth.py
    participant Model as User Model
    participant DB as SQLite

    User->>Browser: 填寫帳號密碼，點擊登入
    Browser->>Flask: POST /login
    Flask->>Model: 查詢 user by email
    Model->>DB: SELECT * FROM users WHERE email=?
    DB-->>Model: 回傳使用者資料
    Model-->>Flask: User 物件
    Flask->>Flask: bcrypt 驗證密碼
    alt 密碼正確
        Flask->>Flask: Flask-Login 建立 Session
        Flask-->>Browser: 302 重導向 /dashboard
    else 密碼錯誤
        Flask-->>Browser: 重新顯示 /login（含錯誤提示）
    end
```

---

### 2.2 上傳筆記與 AI 摘要流程

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route\nnotes.py
    participant Parser as pdf_parser.py
    participant AI as ai_helper.py
    participant API as OpenAI/Gemini API
    participant Model as Note Model
    participant DB as SQLite

    User->>Browser: 選擇科目、上傳 PDF，點擊確認
    Browser->>Flask: POST /notes/upload (multipart/form-data)
    Flask->>Flask: 驗證檔案類型（白名單）
    Flask->>Parser: 解析 PDF 取得純文字
    Parser-->>Flask: 文字內容字串
    Flask->>AI: summarize(text)
    AI->>API: POST /chat/completions（摘要 Prompt）
    API-->>AI: 結構化摘要 JSON
    AI-->>Flask: {summary, key_points, keywords}
    Flask->>Model: Note.create(user_id, subject_id, content, summary...)
    Model->>DB: INSERT INTO notes
    DB-->>Model: 成功，回傳 note_id
    Flask-->>Browser: 302 重導向 /notes/{note_id}
    Browser->>User: 顯示筆記詳情（AI 摘要）
```

---

### 2.3 AI 出題與測驗批改流程

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route\nquiz.py
    participant AI as ai_helper.py
    participant API as OpenAI/Gemini API
    participant Model as Quiz/Answer Model
    participant DB as SQLite

    User->>Browser: 選擇筆記、題數（10題）、難度（中）
    Browser->>Flask: POST /quiz/generate
    Flask->>DB: SELECT content FROM notes WHERE id=?
    DB-->>Flask: 筆記內容
    Flask->>AI: generate_questions(content, count=10, difficulty="medium")
    AI->>API: POST /chat/completions（出題 Prompt）
    API-->>AI: 題目 JSON Array
    AI-->>Flask: [{question, options, answer, explanation}, ...]
    Flask->>DB: INSERT INTO quizzes + questions
    Flask-->>Browser: 302 重導向 /quiz/{quiz_id}

    User->>Browser: 逐題作答，點擊提交
    Browser->>Flask: POST /quiz/{quiz_id}/submit (answers JSON)
    Flask->>DB: INSERT INTO answers（每題作答記錄）
    Flask->>Flask: 計算正確率，更新弱點統計
    Flask->>DB: UPDATE weakness_stats
    Flask-->>Browser: 302 重導向 /quiz/{quiz_id}/result
    Browser->>User: 顯示結果（正確率、每題解析）
```

---

### 2.4 語音問答學習流程

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器（Web Speech API）
    participant Flask as Flask Route\nchat.py
    participant AI as ai_helper.py
    participant API as OpenAI/Gemini API
    participant DB as SQLite

    alt 語音輸入
        User->>Browser: 點擊麥克風，開始說話
        Browser->>Browser: Web Speech API 轉換語音→文字
        Browser->>User: 顯示轉錄文字（可修正）
    else 文字輸入
        User->>Browser: 直接在輸入框打字
    end

    Browser->>Flask: POST /chat/ask {question: "..."}
    Flask->>AI: answer_question(question, context)
    AI->>API: POST /chat/completions（問答 Prompt）
    API-->>AI: AI 回答文字
    AI-->>Flask: {answer, references}
    Flask->>DB: INSERT INTO chat_logs
    Flask-->>Browser: JSON {answer: "..."}
    Browser->>User: 顯示 AI 回答（含公式/說明）
```

---

### 2.5 弱點分析流程

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route\nanalysis.py
    participant Helper as analysis_helper.py
    participant DB as SQLite

    User->>Browser: 點擊「弱點分析」
    Browser->>Flask: GET /analysis
    Flask->>DB: SELECT * FROM answers WHERE user_id=? ORDER BY created_at DESC
    DB-->>Flask: 歷史答題記錄
    Flask->>Helper: calculate_weakness(answers)
    Helper->>Helper: 依知識點分組計算正確率
    Helper-->>Flask: [{topic, score, level:"弱/中/強"}, ...]
    Flask->>DB: 查詢各弱點對應筆記
    DB-->>Flask: 推薦筆記清單
    Flask-->>Browser: render analysis/index.html
    Browser->>User: 顯示弱點分析（圖表 + 推薦複習）
```

---

## 3. 功能清單對照表

| # | 功能 | URL 路徑 | HTTP 方法 | 說明 |
|---|---|---|---|---|
| 1 | 首頁 | `/` | GET | Landing Page，未登入顯示介紹 |
| 2 | 註冊 | `/register` | GET / POST | 建立新帳號 |
| 3 | 登入 | `/login` | GET / POST | 帳號驗證與 Session 建立 |
| 4 | 登出 | `/logout` | POST | 清除 Session |
| 5 | 儀表板 | `/dashboard` | GET | 學習進度總覽 |
| 6 | 科目列表 | `/subjects` | GET | 顯示所有科目 |
| 7 | 建立科目 | `/subjects` | POST | 新增科目 |
| 8 | 科目詳情 | `/subjects/<id>` | GET | 該科目的筆記與測驗列表 |
| 9 | 上傳筆記 | `/notes/upload` | GET / POST | 上傳 PDF 並觸發 AI 摘要 |
| 10 | 筆記詳情 | `/notes/<id>` | GET | 顯示 AI 摘要與原文 |
| 11 | 編輯筆記 | `/notes/<id>/edit` | GET / POST | 手動編輯摘要 |
| 12 | 刪除筆記 | `/notes/<id>/delete` | POST | 刪除筆記 |
| 13 | 出題設定 | `/quiz/generate` | GET / POST | 設定題數、難度，觸發 AI 出題 |
| 14 | 進行測驗 | `/quiz/<id>` | GET | 顯示題目 |
| 15 | 提交答案 | `/quiz/<id>/submit` | POST | 批改並計算正確率 |
| 16 | 測驗結果 | `/quiz/<id>/result` | GET | 顯示結果與解析 |
| 17 | 弱點分析 | `/analysis` | GET | 顯示弱點圖表與複習建議 |
| 18 | 問答頁面 | `/chat` | GET | 語音/文字問答介面 |
| 19 | 提問 API | `/chat/ask` | POST | 接收問題，回傳 AI 回答（JSON） |

---

*📌 下一步：請繼續使用 **/db-design** skill 設計資料庫 Schema。*
