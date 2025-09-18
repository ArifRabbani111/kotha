🗣️ Kotha – AI-Powered Personal Knowledge Chatbot

Kotha is an AI-powered chatbot that lets you upload your personal documents (TXT, PDF, DOCX) and then chat with them naturally.
It uses Large Language Models (LLMs) with vector search (FAISS) to provide accurate, context-aware answers.

🚀 Features

📂 Document Upload: Upload .txt, .pdf, and .docx files as knowledge sources.

🧠 Memory System: Remembers previous chats for a more human-like conversation.

🔍 Vector Database (FAISS): Stores embeddings for efficient semantic search.

🤖 AI Responses: Uses Google Gemini via LangChain.

🛠️ Extensible: Add more file types (CSV, etc.) in the future.

🏗️ Project Structure
KOTHA/
│── backend/
│   ├── app.py              # FastAPI backend (file upload + chat)
│   ├── chatbot.py          # Chatbot logic (Gemini)
│   ├── knowledge.py        # Ingestion (TXT/PDF/DOCX -> chunks -> FAISS)
│   ├── memory.py           # Chat history (optional)
│   └── requirements.txt    # Backend dependencies
│
└── frontend/
    ├── ui.py               # Streamlit UI
    └── requirements.txt    # Frontend dependencies

⚡ Installation & Setup

1️⃣ Clone Repository

```
git clone https://github.com/your-username/kotha.git
cd kotha
```

2️⃣ Create Virtual Environments

Backend
```
cd backend
python -m venv venv
venv\Scripts\activate    # Windows
# source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

Frontend (optional separate venv)
```
cd ../frontend
python -m venv venv
venv\Scripts\activate    # Windows
# source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

3️⃣ Setup Environment Variables

Create an environment variable (or a .env loaded before run):

```
GOOGLE_API_KEY=your_google_gemini_api_key
```

4️⃣ Run the App

Start backend (port 5000):
```
cd backend
venv\Scripts\activate
python app.py
```

Start frontend (in a separate terminal):
```
cd frontend
venv\Scripts\activate
streamlit run ui.py
```

🧑‍💻 Usage

- Open Streamlit link (usually http://localhost:8501)
- Upload documents (.txt / .pdf / .docx)
- Ask natural language questions about your files
- Chatbot responds using AI + your knowledge base
