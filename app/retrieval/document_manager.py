"""
Document manager for OFFLINE GENIUS.

Connects local PDF files with the Local Knowledge Vault.
"""

from pathlib import Path

from .knowledge_vault import KnowledgeVault
from .pdf_reader import extract_text


class DocumentManager:
    """Manage local documents for the Knowledge Vault."""

    def __init__(self):
        self.vault = KnowledgeVault()

    def add_pdf(self, pdf_path: str) -> bool:
        """Read a local PDF and split it into searchable sections."""

        path = Path(pdf_path)

        if not path.exists():
            return False

        if path.suffix.lower() != ".pdf":
            return False

        try:
            content = extract_text(str(path))

            self.vault.add_document(
                name=path.name,
                path=str(path),
                content=content,
            )

            return True

        except (OSError, ValueError):
            return False

    def search(self, query: str):
        """Search locally indexed document sections."""

        return self.vault.search(query)

    def count(self) -> int:
        """Return the number of indexed document sections."""

        return self.vault.document_count()


if __name__ == "__main__":

    manager = DocumentManager()

    print("OFFLINE GENIUS - Document Manager")
    print("Local document processing: ON")
    print("Cloud upload: OFF")
    print(
        "Indexed document sections:",
        manager.count(),
    )
