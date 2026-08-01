import os
import shutil
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

class VectorStore:

    def __init__(self, persist_directory="vector_db"):

        self.persist_directory = persist_directory

        self.embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

    def create_vector_store(self, chunks):
        """
        Create a new Chroma database.
        """

        vector_db = Chroma.from_documents(
            documents=chunks,
            embedding=self.embedding_model,
            persist_directory=self.persist_directory,
        )

        return vector_db

    def load_vector_store(self):
        """
        Load existing Chroma DB.
        """

        return Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embedding_model,
        )

    def clear_vector_store(self):
        """
        Delete old vector database before creating a new one.
        """

        if os.path.exists(self.persist_directory):
            shutil.rmtree(self.persist_directory)
            print("Old vector database deleted.")