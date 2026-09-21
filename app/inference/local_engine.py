"""
Local AI inference layer for OFFLINE GENIUS.

This module provides a simple local-first interface that can later
be connected to a Snapdragon-optimized model runtime.
"""

from dataclasses import dataclass


@dataclass
class InferenceResult:
    """Result returned by the local inference engine."""

    response: str
    model: str = "local-demo-model"
    device: str = "CPU"


class LocalEngine:
    """
    Local-first AI inference interface.

    The model runtime can later be replaced with a supported
    Windows/Snapdragon execution backend without changing the
    rest of the application.
    """

    def __init__(self, model_name: str = "local-demo-model"):
        self.model_name = model_name
        self.device = "CPU"

    def status(self) -> dict:
        """Return the current local inference status."""
        return {
            "model": self.model_name,
            "device": self.device,
            "network_required": False,
            "data_sent_to_cloud": False,
        }

    def generate(self, prompt: str) -> InferenceResult:
        """
        Generate a local response.

        This is currently a prototype response layer.
        A real local model will be connected here later.
        """
        if not prompt.strip():
            return InferenceResult(
                response="Please enter a question.",
                model=self.model_name,
                device=self.device,
            )

        response = (
            "OFFLINE GENIUS received your request locally. "
            "The production version will process this request "
            "using a local AI model without sending your data "
            "to the cloud."
        )

        return InferenceResult(
            response=response,
            model=self.model_name,
            device=self.device,
        )


if __name__ == "__main__":
    engine = LocalEngine()

    print("OFFLINE GENIUS - Local Engine")
    print(engine.status())

    result = engine.generate("What is offline AI?")
    print("\nResponse:")
    print(result.response)
