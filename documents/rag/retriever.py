from typing import List
from langchain_core.documents import Document
from documents.rag.vector_store import VectorStore

class DocumentRetriever:

    def __init__(self):

        self.vector_store = VectorStore().load_vector_store()

    def retrieve(
        self,
        query: str,
        k: int = 4
    ) -> List[Document]:

        try:

            retriever = self.vector_store.as_retriever(

                search_type="similarity",

                search_kwargs={
                    "k": k
                }

            )

            return retriever.invoke(query)

        except Exception:

            return []