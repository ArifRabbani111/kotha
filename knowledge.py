# knowledge.py
import os
import asyncio
from typing import Callable, Optional

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from langchain.vectorstores import FAISS

# Two embedding options - API embedding (e.g., Google/OpenAI) or local HuggingFace
# If you use API embeddings, pass an embedding object into KnowledgeBase(..., api_embedding=...)
from langchain.embeddings import HuggingFaceEmbeddings

# Ensure event loop for any async libs that need it
try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())


class KnowledgeBase:
    def __init__(
        self,
        api_embedding=None,          # optional API embedding instance (OpenAI/Google)
        local_embedding_model="sentence-transformers/all-MiniLM-L6-v2",
    ):
        """
        If api_embedding is provided, we try that first and fall back to local HF embeddings on failure.
        """
        self.api_embedding = api_embedding
        self.local_embedding_model = local_embedding_model
        self.embedding = None        # resolved embedding instance (either api_embedding or local HF)
        self.vector_store = None
        self._initialized_with = None  # "api" or "local"

    def _ensure_embedding(self, use_local=False):
        """Create or set embedding instance. If use_local True, force HF local embedding."""
        if use_local or self.api_embedding is None:
            # Use local HF embeddings
            self.embedding = HuggingFaceEmbeddings(model_name=self.local_embedding_model)
            self._initialized_with = "local"
        else:
            self.embedding = self.api_embedding
            self._initialized_with = "api"

    def load_document(self, file_path: str, progress_callback: Optional[Callable[[int, int], None]] = None, chunk_size: int = 1000, chunk_overlap: int = 100):
        """
        Load file, split into chunks, and add to FAISS. If API embedding fails due to quota/errors,
        automatically fall back to local HF embeddings.

        progress_callback(current_chunks_processed, total_chunks) -> None
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"{file_path} not found")

        # select loader
        if file_path.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
            documents = loader.load()
        elif file_path.endswith(".txt"):
            loader = TextLoader(file_path, encoding="utf-8")
            documents = loader.load()
        elif file_path.endswith(".docx"):
            loader = Docx2txtLoader(file_path)
            documents = loader.load()
        else:
            raise ValueError("Unsupported file format")

        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        docs = splitter.split_documents(documents)
        total = len(docs)

        # Try using API embedding first if available, else go directly to local
        tried_local = False
        for attempt_local in (False, True):
            try:
                self._ensure_embedding(use_local=attempt_local)
                # create or add to FAISS store in one shot (this will run embedding)
                if self.vector_store is None:
                    # from_documents will compute embeddings and build index
                    self.vector_store = FAISS.from_documents(docs, self.embedding)
                else:
                    # add_documents will compute embeddings for new docs and add them
                    self.vector_store.add_documents(docs)
                # success: report progress completion, then return
                if progress_callback:
                    progress_callback(total, total)
                return {"status": "ok", "backend": self._initialized_with, "indexed_chunks": total}
            except Exception as e:
                # If we failed with API-related error, log and fall back to local.
                # Caller/UI should show friendly message.
                last_exception = e
                tried_local = True if attempt_local else False
                # Clean up partially created vector store if it's in inconsistent state
                try:
                    if self.vector_store is not None and self._initialized_with == "api":
                        # best effort: delete/clear to allow local rebuild
                        self.vector_store = None
                except Exception:
                    self.vector_store = None
                # If we already tried local and it still failed -> re-raise
                if attempt_local:
                    raise RuntimeError(f"Embeddings failed with both API and local backend. Last error: {e}") from e
                # Otherwise loop will retry with local embeddings

        # unreachable normally
        raise RuntimeError("Failed to build vector store.") from last_exception

    def similarity_search(self, query: str, k: int = 3):
        """Return top-k most relevant text chunks (page_content)."""
        if self.vector_store is None:
            return []
        results = self.vector_store.similarity_search(query, k=k)
        return [doc.page_content for doc in results]

    def clear(self):
        """Clear in-memory index (doesn't delete any persisted files)."""
        self.vector_store = None
        self._initialized_with = None
