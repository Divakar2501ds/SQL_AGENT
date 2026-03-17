# 🤖 SQLAGENT — AI-Powered Document & Database Chatbot

A FastAPI-based intelligent chatbot that uses **LangGraph** to route user queries between a SQL agent (for database questions) and a general-purpose agent. It maintains conversation history and can answer questions about templates, documents, users, and sessions stored in a PostgreSQL database.

---

## 🧠 How It Works

```
User Question
     │
     ▼
 [Decider Node]  ──── routes to ────►  [SQL Agent] → [Execute SQL] → [Summarise]
     │
     └──────────────────────────────►  [General Agent]
```

1. **Decider Node** — classifies the question as `sql` or `general` using an LLM.
2. **SQL Agent** — generates a PostgreSQL query from natural language using a detailed schema prompt.
3. **Execute SQL** — runs the generated query against the database.
4. **Summarise Node** — converts raw SQL results into a human-readable answer.
5. **General Agent** — handles non-database questions using conversation history.

---

## 📁 Project Structure

```
├── router/
│   └── chatbot.py          # FastAPI route (/chat)
├── utilities/
│   ├── agent_nodes.py      # LangGraph node definitions
│   ├── graph.py            # LangGraph graph builder
│   ├── prompting.py        # System prompts & SQL queries
│   ├── chat_history.py     # DB upload/retrieve for history
│   └── llm_setup.py        # LLM client setup (Novita AI)
├── schemas/
│   └── chat_schema.py      # Pydantic models (GraphState, Chatting)
├── database/
│   └── database.py         # DB connection & SQL runner
└── main.py                 # FastAPI app entry point
```

---

## 🗄️ Database Schema (Overview)

| Table | Description |
|---|---|
| `users` | User accounts |
| `templates` | Document templates |
| `template_versions` | Versioned template records |
| `template_sections` | Sections within a template version |
| `sections` | Base section definitions |
| `documents` | Uploaded documents |
| `document_validation` | Validation results per document |
| `sessions` | User login sessions |
| `templates_history` | Audit history for templates |
| `history` | Chat message history |

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/your-username/docuquery-chatbot.git
cd docuquery-chatbot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

Create a `.env` file:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/your_db
NOVITA_API_KEY=your_novita_api_key
```

### 4. Run the server

```bash
uvicorn main:app --reload
```

---

## 📡 API Endpoint

### `POST /chat`

**Request body:**
```json
{
  "question": "How many active users are there?"
}
```

**Response:**
```json
{
  "message": "Data fetched successfully",
  "llm_response": "There are 42 active users in the system."
}
```

---

## 🔧 Tech Stack

| Layer | Technology |
|---|---|
| API Framework | FastAPI |
| Agent Orchestration | LangGraph |
| LLM Provider | Novita AI (`openai/gpt-oss-120b`) |
| Database | PostgreSQL |
| Language | Python 3.10+ |

---

## 📝 Example Questions

**Database queries:**
- *"How many documents have been uploaded this month?"*
- *"List all sections in the latest SOP template."*
- *"Show me all users with admin roles."*

**General questions:**
- *"What is a document validation compliance score?"*
- *"Explain what template versioning means."*

---

## 📄 License

MIT License — feel free to use and modify.
