"""
Local Answer Generator for OFFLINE GENIUS.
Generates clean, direct offline responses without technical metadata in the main answer.
"""

from dataclasses import dataclass
from typing import List, Any


@dataclass
class GeneratedAnswer:
    answer: str
    source: str


class LocalAnswerGenerator:
    """Processes search results locally and formats clean AI output."""

    def generate(self, question: str, retrieved_sections: List[Any]) -> GeneratedAnswer:
        if not retrieved_sections:
            return GeneratedAnswer(
                answer="I couldn't find enough information in your local documents.",
                source="Local Knowledge Vault",
            )

        extracted_texts = []
        doc_name = "Local Document"

        for item in retrieved_sections[:3]:
            # Extract content from Document object
            if hasattr(item, "page_content"):
                text = item.page_content.strip()
                # Check for content attribute if page_content is empty
                if not text and hasattr(item, "content"):
                    text = str(item.content).strip()
                extracted_texts.append(text)

                if hasattr(item, "metadata") and isinstance(item.metadata, dict):
                    doc_name = item.metadata.get("source", doc_name)
                elif hasattr(item, "name"):
                    doc_name = getattr(item, "name")

            # Extract content if item is a dictionary
            elif isinstance(item, dict):
                text = item.get("content", item.get("page_content", "")).strip()
                extracted_texts.append(text)
                doc_name = item.get("name", doc_name)

            # Fallback for direct string or generic object
            else:
                if hasattr(item, "content"):
                    extracted_texts.append(str(item.content).strip())
                else:
                    extracted_texts.append(str(item).strip())

        # Clean up any leftover file path text in the answer body
        clean_answers = [
            t for t in extracted_texts 
            if t and not t.lower().startswith("document(") and "Users\\" not in t
        ]

        final_answer = "\n".join(clean_answers) if clean_answers else "Information retrieved locally."
        
        # Keep file names clean without full system paths
        if "\\" in doc_name or "/" in doc_name:
            import os
            doc_name = os.path.basename(doc_name)

        return GeneratedAnswer(
            answer=final_answer,
            source=f"{doc_name} — Section 1"
        )