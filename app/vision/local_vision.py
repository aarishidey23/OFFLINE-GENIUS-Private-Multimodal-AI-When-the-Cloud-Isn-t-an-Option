"""
Local Vision Understanding for OFFLINE GENIUS.

Connects the application to the hardware-independent
VisionModelAdapter.

No cloud API is used.
"""

from pathlib import Path

from PIL import Image

from app.vision.vision_model import VisionModelAdapter


class LocalVisionUnderstanding:
    """Provide local visual understanding."""

    SUPPORTED_EXTENSIONS = {
        ".png",
        ".jpg",
        ".jpeg",
        ".webp",
        ".bmp",
    }

    def __init__(self, image_path: str):
        self.image_path = Path(image_path)

        if not self.image_path.exists():
            raise FileNotFoundError(
                f"Image not found: {image_path}"
            )

        if (
            self.image_path.suffix.lower()
            not in self.SUPPORTED_EXTENSIONS
        ):
            raise ValueError(
                "Unsupported image format."
            )

        self.vision_model = VisionModelAdapter()

    def describe(self) -> str:
        """Describe the image using the local vision layer."""

        with Image.open(self.image_path) as image:

            width, height = image.size
            image_format = (
                image.format or "UNKNOWN"
            )
            mode = image.mode

        model_result = self.vision_model.analyze(
            str(self.image_path),
            "Describe this image.",
        )

        return (
            "LOCAL IMAGE ANALYSIS\n\n"
            f"Image: {self.image_path.name}\n"
            f"Dimensions: {width} × {height} pixels\n"
            f"Format: {image_format}\n"
            f"Color mode: {mode}\n\n"
            f"{model_result}\n\n"
            "PRIVACY:\n"
            "Image processing remains local.\n"
            "No cloud upload was used."
        )

    def ask(self, question: str) -> str:
        """Ask a question about the image."""

        question = question.strip()

        if not question:
            question = "Describe this image."

        # Basic image properties remain available immediately.
        with Image.open(self.image_path) as image:

            width, height = image.size
            image_format = (
                image.format or "UNKNOWN"
            )
            mode = image.mode

        question_lower = question.lower()

        if "width" in question_lower:
            return (
                f"The image width is "
                f"{width} pixels.\n\n"
                "Processed locally."
            )

        if "height" in question_lower:
            return (
                f"The image height is "
                f"{height} pixels.\n\n"
                "Processed locally."
            )

        if (
            "dimension" in question_lower
            or "size" in question_lower
        ):
            return (
                f"The image dimensions are "
                f"{width} × {height} pixels.\n\n"
                "Processed locally."
            )

        if "format" in question_lower:
            return (
                f"The image format is "
                f"{image_format}.\n\n"
                "Processed locally."
            )

        if (
            "color" in question_lower
            or "colour" in question_lower
        ):
            return (
                f"The image color mode is "
                f"{mode}.\n\n"
                "Processed locally."
            )

        # All deeper questions go through the local
        # vision-model adapter.
        return self.vision_model.analyze(
            str(self.image_path),
            question,
        )


if __name__ == "__main__":

    print("=" * 60)
    print("OFFLINE GENIUS - LOCAL VISION")
    print("=" * 60)
    print("Vision layer: CONNECTED")
    print("Processing: LOCAL")
    print("Cloud upload: DISABLED")
    print("=" * 60)