import os
import asyncio
import streamlit as st
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from pypdf import PdfReader

# Ensure an event loop exists for async operations
try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())


class KnowledgeBase:
    def __init__(self):
        self.embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        self.vector_store = None

    

    def add_document(self, text):
        """Add text to the knowledge base."""
        self.documents.append(text)

    def query(self, question):
        """Simple placeholder retrieval (later replace with embeddings)."""
        # For now, just return all documents
        return self.documents

# ---------------------------
# File loading helpers
# ---------------------------

def load_txt(file_path):
    """Read a text file and return its content."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def load_pdf(file_path):
    """Read a PDF file and return its extracted text."""
    text = ""
    reader = PdfReader(file_path)
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def load_document(file_path):
    """Load document content depending on type."""
    ext = os.path.splitext(file_path)[-1].lower()
    if ext == ".txt":
        return load_txt(file_path)
    elif ext == ".pdf":
        return load_pdf(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")
    
    
    
def load_document(self, file_path):
        """Load documents based on file type"""
        if file_path.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        elif file_path.endswith(".txt"):
            loader = TextLoader(file_path)
        elif file_path.endswith(".docx"):
            loader = Docx2txtLoader(file_path)
        else:
            raise ValueError("Unsupported file format")

        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        docs = text_splitter.split_documents(documents)

        # Create FAISS vector store
        self.vector_store = FAISS.from_documents(docs, self.embedding_model)

def similarity_search(self, query, k=3):
        """Retrieve similar documents"""
        if not self.vector_store:
            return ["No knowledge base loaded yet."]
        results = self.vector_store.similarity_search(query, k=k)
        return [doc.page_content for doc in results]
