# 🧠 Enterprise AI Assistant (Nexa)

A smart, modular AI assistant built to help employees in an enterprise setting. **Nexa** can answer company-specific questions using internal knowledge, retrieve structured data, and provide intelligent assistance via a modern chat interface.

## 🔍 Features

- 🗂️ **RAG-based Document Search**: Uses embeddings + vector database (Pinecone) to provide precise answers from internal documents.
- 💬 **Chat Interface with Memory**: A WhatsApp-style Streamlit frontend with avatars, chat bubbles, and typing indicators.
- ⚙️ **Groq LLM Integration**: Blazing-fast responses powered by LLaMA 3 via the Groq API.
- 🧩 **Agent-Based Architecture**: Easily extendable to support new tools and workflows (e.g., meeting scheduling, email drafting).
- 📂 **Modular Project Structure**: Clean and scalable architecture, built for growth.

## 📁 Project Structure

enterprise_bot/
├── .venv/ # Virtual environment (excluded from Git)

├── agents/ # Agent definitions and LLM tool setup

│ └── meeting_agent.py

├── utils/ # Utilities like RAG setup and document processing

│ └── rag_search.py

├── vector_store/ # Precomputed vector index for company data

├── streamlit_app.py # Main UI entry point

├── requirements.txt # If using pip

├── pyproject.toml # If using uv or poetry

└── README.md # This file


## 🧪 Example Queries

> **Who is the owner of Chopra Enterprise?**  
✅ *Ansh Chopra*

> **What department does Omar Hishan work in?**  
✅ *Quality Control*

## 🚀 Getting Started

1. **Install dependencies**  
   We recommend using [`uv`](https://github.com/astral-sh/uv) for fast Python package management:
   ```bash
   uv venv
   uv pip install -r requirements.txt

🧠 Future Extensions
📅 Calendar + meeting scheduling with Teams/Google

📧 Email drafting and sending via Outlook/Gmail

🧾 HR, payroll, and document workflows

🕵️ Audit trail and analytics dashboard

🛠️ Tech Stack
Frontend: Streamlit

LLM: Groq API with LLaMA 3 (8B)

Vector DB: Pinecone

LangChain: for RAG + agent orchestration

Python: 3.10+

