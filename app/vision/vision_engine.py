"""
Local vision engine for OFFLINE GENIUS.

Provides an interface for connecting a local
vision-language model in the future.
"""

from dataclasses import dataclass

from .image_analyzer import ImageAnalyzer


@dataclass
class VisionResult:
    """Result returned by the local vision engine."""

    description: str
    model: str = "local-vision-demo"
    device: str = "CPU"


class VisionEngine:
    """Local-first vision analysis interface."""

    def __init__(
        self,
        model_name: str = "local-vision-demo",
    ):
        self.model_name = model_name
        self.device = "CPU"
        self.image_analyzer = ImageAnalyzer()

    def status(self) -> dict:
        """Return the current vision system status."""

        return {
            "model": self.model_name,
            "device": self.device,
            "network_required": False,
            "data_sent_to_cloud": False,
        }

    def analyze_image(self, image_path: str) -> VisionResult:
        """
        Analyze a local image.

        The current version provides a prototype response.
        A local vision-language model can be connected later.
        """

        description = self.image_analyzer.describe(image_path)

        return VisionResult(
            description=description,
            model=self.model_name,
            device=self.device,
        )


if __name__ == "__main__":
    engine = VisionEngine()

    print("OFFLINE GENIUS - Local Vision Engine")
    print(engine.status())
