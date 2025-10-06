from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List, Dict


class PDFProcessor:
    """Handles PDF text extraction and chunking."""

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )

    def extract_text_with_pages(self, pdf_path: str) -> List[Dict[str, any]]:
        """
        Extract text from PDF, preserving page numbers.

        Returns list of dicts: [{"page_number": 1, "text": "..."}, ...]
        """
        reader = PdfReader(pdf_path)
        pages_data = []

        for page_num, page in enumerate(reader.pages, start=1):
            text = page.extract_text()
            if text.strip():  # Only include pages with actual text
                pages_data.append({
                    "page_number": page_num,
                    "text": text
                })

        return pages_data

    def chunk_text(self, pages_data: List[Dict[str, any]]) -> List[Dict[str, any]]:
        """
        Chunk text from pages, preserving metadata.

        Returns list of dicts with: page_number, chunk_index, text
        """
        chunks_with_metadata = []
        chunk_index = 0

        for page_data in pages_data:
            page_number = page_data["page_number"]
            text = page_data["text"]

            # Split text into chunks
            text_chunks = self.text_splitter.split_text(text)

            # Add metadata to each chunk
            for chunk_text in text_chunks:
                chunks_with_metadata.append({
                    "page_number": page_number,
                    "chunk_index": chunk_index,
                    "text": chunk_text
                })
                chunk_index += 1

        return chunks_with_metadata

    def process_pdf(self, pdf_path: str) -> List[Dict[str, any]]:
        """
        Complete pipeline: extract text and chunk it.

        Returns list of chunks with metadata.
        """
        pages_data = self.extract_text_with_pages(pdf_path)
        chunks = self.chunk_text(pages_data)
        return chunks
