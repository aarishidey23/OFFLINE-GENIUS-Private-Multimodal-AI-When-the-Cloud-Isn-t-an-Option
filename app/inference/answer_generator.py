"""
Local answer generator for OFFLINE GENIUS.

Turns retrieved document passages into concise answers.
This prototype does not use a cloud API.
"""

import re
from dataclasses import dataclass


@dataclass
class AnswerResult:
    """Answer returned by the local answer layer."""

    answer: str
    source: str
    confidence: str = "LOCAL RETRIEVAL"


class LocalAnswerGenerator:
    """
    Generate concise answers from locally retrieved passages.

    This is a lightweight prototype layer. A local
    generative model can replace it later.
    """

    def generate(
        self,
        question: str,
        passages: list,
    ) -> AnswerResult:
        """Create a concise answer from retrieved passages."""

        if not passages:
            return AnswerResult(
                answer=(
                    "I couldn't find enough information "
                    "in your local documents."
                ),
                source="Local Knowledge Vault",
            )

        best_passage = passages[0]

        text = best_passage.content.strip()

        answer = self._extract_relevant_sentences(
            question,
            text,
        )

        return AnswerResult(
            answer=answer,
            source=best_passage.name,
        )

    def _extract_relevant_sentences(
        self,
        question: str,
        text: str,
    ) -> str:
        """Select the most relevant sentences locally."""

        sentences = re.split(
            r"(?<=[.!?])\s+",
            text,
        )

        if not sentences:
            return text[:500]

        question_words = {
            word.lower()
            for word in re.findall(
                r"\b[a-zA-Z0-9%]+\b",
                question,
            )
            if len(word) > 2
        }

        scored = []

        for sentence in sentences:

            sentence_words = {
                word.lower()
                for word in re.findall(
                    r"\b[a-zA-Z0-9%]+\b",
                    sentence,
                )
            }

            score = len(
                question_words
                & sentence_words
            )

            # Give sentences containing numbers
            # a small priority for factual questions.
            if re.search(r"\d", sentence):
                score += 1

            if score > 0:
                scored.append(
                    (score, sentence.strip())
                )

        scored.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        if scored:
            selected = [
                sentence
                for score, sentence
                in scored[:2]
            ]

            return " ".join(selected)

        return sentences[0].strip()


if __name__ == "__main__":

    generator = LocalAnswerGenerator()

    demo_passage = type(
        "DemoPassage",
        (),
        {
            "name": "Saathi.pdf — Section 1",
            "content": (
                "A 2022 NCRB-based figure reports "
                "that 96.6% of registered rape cases "
                "had an offender known to the victim."
            ),
        },
    )()

    result = generator.generate(
        "How many rape cases involved someone "
        "the victim already knew?",
        [demo_passage],
    )

    print("OFFLINE GENIUS")
    print("Answer:")
    print(result.answer)
    print("Source:", result.source)
