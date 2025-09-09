import os
import chromadb
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_community.document_loaders import PyPDFLoader

DB_DIR = "chroma_db"

class KnowledgeBase:
    def __init__(self):
        # Initialize Chroma
        self.client = chromadb.PersistentClient(path=DB_DIR)
        self.collection = self.client.get_or_create_collection("chatbot_docs")

        # Embeddings model (Gemini)
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    def add_pdf(self, pdf_path):
        """Load a PDF and store embeddings"""
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"{pdf_path} not found")

        loader = PyPDFLoader(pdf_path)
        pages = loader.load()

        # Split text into chunks
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        docs = splitter.split_documents(pages)

        # Store in Chroma
        for i, doc in enumerate(docs):
            self.collection.add(
                documents=[doc.page_content],
                metadatas=[{"source": pdf_path}],
                ids=[f"{pdf_path}-{i}"]
            )

        print(f"✅ Added {len(docs)} chunks from {pdf_path}")

    def query(self, question, top_k=3):
        """Retrieve top-k relevant docs"""
        results = self.collection.query(
            query_texts=[question],
            n_results=top_k
        )
        return results["documents"][0] if results["documents"] else []
