import os
import asyncio
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader

# Ensure an event loop exists for async operations
try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())


class KnowledgeBase:
    def __init__(self):
        self.embedding_model = GoogleGenerativeAIEmbeddings(model="text-embedding-3-small")
        self.vector_store = None  # Holds FAISS index

    def load_document(self, file_path):
        """Load documents based on file type and add them to the FAISS vector store."""
        # Select loader by file extension
        if file_path.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        elif file_path.endswith(".txt"):
            loader = TextLoader(file_path)
        elif file_path.endswith(".docx"):
            loader = Docx2txtLoader(file_path)
        else:
            raise ValueError("Unsupported file format")

        # Load and split into chunks
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        docs = text_splitter.split_documents(documents)

        # Create FAISS index or add to existing one
        if self.vector_store is None:
            self.vector_store = FAISS.from_documents(docs, self.embedding_model)
        else:
            self.vector_store.add_documents(docs)

    def similarity_search(self, query, k=3):
        """Retrieve top-k similar documents from the knowledge base."""
        if not self.vector_store:
            return ["⚠️ No knowledge base loaded yet. Please upload a document."]
        results = self.vector_store.similarity_search(query, k=k)
        return [doc.page_content for doc in results]
