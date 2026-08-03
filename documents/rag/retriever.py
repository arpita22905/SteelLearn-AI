"""
retriever.py

Retrieves relevant chunks from the Chroma Vector Database.

Optimized:
- Vector database is loaded only once.
- Retriever is created only once.
"""

from typing import List
from langchain_core.documents import Document
from documents.rag.vector_store import VectorStore

_retriever = None


class DocumentRetriever:

    def __init__(self):

        global _retriever

        if _retriever is None:

            print("Creating Retriever...")

            vector_store = VectorStore().load_vector_store()

            _retriever = vector_store.as_retriever(

                search_type="similarity",

                search_kwargs={
                    "k": 5
                }

            )

            print("Retriever Ready.")

        self.retriever = _retriever

    def retrieve(
        self,
        query: str,
    ) -> List[Document]:
        """
        Retrieve relevant document chunks.

        Args:
            query (str)

        Returns:
            List[Document]
        """

        try:

            return self.retriever.invoke(query)

        except Exception as e:

            print("Retriever Error:", e)

            return []