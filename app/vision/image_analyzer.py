"""
Local image analyzer for OFFLINE GENIUS.

Performs basic image inspection locally.
No image is uploaded to the cloud.
"""

from dataclasses import dataclass
from pathlib import Path

from PIL import Image


@dataclass
class ImageAnalysisResult:
    """Result returned by the local image analyzer."""

    filename: str
    width: int
    height: int
    mode: str
    format: str
    size_kb: float
    message: str


class LocalImageAnalyzer:
    """Analyze image files locally."""

    SUPPORTED_EXTENSIONS = {
        ".png",
        ".jpg",
        ".jpeg",
        ".webp",
        ".bmp",
    }

    def analyze(
        self,
        image_path: str,
    ) -> ImageAnalysisResult:
        """Inspect an image locally."""

        path = Path(image_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Image not found: {image_path}"
            )

        if (
            path.suffix.lower()
            not in self.SUPPORTED_EXTENSIONS
        ):
            raise ValueError(
                "Unsupported image format."
            )

        file_size_kb = (
            path.stat().st_size / 1024
        )

        with Image.open(path) as image:

            width, height = image.size
            mode = image.mode
            image_format = (
                image.format or "UNKNOWN"
            )

        message = (
            "Image inspected locally. "
            "No cloud upload was used."
        )

        return ImageAnalysisResult(
            filename=path.name,
            width=width,
            height=height,
            mode=mode,
            format=image_format,
            size_kb=round(
                file_size_kb,
                2,
            ),
            message=message,
        )


if __name__ == "__main__":

    print("=" * 60)
    print("OFFLINE GENIUS - Offline Vision")
    print("=" * 60)
    print("Image processing: LOCAL")
    print("Cloud upload: DISABLED")
    print("=" * 60)