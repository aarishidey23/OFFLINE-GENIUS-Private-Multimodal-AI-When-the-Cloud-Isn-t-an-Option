"""
Semantic search for OFFLINE GENIUS.

Uses local sentence-transformers embeddings and FAISS
to find the most relevant document sections.
"""

from dataclasses import dataclass

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


@dataclass
class SearchResult:
    """A semantic search result."""

    document_name: str
    text: str
    score: float


class SemanticSearch:
    """Local semantic search engine."""

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
    ):
        self.model_name = model_name

        print("Loading local embedding model...")
        self.model = SentenceTransformer(model_name)

        self.texts: list[str] = []
        self.document_names: list[str] = []
        self.index = None

    def add_text(
        self,
        text: str,
        document_name: str,
    ) -> None:
        """Add one document section to the local index."""

        if not text.strip():
            return

        self.texts.append(text)
        self.document_names.append(document_name)

        self._rebuild_index()

    def add_texts(
        self,
        texts: list[str],
        document_name: str,
    ) -> None:
        """Add multiple document sections."""

        for text in texts:

            if text.strip():

                self.texts.append(text)
                self.document_names.append(
                    document_name
                )

        self._rebuild_index()

    def _rebuild_index(self) -> None:
        """Build the local FAISS index."""

        if not self.texts:
            self.index = None
            return

        embeddings = self.model.encode(
            self.texts,
            convert_to_numpy=True,
            show_progress_bar=False,
        ).astype("float32")

        # Normalize embeddings so inner product
        # behaves like cosine similarity.
        faiss.normalize_L2(embeddings)

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatIP(
            dimension
        )

        self.index.add(embeddings)

    def search(
        self,
        query: str,
        top_k: int = 3,
    ) -> list[SearchResult]:
        """Find the most semantically relevant sections."""

        if not query.strip():
            return []

        if self.index is None:
            return []

        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
            show_progress_bar=False,
        ).astype("float32")

        faiss.normalize_L2(
            query_embedding
        )

        number_of_results = min(
            top_k,
            len(self.texts),
        )

        scores, indices = self.index.search(
            query_embedding,
            number_of_results,
        )

        results = []

        for score, index in zip(
            scores[0],
            indices[0],
        ):

            if index < 0:
                continue

            results.append(
                SearchResult(
                    document_name=self.document_names[
                        index
                    ],
                    text=self.texts[index],
                    score=float(score),
                )
            )

        return results

    def clear(self) -> None:
        """Clear the local semantic index."""

        self.texts.clear()
        self.document_names.clear()
        self.index = None


if __name__ == "__main__":

    print("=" * 60)
    print("OFFLINE GENIUS - Semantic Search")
    print("=" * 60)
    print("Embeddings: LOCAL")
    print("Vector database: FAISS")
    print("Cloud document upload: DISABLED")
    print("=" * 60)
