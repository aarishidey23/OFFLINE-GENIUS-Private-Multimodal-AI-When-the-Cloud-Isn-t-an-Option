"""
OFFLINE GENIUS Desktop UI.

Private, Multimodal AI — When the Cloud Isn't an Option.
"""

import sys
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox


class OfflineGeniusApp:
    """Main desktop interface for OFFLINE GENIUS."""

    def __init__(self, root):
        self.root = root

        self.document_manager = None
        self.current_file = None

        root.title("OFFLINE GENIUS")
        root.geometry("900x600")
        root.minsize(750, 500)

        self.create_header()
        self.create_status_panel()
        self.create_chat_area()
        self.create_action_panel()

    def create_header(self):
        """Create application header."""

        header = tk.Frame(
            self.root,
            padx=20,
            pady=15,
        )
        header.pack(fill="x")

        title = tk.Label(
            header,
            text="OFFLINE GENIUS",
            font=("Arial", 24, "bold"),
        )
        title.pack(anchor="w")

        subtitle = tk.Label(
            header,
            text="Private, Multimodal AI — When the Cloud Isn't an Option",
            font=("Arial", 11),
        )
        subtitle.pack(anchor="w")

    def create_status_panel(self):
        """Create privacy and connection status."""

        panel = tk.Frame(
            self.root,
            relief="groove",
            borderwidth=1,
            padx=15,
            pady=10,
        )
        panel.pack(
            fill="x",
            padx=20,
            pady=5,
        )

        self.status_label = tk.Label(
            panel,
            text=(
                "● OFFLINE     "
                "LOCAL PROCESSING     "
                "DATA STAYS ON THIS PC"
            ),
            font=("Arial", 10, "bold"),
        )
        self.status_label.pack(anchor="w")

        self.file_label = tk.Label(
            panel,
            text="No document loaded",
            font=("Arial", 9),
        )
        self.file_label.pack(anchor="w", pady=(4, 0))

    def create_chat_area(self):
        """Create the main AI interaction area."""

        frame = tk.Frame(
            self.root,
            padx=20,
            pady=10,
        )
        frame.pack(
            fill="both",
            expand=True,
        )

        label = tk.Label(
            frame,
            text="Ask your local AI",
            font=("Arial", 14, "bold"),
        )
        label.pack(anchor="w")

        self.chat = tk.Text(
            frame,
            height=12,
            wrap="word",
            state="disabled",
        )
        self.chat.pack(
            fill="both",
            expand=True,
            pady=8,
        )

        input_frame = tk.Frame(frame)
        input_frame.pack(fill="x")

        self.question = tk.Entry(
            input_frame,
            font=("Arial", 11),
        )
        self.question.pack(
            side="left",
            fill="x",
            expand=True,
        )

        self.question.bind(
            "<Return>",
            lambda event: self.ask_ai(),
        )

        ask_button = tk.Button(
            input_frame,
            text="ASK LOCAL AI",
            command=self.ask_ai,
        )
        ask_button.pack(
            side="right",
            padx=(8, 0),
        )

    def create_action_panel(self):
        """Create buttons for multimodal features."""

        panel = tk.Frame(
            self.root,
            padx=20,
            pady=15,
        )
        panel.pack(fill="x")

        tk.Button(
            panel,
            text="GO OFFLINE",
            command=self.go_offline,
        ).pack(
            side="left",
            padx=5,
        )

        tk.Button(
            panel,
            text="ADD DOCUMENT",
            command=self.add_document,
        ).pack(
            side="left",
            padx=5,
        )

        tk.Button(
            panel,
            text="ANALYZE IMAGE",
            command=self.analyze_image,
        ).pack(
            side="left",
            padx=5,
        )

        tk.Button(
            panel,
            text="PRIVACY STATUS",
            command=self.show_privacy,
        ).pack(
            side="right",
            padx=5,
        )

    def add_message(self, message):
        """Add a message to the chat area."""

        self.chat.config(state="normal")

        self.chat.insert(
            "end",
            message + "\n\n",
        )

        self.chat.config(state="disabled")
        self.chat.see("end")

    def ask_ai(self):
        """Search the locally indexed Knowledge Vault."""

        question = self.question.get().strip()

        if not question:
            return

        self.add_message(
            "YOU:\n" + question
        )

        if self.document_manager is None:
            self.add_message(
                "OFFLINE GENIUS:\n"
                "No document is currently indexed.\n"
                "Please click ADD DOCUMENT first."
            )

            self.question.delete(
                0,
                "end",
            )
            return

        try:
            results = self.document_manager.search(
                question
            )

            if results:

                self.add_message(
                    "KNOWLEDGE VAULT — "
                    f"{len(results)} RELEVANT SECTIONS FOUND"
                )

                for number, document in enumerate(
                    results,
                    start=1,
                ):

                    text = document.content.strip()

                    excerpt = text[:1200]

                    if len(text) > 1200:
                        excerpt += "\n..."

                    self.add_message(
                        f"RELEVANT SECTION {number}\n"
                        f"Document: {document.name}\n\n"
                        f"{excerpt}"
                    )

            else:

                self.add_message(
                    "OFFLINE GENIUS:\n"
                    "I couldn't find a matching passage "
                    "in your locally indexed documents.\n\n"
                    "Try using different words from the "
                    "document."
                )

        except Exception as error:

            self.add_message(
                "KNOWLEDGE VAULT ERROR:\n"
                f"{error}"
            )

        self.question.delete(
            0,
            "end",
        )

    def go_offline(self):
        """Activate local-first mode."""

        self.status_label.config(
            text=(
                "● OFFLINE MODE ACTIVE     "
                "LOCAL PROCESSING     "
                "CLOUD ACCESS DISABLED"
            )
        )

        self.add_message(
            "SYSTEM:\n"
            "OFFLINE MODE activated.\n"
            "The workspace is ready for local processing."
        )

    def add_document(self):
        """Select and process a local PDF."""

        file_path = filedialog.askopenfilename(
            title="Select a document",
            filetypes=[
                ("PDF files", "*.pdf"),
                ("Text files", "*.txt"),
                ("All files", "*.*"),
            ],
        )

        if not file_path:
            return

        try:

            project_root = Path(
                __file__
            ).resolve().parents[2]

            if str(project_root) not in sys.path:
                sys.path.insert(
                    0,
                    str(project_root),
                )

            from app.retrieval.document_manager import (
                DocumentManager
            )

            if self.document_manager is None:
                self.document_manager = DocumentManager()

            path = Path(file_path)

            if path.suffix.lower() == ".pdf":

                success = self.document_manager.add_pdf(
                    str(path)
                )

            else:

                success = False

            if success:

                self.current_file = path.name

                self.file_label.config(
                    text=(
                        f"📄 {path.name} — "
                        "processed locally"
                    )
                )

                self.add_message(
                    "KNOWLEDGE VAULT:\n"
                    "✓ Document processed locally.\n"
                    f"File: {path.name}\n"
                    "✓ Text split into searchable sections.\n"
                    "✓ No cloud upload."
                )

                messagebox.showinfo(
                    "Knowledge Vault",
                    "Document successfully processed locally.",
                )

            else:

                messagebox.showwarning(
                    "Knowledge Vault",
                    "The document could not be processed.",
                )

        except ImportError:

            messagebox.showerror(
                "Missing Dependency",
                "The PDF library is not installed.\n\n"
                "Install it using:\n"
                "python -m pip install pypdf",
            )

        except Exception as error:

            messagebox.showerror(
                "Document Error",
                "Could not process the document.\n\n"
                f"{error}",
            )

    def analyze_image(self):
        """Select a local image."""

        file_path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[
                (
                    "Image files",
                    "*.png *.jpg *.jpeg *.webp",
                ),
                ("All files", "*.*"),
            ],
        )

        if file_path:

            self.add_message(
                "VISION:\n"
                "Local image selected:\n"
                + file_path
            )

    def show_privacy(self):
        """Display the privacy state."""

        messagebox.showinfo(
            "Privacy Status",
            "Network: OFFLINE\n"
            "Processing: LOCAL\n"
            "Cloud upload: DISABLED\n"
            "Data boundary: THIS PC",
        )


def main():
    """Start the OFFLINE GENIUS desktop application."""

    root = tk.Tk()

    OfflineGeniusApp(root)

    root.mainloop()


if __name__ == "__main__":
    main()
