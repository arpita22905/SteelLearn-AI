from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader


class DocumentLoader:

    @staticmethod
    def load_pdf(pdf_path: str):
        """
        Load a PDF file.

        Args:
            pdf_path (str): Path to PDF

        Returns:
            List[Document]
        """

        pdf_path = Path(pdf_path)

        if not pdf_path.exists():
            raise FileNotFoundError(
                f"PDF file not found: {pdf_path}"
            )

        loader = PyPDFLoader(str(pdf_path))

        documents = loader.load()

        return documents