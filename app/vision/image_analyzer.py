"""
Offline image and diagram analysis for OFFLINE GENIUS.

This module prepares local images for analysis without
uploading them to a cloud service.
"""

from dataclasses import dataclass
from pathlib import Path

from PIL import Image


@dataclass
class ImageInfo:
    """Information about a locally loaded image."""

    filename: str
    width: int
    height: int
    mode: str
    format: str


class ImageAnalyzer:
    """Local image analysis interface."""

    SUPPORTED_FORMATS = {
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
        ".bmp",
    }

    def analyze(self, image_path: str) -> ImageInfo:
        """
        Read basic information from a local image.

        No image is uploaded to the cloud.
        """

        path = Path(image_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Image not found: {image_path}"
            )

        if path.suffix.lower() not in self.SUPPORTED_FORMATS:
            raise ValueError(
                "Unsupported image format."
            )

        with Image.open(path) as image:
            return ImageInfo(
                filename=path.name,
                width=image.width,
                height=image.height,
                mode=image.mode,
                format=image.format or "UNKNOWN",
            )

    def describe(self, image_path: str) -> str:
        """
        Return a prototype description of the image.

        A real local vision-language model can be connected
        here later for diagram and image understanding.
        """

        info = self.analyze(image_path)

        return (
            f"Local image loaded successfully: {info.filename}. "
            f"Size: {info.width}x{info.height}. "
            "The production version will use a local vision "
            "model to understand diagrams, screenshots, "
            "documents, and other visual content."
        )


if __name__ == "__main__":
    analyzer = ImageAnalyzer()

    print("OFFLINE GENIUS - Offline Vision")
    print("Image processing: LOCAL")
    print("Cloud upload: DISABLED")
