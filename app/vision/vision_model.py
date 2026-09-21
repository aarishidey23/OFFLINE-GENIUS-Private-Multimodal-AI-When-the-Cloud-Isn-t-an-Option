"""
Vision Model Adapter for OFFLINE GENIUS.

This layer separates the application UI from the
actual local vision model/runtime.

The prototype currently provides a safe local fallback.
A real local vision backend can be connected later
without changing the main application UI.

No cloud API is used.
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class VisionModelStatus:
    """Status information for the local vision backend."""

    backend: str
    model_loaded: bool
    execution: str
    cloud_upload: bool


class VisionModelAdapter:
    """
    Hardware/runtime-independent vision model adapter.

    The application talks to this class instead of directly
    depending on a particular AI framework.
    """

    def __init__(self):
        self.model = None
        self.model_name = "Local Vision Backend"

    def status(self) -> VisionModelStatus:
        """Return the current local vision backend status."""

        if self.model is None:
            return VisionModelStatus(
                backend=self.model_name,
                model_loaded=False,
                execution="LOCAL FALLBACK",
                cloud_upload=False,
            )

        return VisionModelStatus(
            backend=self.model_name,
            model_loaded=True,
            execution="LOCAL",
            cloud_upload=False,
        )

    def load_model(self) -> bool:
        """
        Prepare the vision model backend.

        The actual model will be connected here once the
        compatible local runtime is selected.
        """

        # Model loading will be implemented in the next stage.
        self.model = None

        return False

    def analyze(
        self,
        image_path: str,
        question: str = "",
    ) -> str:
        """
        Analyze an image locally.

        Current stage:
            Provides a safe fallback response.

        Future stage:
            Sends the image to a local multimodal model.
        """

        path = Path(image_path)

        if not path.exists():
            return "Image file was not found."

        if not question.strip():
            question = "Describe this image."

        status = self.status()

        if not status.model_loaded:

            return (
                "OFFLINE VISION\n\n"
                "Image received locally.\n\n"
                f"Question: {question}\n\n"
                "Vision model status: "
                "LOCAL MODEL NOT LOADED\n\n"
                "The image remains on this computer. "
                "No cloud upload was used.\n\n"
                "NEXT AI LAYER:\n"
                "A compatible local multimodal model "
                "will be connected to this adapter."
            )

        return (
            "Local vision model processed the image."
        )


if __name__ == "__main__":

    adapter = VisionModelAdapter()
    status = adapter.status()

    print("=" * 60)
    print("OFFLINE GENIUS - VISION MODEL ADAPTER")
    print("=" * 60)
    print(f"Backend: {status.backend}")
    print(f"Model loaded: {status.model_loaded}")
    print(f"Execution: {status.execution}")
    print(f"Cloud upload: {status.cloud_upload}")
    print("=" * 60)
    