import os
import asyncio
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from PyPDF2 import PdfReader
import docx

# Ensure event loop exists (needed for GoogleGenerativeAIEmbeddings async gRPC)
try:
    asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

class KnowledgeBase:
    def __init__(self, api_key: str):
        self.api_key = api_key
        os.environ["GOOGLE_API_KEY"] = api_key

        # Initialize embedding model
        self.embedding_model = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=self.api_key
        )

        self.vector_store = None

    def load_file(self, file_path: str) -> str:
        """Extract text from PDF, DOCX, or TXT file."""
        ext = os.path.splitext(file_path)[1].lower()
        text = ""

        if ext == ".pdf":
            reader = PdfReader(file_path)
            text = "\n".join(
                [page.extract_text() or "" for page in reader.pages]
            )
        elif ext == ".docx":
            doc = docx.Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
        elif ext == ".txt":
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
        else:
            raise ValueError("Unsupported file type. Use PDF, DOCX, or TXT.")

        if not text.strip():
            raise ValueError(f"No text could be extracted from {file_path}")

        return text

    def chunk_text(self, text: str, source: str = ""):
        """Split text into smaller chunks with metadata."""
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        return splitter.create_documents([text], metadatas=[{"source": source}])

    def add_file(self, file_path: str):
        """Add a new file to the vector store."""
        text = self.load_file(file_path)
        docs = self.chunk_text(text, source=os.path.basename(file_path))

        if self.vector_store is None:
            self.vector_store = FAISS.from_documents(docs, self.embedding_model)
        else:
            self.vector_store.add_documents(docs)

    def build(self, file_paths: list[str]):
        """Build the knowledge base from a list of file paths."""
        for path in file_paths:
            self.add_file(path)

    def retrieve(self, query: str, k: int = 3):
        """Retrieve top-k relevant chunks for a query."""
        if self.vector_store is None:
            return []
        return self.vector_store.similarity_search(query, k=k)
