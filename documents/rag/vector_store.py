import os
import shutil
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

_embedding_model = None
_vector_db = None


class VectorStore:

    def __init__(self, persist_directory="vector_db"):

        global _embedding_model

        self.persist_directory = persist_directory

        # Load embedding model only once
        if _embedding_model is None:

            print("Loading embedding model...")

            _embedding_model = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )

            print("Embedding model loaded.")

        self.embedding_model = _embedding_model

    def create_vector_store(self, chunks):
        """
        Create a new Chroma vector database.
        """

        global _vector_db

        _vector_db = Chroma.from_documents(
            documents=chunks,
            embedding=self.embedding_model,
            persist_directory=self.persist_directory,
        )

        return _vector_db

    def load_vector_store(self):
        """
        Load existing Chroma DB.

        Uses cached instance if already loaded.
        """

        global _vector_db

        if _vector_db is None:

            print("Loading Chroma database...")

            _vector_db = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embedding_model,
            )

            print("Chroma database loaded.")

        return _vector_db

    def clear_vector_store(self):
        """
        Delete existing vector database.
        """

        global _vector_db

        if os.path.exists(self.persist_directory):

            shutil.rmtree(self.persist_directory)

        _vector_db = None