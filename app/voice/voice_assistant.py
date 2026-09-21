"""
Offline Voice Assistant for OFFLINE GENIUS.

Uses Windows built-in speech services.
No cloud API is required.
"""

import subprocess


class OfflineVoiceAssistant:
    """Simple offline voice output using Windows SAPI."""

    def __init__(self):
        self.available = True

    def speak(self, text: str) -> bool:
        """Read text aloud using Windows built-in speech."""

        text = str(text).strip()

        if not text:
            return False

        # Keep the PowerShell command safe for normal AI responses.
        safe_text = text.replace("'", "''")

        script = (
            "$voice = New-Object -ComObject SAPI.SpVoice; "
            f"$voice.Speak('{safe_text}')"
        )

        try:
            subprocess.Popen(
                [
                    "powershell",
                    "-NoProfile",
                    "-Command",
                    script,
                ],
                creationflags=subprocess.CREATE_NO_WINDOW,
            )

            return True

        except Exception:
            return False

    def stop(self):
        """Placeholder for future voice-stop support."""
        return None

    def status(self) -> str:
        """Return the current voice system status."""
        return "WINDOWS OFFLINE SPEECH"