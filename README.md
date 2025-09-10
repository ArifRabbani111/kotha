🗣️ Kotha – AI-Powered Personal Knowledge Chatbot

Kotha is an AI-powered chatbot that lets you upload your personal documents (TXT, PDF) and then chat with them naturally.
It uses Large Language Models (LLMs) with vector search (ChromaDB) to provide accurate, context-aware answers.

🚀 Features

📂 Document Upload: Upload .txt and .pdf files as knowledge sources.

🧠 Memory System: Remembers previous chats for a more human-like conversation.

🔍 Vector Database (ChromaDB): Stores embeddings for efficient semantic search.

🤖 AI Responses: Uses OpenAI (or Hugging Face) LLMs for intelligent answers.

🛠️ Extensible: Add more file types (CSV, DOCX, etc.) in the future.

🏗️ Project Structure
KOTHA/
│── app.py              # Main Flask/FastAPI app
│── chatbot.py          # Chatbot logic
│── knowledge.py        # Handles knowledge ingestion (TXT/PDF -> vectors)
│── memory.py           # Manages chat history
│── requirements.txt    # Python dependencies
│── .gitignore          # Ignore sensitive/unnecessary files
│── data/               # Uploaded documents (ignored in Git)
│── chroma_db/          # Vector database (ignored in Git)

⚡ Installation & Setup
1️⃣ Clone Repository
git clone https://github.com/your-username/kotha.git
cd kotha

2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Setup Environment Variables

Create a .env file in the root folder:

OPENAI_API_KEY=your_openai_api_key

5️⃣ Run the App
python app.py

🧑‍💻 Usage

Start the server with python app.py.

Upload documents (.txt / .pdf).

Ask natural language questions about your files.

Chatbot will respond using AI + your knowledge base.
