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

    The prototype splits documents into smaller passages
    so searches can return relevant sections instead of
    the entire document.
    """

    SUPPORTED_EXTENSIONS = {
        ".txt",
        ".md",
        ".py",
        ".js",
        ".html",
        ".css",
    }

    def __init__(
        self,
        chunk_size: int = 1200,
        chunk_overlap: int = 200,
    ):
        self.documents: list[Document] = []

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

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

            self.add_document(
                name=path.name,
                path=str(path),
                content=content,
            )

            return True

        except OSError:
            return False

    def add_document(
        self,
        name: str,
        path: str,
        content: str,
    ) -> None:
        """
        Add a document and split it into smaller passages.
        """

        if not content.strip():
            return

        chunks = self._create_chunks(content)

        for number, chunk in enumerate(chunks, start=1):

            self.documents.append(
                Document(
                    name=f"{name} — Section {number}",
                    path=path,
                    content=chunk,
                )
            )

    def _create_chunks(self, content: str) -> list[str]:
        """
        Split document text into overlapping chunks.

        Overlap helps preserve context between sections.
        """

        content = content.strip()

        if not content:
            return []

        chunks = []

        start = 0
        content_length = len(content)

        while start < content_length:

            end = min(
                start + self.chunk_size,
                content_length,
            )

            chunk = content[start:end].strip()

            if chunk:
                chunks.append(chunk)

            if end >= content_length:
                break

            start = end - self.chunk_overlap

        return chunks

    def search(self, query: str) -> list[Document]:
        """
        Search locally indexed document sections.

        Results are ranked using simple word matching.
        """

        if not query.strip():
            return []

        query_words = query.lower().split()

        scored_results = []

        for document in self.documents:

            content = document.content.lower()

            score = 0

            for word in query_words:
                if word in content:
                    score += 1

            if score > 0:
                scored_results.append(
                    (score, document)
                )

        # Highest matching score first.
        scored_results.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return [
            document
            for score, document in scored_results[:5]
        ]

    def document_count(self) -> int:
        """Return the number of indexed document sections."""

        return len(self.documents)


if __name__ == "__main__":

    vault = KnowledgeVault()

    print("OFFLINE GENIUS - Local Knowledge Vault")
    print("Cloud upload: DISABLED")
    print(
        "Document sections indexed:",
        vault.document_count(),
    )
