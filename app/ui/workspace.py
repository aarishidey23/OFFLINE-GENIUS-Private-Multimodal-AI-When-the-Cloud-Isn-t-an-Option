"""
OFFLINE GENIUS Workspace.

Central interface that connects the project's
local AI capabilities.
"""

from dataclasses import dataclass

from ..inference.local_engine import LocalEngine
from ..retrieval.document_manager import DocumentManager
from ..vision.vision_engine import VisionEngine
from ..voice.voice_assistant import VoiceAssistant


@dataclass
class WorkspaceStatus:
    """Current status of the OFFLINE GENIUS workspace."""

    network: str
    processing: str
    privacy: str


class OfflineGeniusWorkspace:
    """Central controller for the local AI workspace."""

    def __init__(self):
        self.ai = LocalEngine()
        self.documents = DocumentManager()
        self.vision = VisionEngine()
        self.voice = VoiceAssistant()

    def status(self) -> WorkspaceStatus:
        """Return the privacy-first workspace status."""

        return WorkspaceStatus(
            network="OFFLINE / LOCAL-FIRST",
            processing="LOCAL DEVICE",
            privacy="DATA STAYS ON THIS PC",
        )

    def ask(self, question: str) -> str:
        """Ask the local AI engine a question."""

        result = self.ai.generate(question)
        return result.response

    def indexed_documents(self) -> int:
        """Return the number of documents in the local vault."""

        return self.documents.count()


if __name__ == "__main__":
    workspace = OfflineGeniusWorkspace()

    status = workspace.status()

    print("=" * 60)
    print("OFFLINE GENIUS WORKSPACE")
    print("=" * 60)
    print("Network:", status.network)
    print("Processing:", status.processing)
    print("Privacy:", status.privacy)
    print("Indexed documents:", workspace.indexed_documents())
    print("=" * 60)

    print("\nTest question:")
    print(workspace.ask("What can you do offline?"))
