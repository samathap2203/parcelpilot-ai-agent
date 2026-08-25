from pathlib import Path
from typing import Dict, List

from pypdf import PdfReader


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DOCUMENTS_DIR = PROJECT_ROOT / "data"


PDF_FILES = [
    "01_Support_Policy_v3_CURRENT.pdf",
    "02_Support_Policy_v2_DEPRECATED.pdf",
    "03_Cancellation_and_Service_Credit_SOP_v4.pdf",
    "04_Product_Operations_Guide_and_Known_Issues.pdf",
    "05_Northstar_Logistics_Enterprise_Agreement.pdf",
    "06_LumenWorks_Service_Agreement.pdf",
]


def extract_pdf_text(file_path: Path) -> str:
    """Extract text from all pages of a PDF."""

    reader = PdfReader(file_path)

    pages = []

    for page in reader.pages:
        text = page.extract_text() or ""
        pages.append(text)

    return "\n".join(pages).strip()


def split_text(
    text: str,
    chunk_size: int = 1200,
    overlap: int = 200,
) -> List[str]:
    """Split document text into overlapping chunks."""

    if not text:
        return []

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = end - overlap

    return chunks


def ingest_documents() -> List[Dict]:
    """
    Read the supplied ParcelPilot PDFs and return
    searchable document chunks with metadata.
    """

    documents = []

    for filename in PDF_FILES:
        file_path = DOCUMENTS_DIR / filename

        if not file_path.exists():
            raise FileNotFoundError(
                f"Required document not found: {file_path}"
            )

        text = extract_pdf_text(file_path)
        chunks = split_text(text)

        for index, chunk in enumerate(chunks):
            documents.append(
                {
                    "document": filename,
                    "chunk_id": index,
                    "text": chunk,
                }
            )

    return documents