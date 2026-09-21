"""
Local Knowledge Vault for OFFLINE GENIUS.

Stores and searches user-provided documents locally.
No cloud upload is performed.
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class Document:
    """Represents a locally indexed document."""

    name: str
    path: str
    content: str


class KnowledgeVault:
    """
    Local document storage and search layer.

    The prototype uses simple text matching.
    Semantic embeddings and FAISS can be connected later.
    """

    SUPPORTED_EXTENSIONS = {
        ".txt",
        ".md",
        ".py",
        ".js",
        ".html",
        ".css",
    }

    def __init__(self):
        self.documents: list[Document] = []

    def add_file(self, file_path: str) -> bool:
        """Add a supported local text file to the vault."""

        path = Path(file_path)

        if not path.exists():
            return False

        if path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            return False

        try:
            content = path.read_text(
                encoding="utf-8",
                errors="ignore",
            )

            self.documents.append(
                Document(
                    name=path.name,
                    path=str(path),
                    content=content,
                )
            )

            return True

        except OSError:
            return False

    def search(self, query: str) -> list[Document]:
        """
        Search locally indexed documents.

        Returns documents containing the search terms.
        """

        if not query.strip():
            return []

        query_words = query.lower().split()
        results = []

        for document in self.documents:
            content = document.content.lower()

            if all(word in content for word in query_words):
                results.append(document)

        return results

    def document_count(self) -> int:
        """Return the number of documents currently indexed."""
        return len(self.documents)


if __name__ == "__main__":
    vault = KnowledgeVault()

    print("OFFLINE GENIUS - Local Knowledge Vault")
    print("Cloud upload: DISABLED")
    print("Documents indexed:", vault.document_count())
