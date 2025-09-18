from fastapi import FastAPI, UploadFile, File, Form, Body
from fastapi.middleware.cors import CORSMiddleware
from chatbot import Chatbot
from knowledge import KnowledgeBase
import os
import shutil
import uvicorn
from dotenv import load_dotenv

# Load .env if present
load_dotenv()

# Ensure API key is set
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise RuntimeError("Set your GOOGLE_API_KEY in the environment before running")

# Initialize app
app = FastAPI()

# Allow frontend to call this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize chatbot + knowledge base
knowledge_base = KnowledgeBase(api_key=GOOGLE_API_KEY)
chatbot = Chatbot(api_key=GOOGLE_API_KEY, knowledge_base=knowledge_base)


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_path = f"uploaded_docs/{file.filename}"
        os.makedirs("uploaded_docs", exist_ok=True)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Add the uploaded file (pdf/docx/txt) to knowledge base
        knowledge_base.add_file(file_path)

        return {"status": "success", "message": f"{file.filename} uploaded and processed."}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/generate")
async def generate_answer(payload: dict = Body(...)):
    try:
        question = payload.get("question") or payload.get("query") or ""
        if not question:
            return {"answer": "Error: Missing 'question' in request body."}
        answer = chatbot.ask(question)
        return {"answer": answer}
    except Exception as e:
        return {"answer": f"Error: {e}"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)

