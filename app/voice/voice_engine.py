"""
Offline voice interface for OFFLINE GENIUS.

Provides a local-first interface for speech recognition
and voice interaction.
"""

from dataclasses import dataclass


@dataclass
class VoiceResult:
    """Result returned by the local voice engine."""

    text: str
    model: str = "local-speech-demo"
    device: str = "CPU"


class VoiceEngine:
    """Local-first speech recognition interface."""

    def __init__(
        self,
        model_name: str = "local-speech-demo",
    ):
        self.model_name = model_name
        self.device = "CPU"

    def status(self) -> dict:
        """Return the current voice system status."""

        return {
            "model": self.model_name,
            "device": self.device,
            "network_required": False,
            "audio_sent_to_cloud": False,
        }

    def transcribe(
        self,
        audio_path: str,
    ) -> VoiceResult:
        """
        Convert a local audio file into text.

        This is currently a prototype interface.
        A local speech-recognition model can be connected
        here later.
        """

        if not audio_path.strip():
            return VoiceResult(
                text="No audio file was provided.",
                model=self.model_name,
                device=self.device,
            )

        return VoiceResult(
            text=(
                "OFFLINE GENIUS received the audio locally. "
                "The production version will transcribe "
                "speech using a local speech model without "
                "sending the recording to the cloud."
            ),
            model=self.model_name,
            device=self.device,
        )


if __name__ == "__main__":
    engine = VoiceEngine()

    print("OFFLINE GENIUS - Offline Voice")
    print(engine.status())
