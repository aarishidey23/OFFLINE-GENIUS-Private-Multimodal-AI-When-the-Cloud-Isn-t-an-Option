"""
Semantic search for OFFLINE GENIUS.

Uses a local sentence-transformers model and FAISS
to search documents without sending data to the cloud.
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

        # The model is downloaded once and can then be
        # used locally without sending document data to
        # an external AI service.
        self.model = SentenceTransformer(model_name)

        self.texts: list[str] = []
        self.document_names: list[str] = []
        self.index = None

    def add_text(
        self,
        text: str,
        document_name: str,
    ) -> None:
        """Add text to the local semantic index."""

        if not text.strip():
            return

        self.texts.append(text)
        self.document_names.append(document_name)

        embeddings = self.model.encode(
            self.texts,
            convert_to_numpy=True,
        ).astype("float32")

        faiss.normalize_L2(embeddings)

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(embeddings)

    def search(
        self,
        query: str,
        top_k: int = 3,
    ) -> list[SearchResult]:
        """Search the local semantic index."""

        if not query.strip() or self.index is None:
            return []

        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
        ).astype("float32")

        faiss.normalize_L2(query_embedding)

        scores, indices = self.index.search(
            query_embedding,
            min(top_k, len(self.texts)),
        )

        results = []

        for score, index in zip(scores[0], indices[0]):
            if index < 0:
                continue

            results.append(
                SearchResult(
                    document_name=self.document_names[index],
                    text=self.texts[index],
                    score=float(score),
                )
            )

        return results


if __name__ == "__main__":
    print("OFFLINE GENIUS - Semantic Search")
    print("Embeddings: LOCAL")
    print("Vector database: FAISS")
    print("Cloud document upload: DISABLED")
