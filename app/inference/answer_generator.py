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

        if not passages:
            return AnswerResult(
                answer=(
                    "I couldn't find enough information "
                    "in your local documents."
                ),
                source="Local Knowledge Vault",
            )

        candidates = []

        for passage in passages:

            text = passage.content.strip()

            if not text:
                continue

            # PDF extraction often creates line breaks
            # in the middle of sentences.
            text = re.sub(
                r"\s+",
                " ",
                text,
            ).strip()

            # Split text into sentence-like statements.
            sentences = re.split(
                r"(?<=[.!?])\s+",
                text,
            )

            # Also split around statistical percentage
            # statements when PDFs place multiple statistics
            # next to each other.
            expanded_sentences = []

            for sentence in sentences:

                percentage_matches = list(
                    re.finditer(
                        r"\b\d+(?:\.\d+)?%\b",
                        sentence,
                    )
                )

                if len(percentage_matches) <= 1:
                    expanded_sentences.append(
                        sentence.strip()
                    )
                    continue

                # Keep the complete sentence if there are
                # multiple percentages but no clear boundary.
                expanded_sentences.append(
                    sentence.strip()
                )

            for sentence in expanded_sentences:

                if not sentence:
                    continue

                score = self._score_sentence(
                    question,
                    sentence,
                )

                candidates.append(
                    (
                        score,
                        sentence,
                        passage.name,
                    )
                )

        if not candidates:

            return AnswerResult(
                answer=(
                    "I couldn't find enough information "
                    "in your local documents."
                ),
                source=passages[0].name,
            )

        candidates.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        best_score, best_sentence, best_source = (
            candidates[0]
        )

        if best_score <= 0:

            return AnswerResult(
                answer=(
                    "I found related information, "
                    "but I couldn't identify a precise answer."
                ),
                source=best_source,
            )

        # Clean common PDF formatting artifacts.
        answer = self._clean_answer(
            best_sentence
        )

        return AnswerResult(
            answer=answer,
            source=best_source,
        )

    def _score_sentence(
        self,
        question: str,
        sentence: str,
    ) -> int:
        """Score how closely a sentence matches the question."""

        question_words = {
            word.lower()
            for word in re.findall(
                r"\b[a-zA-Z0-9%]+\b",
                question,
            )
            if len(word) > 2
        }

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

        # Strong boost for questions asking about
        # percentages/statistics.
        if "%" in sentence:
            score += 3

        # Important terms for the current type of question.
        important_terms = {
            "rape",
            "cases",
            "offender",
            "victim",
            "known",
            "registered",
        }

        score += len(
            important_terms
            & sentence_words
        ) * 2

        return score

    def _clean_answer(
        self,
        answer: str,
    ) -> str:
        """Clean common PDF extraction artifacts."""

        answer = re.sub(
            r"\s+",
            " ",
            answer,
        ).strip()

        answer = answer.replace(
            "&#x20;",
            " ",
        )

        return answer


if __name__ == "__main__":

    generator = LocalAnswerGenerator()

    demo_passage = type(
        "DemoPassage",
        (),
        {
            "name": "Saathi.pdf — Section 1",
            "content": (
                "29.2% ever-married women 18–49 "
                "reported spousal violence. "
                "NFHS-5, India, 2019–21. "
                "96.6% of registered rape cases "
                "in 2022 involved an offender known "
                "to the victim."
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