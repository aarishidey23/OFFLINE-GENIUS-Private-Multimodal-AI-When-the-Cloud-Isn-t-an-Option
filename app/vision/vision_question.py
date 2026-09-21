"""
Offline Vision Question Engine for OFFLINE GENIUS.

Prototype image understanding layer.
Runs locally and prepares image information for
a future local vision model.

No cloud API is used.
"""

from pathlib import Path

from PIL import Image


class OfflineVisionQuestion:
    """Answer basic questions about a local image."""

    def __init__(self, image_path: str):
        self.image_path = Path(image_path)

        if not self.image_path.exists():
            raise FileNotFoundError(
                f"Image not found: {image_path}"
            )

        self.image = Image.open(
            self.image_path
        )

    def ask(self, question: str) -> str:
        """Answer a basic question about the image."""

        question = question.lower().strip()

        width, height = self.image.size

        if "width" in question:
            return (
                f"The image width is {width} pixels."
            )

        if "height" in question:
            return (
                f"The image height is {height} pixels."
            )

        if (
            "size" in question
            or "dimension" in question
        ):
            return (
                f"The image dimensions are "
                f"{width} × {height} pixels."
            )

        if "format" in question:
            return (
                f"The image format is "
                f"{self.image.format}."
            )

        if (
            "color" in question
            or "colour" in question
        ):
            return (
                f"The image color mode is "
                f"{self.image.mode}."
            )

        return (
            "I can currently answer basic image "
            "properties locally. A local vision model "
            "can be connected here later for deeper "
            "visual understanding."
        )


if __name__ == "__main__":

    print("=" * 60)
    print("OFFLINE GENIUS - OFFLINE VISION")
    print("=" * 60)
    print("Processing: LOCAL")
    print("Cloud upload: DISABLED")
    print("=" * 60)