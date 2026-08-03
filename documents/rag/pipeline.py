from documents.rag.loader import DocumentLoader
from documents.rag.splitter import DocumentSplitter
from documents.rag.vector_store import VectorStore


class RAGPipeline:

    def __init__(self):

        self.loader = DocumentLoader()
        self.splitter = DocumentSplitter()
        self.vector_store = VectorStore()

    def build_pipeline(self, pdf_path):
        """
        Build a fresh vector database from an uploaded PDF.

        Args:
            pdf_path (str): Path to uploaded PDF

        Returns:
            Chroma
        """

        print("\n========== BUILDING RAG PIPELINE ==========\n")

        print("Loading PDF...")
        documents = self.loader.load_pdf(pdf_path)
        print(f"Loaded {len(documents)} pages.")

        print("Splitting document...")
        chunks = self.splitter.split_documents(documents)
        print(f"Created {len(chunks)} chunks.")

        print("Updating vector database...")

        vector_db = self.vector_store.create_vector_store(chunks)

        print("RAG pipeline built successfully.\n")

        return vector_db