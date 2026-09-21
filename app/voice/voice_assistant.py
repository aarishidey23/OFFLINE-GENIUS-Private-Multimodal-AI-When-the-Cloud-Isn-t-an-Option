"""
Voice assistant workflow for OFFLINE GENIUS.

Connects local speech recognition with the local
AI inference engine.
"""

from dataclasses import dataclass

from ..inference.local_engine import LocalEngine
from .voice_engine import VoiceEngine


@dataclass
class VoiceAssistantResult:
    """Result from the voice assistant workflow."""

    spoken_text: str
    response: str
    model: str
    device: str


class VoiceAssistant:
    """Connect speech input to the local AI engine."""

    def __init__(self):
        self.voice_engine = VoiceEngine()
        self.ai_engine = LocalEngine()

    def process_audio(
        self,
        audio_path: str,
    ) -> VoiceAssistantResult:
        """
        Process an audio file locally.

        Speech recognition and AI processing remain
        inside the local application.
        """

        voice_result = self.voice_engine.transcribe(
            audio_path
        )

        ai_result = self.ai_engine.generate(
            voice_result.text
        )

        return VoiceAssistantResult(
            spoken_text=voice_result.text,
            response=ai_result.response,
            model=ai_result.model,
            device=ai_result.device,
        )


if __name__ == "__main__":
    assistant = VoiceAssistant()

    print("OFFLINE GENIUS - Voice Assistant")
    print("Speech processing: LOCAL")
    print("AI processing: LOCAL")
    print("Cloud upload: DISABLED")
