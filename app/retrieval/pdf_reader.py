"""
PDF reader for OFFLINE GENIUS.

Extracts text from PDF files locally.
No document is uploaded to the cloud.
"""

from pathlib import Path

from pypdf import PdfReader


def extract_text(pdf_path: str) -> str:
    """
    Extract all readable text from a local PDF.

    Args:
        pdf_path: Path to the PDF file.

    Returns:
        Extracted text as a single string.
    """

    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    if path.suffix.lower() != ".pdf":
        raise ValueError("The selected file is not a PDF.")

    reader = PdfReader(str(path))

    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n\n".join(pages)


if __name__ == "__main__":
    print("OFFLINE GENIUS - Local PDF Reader")
    print("PDF processing: LOCAL")
    print("Cloud upload: DISABLED")
