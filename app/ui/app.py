"""
OFFLINE GENIUS Desktop UI.

A lightweight prototype interface for the
private, local-first AI workspace.
"""

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox


class OfflineGeniusApp:
    """Main desktop interface for OFFLINE GENIUS."""

    def __init__(self, root):
        self.root = root

        root.title("OFFLINE GENIUS")
        root.geometry("900x600")
        root.minsize(750, 500)

        self.create_header()
        self.create_status_panel()
        self.create_chat_area()
        self.create_action_panel()

    def create_header(self):
        """Create application header."""

        header = tk.Frame(self.root, padx=20, pady=15)
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
        panel.pack(fill="x", padx=20, pady=5)

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

    def create_chat_area(self):
        """Create the main AI interaction area."""

        frame = tk.Frame(self.root, padx=20, pady=10)
        frame.pack(fill="both", expand=True)

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
        self.chat.pack(fill="both", expand=True, pady=8)

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

        ask_button = tk.Button(
            input_frame,
            text="ASK LOCAL AI",
            command=self.ask_ai,
        )
        ask_button.pack(side="right", padx=(8, 0))

    def create_action_panel(self):
        """Create buttons for multimodal features."""

        panel = tk.Frame(self.root, padx=20, pady=15)
        panel.pack(fill="x")

        tk.Button(
            panel,
            text="GO OFFLINE",
            command=self.go_offline,
        ).pack(side="left", padx=5)

        tk.Button(
            panel,
            text="ADD DOCUMENT",
            command=self.add_document,
        ).pack(side="left", padx=5)

        tk.Button(
            panel,
            text="ANALYZE IMAGE",
            command=self.analyze_image,
        ).pack(side="left", padx=5)

        tk.Button(
            panel,
            text="PRIVACY STATUS",
            command=self.show_privacy,
        ).pack(side="right", padx=5)

    def add_message(self, message):
        """Add a message to the chat area."""

        self.chat.config(state="normal")
        self.chat.insert("end", message + "\n\n")
        self.chat.config(state="disabled")
        self.chat.see("end")

    def ask_ai(self):
        """Handle a local AI question."""

        question = self.question.get().strip()

        if not question:
            return

        self.add_message("You: " + question)

        response = (
            "OFFLINE GENIUS: Your request is being "
            "processed locally. No cloud upload is used "
            "in this prototype."
        )

        self.add_message(response)
        self.question.delete(0, "end")

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
            "SYSTEM: OFFLINE MODE activated. "
            "The workspace is ready for local processing."
        )

    def add_document(self):
        """Select and process a local document."""

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
            import sys

            project_root = Path(__file__).resolve().parents[2]

            if str(project_root) not in sys.path:
                sys.path.insert(0, str(project_root))

            from app.retrieval.document_manager import DocumentManager

            manager = DocumentManager()

            if Path(file_path).suffix.lower() == ".pdf":
                success = manager.add_pdf(file_path)
            else:
                success = False

            if success:
                self.add_message(
                    "KNOWLEDGE VAULT: Document processed locally.\n"
                    f"File: {Path(file_path).name}\n"
                    f"Indexed documents: {manager.count()}"
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
                "pypdf is not installed yet.",
            )

        except Exception as error:
            messagebox.showerror(
                "Document Error",
                f"Could not process the document.\n\n{error}",
            )

    def analyze_image(self):
        """Select a local image."""

        file_path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.webp"),
                ("All files", "*.*"),
            ],
        )

        if file_path:
            self.add_message(
                "VISION: Local image selected:\n"
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
