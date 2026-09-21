"""
Connects Offline Vision with the Local Knowledge Vault.

This allows visual information to become part of the
user's private local knowledge workflow.
"""

from dataclasses import dataclass

from .vision_engine import VisionEngine


@dataclass
class VisionKnowledgeResult:
    """Result from visual analysis for the knowledge workflow."""

    filename: str
    description: str
    stored_locally: bool = True


class VisionKnowledge:
    """Manage locally analyzed visual information."""

    def __init__(self):
        self.vision_engine = VisionEngine()
        self.visual_documents: list[VisionKnowledgeResult] = []

    def analyze_and_store(
        self,
        image_path: str,
    ) -> VisionKnowledgeResult:
        """
        Analyze an image locally and store its description
        in the local visual knowledge collection.
        """

        result = self.vision_engine.analyze_image(image_path)

        filename = image_path.split("/")[-1]
        filename = filename.split("\\")[-1]

        visual_result = VisionKnowledgeResult(
            filename=filename,
            description=result.description,
        )

        self.visual_documents.append(visual_result)

        return visual_result

    def search_visual_knowledge(
        self,
        query: str,
    ) -> list[VisionKnowledgeResult]:
        """Search locally stored visual information."""

        if not query.strip():
            return []

        query_words = query.lower().split()
        results = []

        for document in self.visual_documents:
            searchable_text = (
                document.filename
                + " "
                + document.description
            ).lower()

            if all(
                word in searchable_text
                for word in query_words
            ):
                results.append(document)

        return results


if __name__ == "__main__":
    vision_knowledge = VisionKnowledge()

    print("OFFLINE GENIUS - Vision Knowledge")
    print("Visual data storage: LOCAL")
    print("Cloud upload: DISABLED")
    print(
        "Visual documents:",
        len(vision_knowledge.visual_documents),
    )
