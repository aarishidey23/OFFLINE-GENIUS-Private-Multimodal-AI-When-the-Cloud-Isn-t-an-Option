"""
Local Knowledge Vault for OFFLINE GENIUS.

Stores document sections locally and optionally uses
semantic search to find the most relevant passages.
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class Document:
    """Represents a locally indexed document section."""

    name: str
    path: str
    content: str


class KnowledgeVault:
    """
    Local document storage and search layer.

    Documents are split into smaller sections.
    Semantic search can be enabled when the local
    embedding dependencies are available.
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

        self.semantic_search = None

        # Semantic search is optional during development.
        # If its dependencies are unavailable, the
        # application can still use keyword search.
        try:
            from .semantic_search import SemanticSearch

            self.semantic_search = SemanticSearch()

        except Exception as error:
            print(
                "Semantic search unavailable."
            )
            print(
                f"Reason: {error}"
            )
            print(
                "Using local keyword search instead."
            )

    def add_file(self, file_path: str) -> bool:
        """Add a supported local text file."""

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
        """Split a document and add its sections locally."""

        if not content.strip():
            return

        chunks = self._create_chunks(content)

        for number, chunk in enumerate(
            chunks,
            start=1,
        ):

            document = Document(
                name=f"{name} — Section {number}",
                path=path,
                content=chunk,
            )

            self.documents.append(document)

            # Add the same section to the semantic index.
            if self.semantic_search is not None:

                try:
                    self.semantic_search.add_text(
                        chunk,
                        document.name,
                    )

                except Exception as error:

                    print(
                        "Could not add section to "
                        "semantic index:"
                    )

                    print(error)

    def _create_chunks(
        self,
        content: str,
    ) -> list[str]:
        """Split document text into overlapping sections."""

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

    def search(
        self,
        query: str,
    ) -> list[Document]:
        """
        Search the local Knowledge Vault.

        Semantic search is preferred.
        Keyword search is used as a fallback.
        """

        if not query.strip():
            return []

        # Try semantic search first.
        if self.semantic_search is not None:

            try:

                results = self.semantic_search.search(
                    query,
                    top_k=5,
                )

                if results:

                    documents = []

                    for result in results:

                        documents.append(
                            Document(
                                name=result.document_name,
                                path="",
                                content=result.text,
                            )
                        )

                    return documents

            except Exception as error:

                print(
                    "Semantic search failed."
                )

                print(error)

        # Fallback: keyword search.
        return self._keyword_search(query)

    def _keyword_search(
        self,
        query: str,
    ) -> list[Document]:
        """Search document sections using keywords."""

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

        scored_results.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return [
            document
            for score, document
            in scored_results[:5]
        ]

    def document_count(self) -> int:
        """Return the number of indexed sections."""

        return len(self.documents)


if __name__ == "__main__":

    vault = KnowledgeVault()

    print(
        "OFFLINE GENIUS - Local Knowledge Vault"
    )

    print(
        "Cloud upload: DISABLED"
    )

    print(
        "Semantic search:",
        "AVAILABLE"
        if vault.semantic_search is not None
        else "FALLBACK MODE",
    )

    print(
        "Indexed sections:",
        vault.document_count(),
    )
