"""
Document manager for OFFLINE GENIUS.

Connects local PDF files with the Local Knowledge Vault.
"""

from pathlib import Path

from .knowledge_vault import Document, KnowledgeVault
from .pdf_reader import extract_text


class DocumentManager:
    """Manage local documents for the Knowledge Vault."""

    def __init__(self):
        self.vault = KnowledgeVault()

    def add_pdf(self, pdf_path: str) -> bool:
        """Read a local PDF and add its extracted content to the vault."""

        path = Path(pdf_path)

        if not path.exists() or path.suffix.lower() != ".pdf":
            return False

        try:
            content = extract_text(str(path))

            self.vault.documents.append(
                Document(
                    name=path.name,
                    path=str(path),
                    content=content,
                )
            )

            return True

        except (OSError, ValueError):
            return False

    def search(self, query: str) -> list[Document]:
        """Search all locally indexed documents."""

        return self.vault.search(query)

    def count(self) -> int:
        """Return the number of indexed documents."""

        return self.vault.document_count()


if __name__ == "__main__":
    manager = DocumentManager()

    print("OFFLINE GENIUS - Document Manager")
    print("Local document processing: ON")
    print("Cloud upload: OFF")
    print("Indexed documents:", manager.count())
