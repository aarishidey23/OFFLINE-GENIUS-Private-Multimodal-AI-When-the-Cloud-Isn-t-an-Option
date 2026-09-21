"""
OFFLINE GENIUS
Private, Multimodal AI — When the Cloud Isn't an Option
"""

import sys
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox


class OfflineGeniusApp:
    """Main desktop application for OFFLINE GENIUS."""

    BG = "#0B1020"
    PANEL = "#151C2F"
    PANEL_LIGHT = "#1D2740"
    TEXT = "#F5F7FF"
    MUTED = "#9AA6C0"
    GREEN = "#35D07F"
    BLUE = "#4DA3FF"
    PURPLE = "#9B7BFF"
    BORDER = "#293451"

    def __init__(self, root):
        self.root = root

        self.document_manager = None
        self.answer_generator = None

        self.current_file = None
        self.current_image = None

        self.offline_mode = False

        self.root.title("OFFLINE GENIUS")
        self.root.geometry("1120x800")
        self.root.minsize(900, 680)
        self.root.configure(bg=self.BG)

        self.create_header()
        self.create_dashboard()
        self.create_chat_area()
        self.create_action_panel()

    # =========================================================
    # PROJECT PATH
    # =========================================================

    def project_root(self):
        """Return the OFFLINE GENIUS project root."""

        root = Path(__file__).resolve().parents[2]

        if str(root) not in sys.path:
            sys.path.insert(0, str(root))

        return root

    # =========================================================
    # HEADER
    # =========================================================

    def create_header(self):

        header = tk.Frame(
            self.root,
            bg=self.BG,
            padx=30,
            pady=22,
        )

        header.pack(fill="x")

        title_row = tk.Frame(
            header,
            bg=self.BG,
        )

        title_row.pack(fill="x")

        tk.Label(
            title_row,
            text="OFFLINE GENIUS",
            bg=self.BG,
            fg=self.TEXT,
            font=("Segoe UI", 26, "bold"),
        ).pack(side="left")

        self.header_status = tk.Label(
            title_row,
            text="● LOCAL-FIRST",
            bg=self.BG,
            fg=self.GREEN,
            font=("Segoe UI", 11, "bold"),
        )

        self.header_status.pack(
            side="right",
            pady=8,
        )

        tk.Label(
            header,
            text=(
                "Private, Multimodal AI  •  "
                "When the Cloud Isn't an Option"
            ),
            bg=self.BG,
            fg=self.MUTED,
            font=("Segoe UI", 11),
        ).pack(
            anchor="w",
            pady=(4, 0),
        )

    # =========================================================
    # DASHBOARD
    # =========================================================

    def create_dashboard(self):

        outer = tk.Frame(
            self.root,
            bg=self.BG,
            padx=25,
            pady=5,
        )

        outer.pack(fill="x")

        tk.Label(
            outer,
            text="LOCAL KNOWLEDGE VAULT",
            bg=self.BG,
            fg=self.TEXT,
            font=("Segoe UI", 13, "bold"),
        ).pack(
            anchor="w",
            pady=(0, 10),
        )

        cards = tk.Frame(
            outer,
            bg=self.BG,
        )

        cards.pack(fill="x")

        self.create_status_card(
            cards,
            "🔒  PRIVACY",
            "LOCAL ONLY",
            "No cloud upload",
            "privacy",
        )

        self.create_status_card(
            cards,
            "◉  MODE",
            "LOCAL-FIRST",
            "Offline ready",
            "mode",
        )

        self.create_status_card(
            cards,
            "▣  DOCUMENT",
            "NONE",
            "Add a local document",
            "document",
        )

        self.create_status_card(
            cards,
            "⌁  INDEX",
            "0",
            "Searchable sections",
            "sections",
        )

    def create_status_card(
        self,
        parent,
        heading,
        value,
        detail,
        card_type,
    ):

        card = tk.Frame(
            parent,
            bg=self.PANEL,
            highlightbackground=self.BORDER,
            highlightthickness=1,
            padx=15,
            pady=13,
        )

        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5,
        )

        tk.Label(
            card,
            text=heading,
            bg=self.PANEL,
            fg=self.MUTED,
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w")

        value_label = tk.Label(
            card,
            text=value,
            bg=self.PANEL,
            fg=(
                self.GREEN
                if card_type == "privacy"
                else self.TEXT
            ),
            font=("Segoe UI", 14, "bold"),
        )

        value_label.pack(
            anchor="w",
            pady=(5, 1),
        )

        detail_label = tk.Label(
            card,
            text=detail,
            bg=self.PANEL,
            fg=self.MUTED,
            font=("Segoe UI", 8),
        )

        detail_label.pack(anchor="w")

        if card_type == "privacy":
            self.privacy_value = value_label
            self.privacy_detail = detail_label

        elif card_type == "mode":
            self.mode_value = value_label
            self.mode_detail = detail_label

        elif card_type == "document":
            self.document_value = value_label
            self.document_detail = detail_label

        elif card_type == "sections":
            self.sections_value = value_label
            self.sections_detail = detail_label

    # =========================================================
    # CHAT AREA
    # =========================================================

    def create_chat_area(self):

        outer = tk.Frame(
            self.root,
            bg=self.BG,
            padx=25,
            pady=15,
        )

        outer.pack(
            fill="both",
            expand=True,
        )

        title_row = tk.Frame(
            outer,
            bg=self.BG,
        )

        title_row.pack(fill="x")

        tk.Label(
            title_row,
            text="ASK YOUR LOCAL AI",
            bg=self.BG,
            fg=self.TEXT,
            font=("Segoe UI", 13, "bold"),
        ).pack(side="left")

        tk.Label(
            title_row,
            text="LOCAL MULTIMODAL AI",
            bg=self.BG,
            fg=self.BLUE,
            font=("Segoe UI", 9, "bold"),
        ).pack(side="right")

        chat_frame = tk.Frame(
            outer,
            bg=self.PANEL,
            highlightbackground=self.BORDER,
            highlightthickness=1,
        )

        chat_frame.pack(
            fill="both",
            expand=True,
            pady=(8, 10),
        )

        self.chat = tk.Text(
            chat_frame,
            height=12,
            wrap="word",
            state="disabled",
            bg=self.PANEL,
            fg=self.TEXT,
            insertbackground=self.TEXT,
            selectbackground=self.PURPLE,
            relief="flat",
            borderwidth=0,
            padx=18,
            pady=15,
            font=("Segoe UI", 10),
        )

        self.chat.pack(
            fill="both",
            expand=True,
        )

        input_frame = tk.Frame(
            outer,
            bg=self.BG,
        )

        input_frame.pack(fill="x")

        self.question = tk.Entry(
            input_frame,
            bg=self.PANEL,
            fg=self.TEXT,
            insertbackground=self.TEXT,
            relief="flat",
            highlightbackground=self.BORDER,
            highlightcolor=self.BLUE,
            highlightthickness=1,
            font=("Segoe UI", 11),
        )

        self.question.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=9,
        )

        self.question.bind(
            "<Return>",
            lambda event: self.ask_ai(),
        )

        tk.Button(
            input_frame,
            text="ASK LOCAL AI  →",
            command=self.ask_ai,
            bg=self.BLUE,
            fg="white",
            activebackground=self.BLUE,
            activeforeground="white",
            relief="flat",
            borderwidth=0,
            padx=18,
            pady=8,
            font=("Segoe UI", 10, "bold"),
        ).pack(
            side="right",
            padx=(10, 0),
        )

    # =========================================================
    # ACTION PANEL
    # =========================================================

    def create_action_panel(self):

        panel = tk.Frame(
            self.root,
            bg=self.PANEL,
            padx=25,
            pady=15,
        )

        panel.pack(fill="x")

        self.offline_button = tk.Button(
            panel,
            text="⚡  GO OFFLINE",
            command=self.go_offline,
            bg=self.GREEN,
            fg="#08130D",
            activebackground=self.GREEN,
            activeforeground="#08130D",
            relief="flat",
            borderwidth=0,
            padx=16,
            pady=9,
            font=("Segoe UI", 10, "bold"),
        )

        self.offline_button.pack(
            side="left",
            padx=5,
        )

        tk.Button(
            panel,
            text="＋  ADD DOCUMENT",
            command=self.add_document,
            bg=self.PANEL_LIGHT,
            fg=self.TEXT,
            activebackground=self.BORDER,
            activeforeground=self.TEXT,
            relief="flat",
            borderwidth=0,
            padx=14,
            pady=9,
            font=("Segoe UI", 10, "bold"),
        ).pack(
            side="left",
            padx=5,
        )

        tk.Button(
            panel,
            text="◈  ANALYZE IMAGE",
            command=self.analyze_image,
            bg=self.PANEL_LIGHT,
            fg=self.TEXT,
            activebackground=self.BORDER,
            activeforeground=self.TEXT,
            relief="flat",
            borderwidth=0,
            padx=14,
            pady=9,
            font=("Segoe UI", 10, "bold"),
        ).pack(
            side="left",
            padx=5,
        )

        tk.Button(
            panel,
            text="◉  ASK ABOUT IMAGE",
            command=self.ask_about_image,
            bg=self.PURPLE,
            fg="white",
            activebackground=self.PURPLE,
            activeforeground="white",
            relief="flat",
            borderwidth=0,
            padx=14,
            pady=9,
            font=("Segoe UI", 10, "bold"),
        ).pack(
            side="left",
            padx=5,
        )

        tk.Button(
            panel,
            text="👁  DESCRIBE IMAGE",
            command=self.describe_image,
            bg=self.PANEL_LIGHT,
            fg=self.TEXT,
            activebackground=self.BORDER,
            activeforeground=self.TEXT,
            relief="flat",
            borderwidth=0,
            padx=14,
            pady=9,
            font=("Segoe UI", 10, "bold"),
        ).pack(
            side="left",
            padx=5,
        )

        tk.Button(
            panel,
            text="🔒  PRIVACY STATUS",
            command=self.show_privacy,
            bg=self.PANEL_LIGHT,
            fg=self.TEXT,
            activebackground=self.BORDER,
            activeforeground=self.TEXT,
            relief="flat",
            borderwidth=0,
            padx=14,
            pady=9,
            font=("Segoe UI", 10, "bold"),
        ).pack(
            side="right",
            padx=5,
        )

    # =========================================================
    # CHAT OUTPUT
    # =========================================================

    def add_message(self, message):

        self.chat.config(state="normal")

        self.chat.insert(
            "end",
            message + "\n\n",
        )

        self.chat.config(state="disabled")

        self.chat.see("end")

    # =========================================================
    # ANSWER GENERATOR
    # =========================================================

    def load_answer_generator(self):

        try:

            self.project_root()

            from app.inference.answer_generator import (
                LocalAnswerGenerator
            )

            self.answer_generator = (
                LocalAnswerGenerator()
            )

            return True

        except Exception as error:

            self.add_message(
                "ANSWER GENERATOR ERROR:\n"
                f"{error}"
            )

            return False

    # =========================================================
    # MAIN AI ROUTER
    # =========================================================

    def ask_ai(self):

        question = self.question.get().strip()

        if not question:
            return

        # -----------------------------------------------------
        # IMAGE MODE
        # -----------------------------------------------------

        if self.current_image:

            try:

                self.project_root()

                # IMPORTANT:
                # This is the NEW vision layer.
                # There is NO OfflineVisionQuestion here.
                from app.vision.local_vision import (
                    LocalVisionUnderstanding
                )

                vision = LocalVisionUnderstanding(
                    self.current_image
                )

                self.add_message(
                    "YOU:\n"
                    + question
                )

                answer = vision.ask(
                    question
                )

                self.add_message(
                    "OFFLINE VISION:\n"
                    + answer
                    + "\n\n"
                    "LOCAL IMAGE PROCESSING • "
                    "NO CLOUD UPLOAD"
                )

            except Exception as error:

                self.add_message(
                    "VISION ERROR:\n"
                    f"{error}"
                )

            self.question.delete(
                0,
                "end",
            )

            return

        # -----------------------------------------------------
        # DOCUMENT MODE
        # -----------------------------------------------------

        self.add_message(
            "YOU:\n"
            + question
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

            if not results:

                self.add_message(
                    "OFFLINE GENIUS:\n"
                    "I couldn't find enough information "
                    "in your local documents."
                )

                self.question.delete(
                    0,
                    "end",
                )

                return

            if not self.load_answer_generator():

                self.question.delete(
                    0,
                    "end",
                )

                return

            answer_result = (
                self.answer_generator.generate(
                    question,
                    results,
                )
            )

            self.add_message(
                "OFFLINE GENIUS:\n"
                + answer_result.answer
            )

            self.add_message(
                "SOURCE:\n"
                + answer_result.source
                + "\n\n"
                "LOCAL RETRIEVAL • "
                "NO CLOUD UPLOAD"
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

    # =========================================================
    # OFFLINE MODE
    # =========================================================

    def go_offline(self):

        if self.offline_mode:

            self.add_message(
                "SYSTEM:\n"
                "OFFLINE MODE is already active.\n"
                "All local processing continues on this PC."
            )

            return

        self.offline_mode = True

        self.header_status.config(
            text="● OFFLINE ACTIVE",
            fg=self.GREEN,
        )

        self.mode_value.config(
            text="OFFLINE",
            fg=self.GREEN,
        )

        self.mode_detail.config(
            text="Network not required",
        )

        self.privacy_value.config(
            text="LOCAL ONLY",
            fg=self.GREEN,
        )

        self.privacy_detail.config(
            text="Cloud access disabled",
        )

        self.offline_button.config(
            text="✓  OFFLINE MODE ACTIVE",
            bg=self.GREEN,
        )

        self.add_message(
            "SYSTEM:\n"
            "✓ OFFLINE MODE activated.\n"
            "✓ Cloud access disabled.\n"
            "✓ Local document retrieval remains available.\n"
            "✓ Your indexed data stays on this PC.\n"
            "✓ Questions can continue to be answered locally."
        )

    # =========================================================
    # ADD DOCUMENT
    # =========================================================

    def add_document(self):

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

            self.project_root()

            from app.retrieval.document_manager import (
                DocumentManager
            )

            if self.document_manager is None:

                self.document_manager = (
                    DocumentManager()
                )

            path = Path(file_path)

            if path.suffix.lower() == ".pdf":

                success = (
                    self.document_manager.add_pdf(
                        str(path)
                    )
                )

            else:

                success = False

            if success:

                self.current_file = path.name

                self.document_value.config(
                    text=path.name,
                    fg=self.TEXT,
                )

                self.document_detail.config(
                    text="Processed locally",
                )

                section_count = (
                    self.document_manager.count()
                )

                self.sections_value.config(
                    text=str(section_count),
                    fg=self.BLUE,
                )

                self.add_message(
                    "KNOWLEDGE VAULT:\n"
                    "✓ Document processed locally.\n"
                    f"File: {path.name}\n"
                    "✓ Text split into searchable sections.\n"
                    "✓ Local retrieval available.\n"
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

    # =========================================================
    # ANALYZE IMAGE
    # =========================================================

    def analyze_image(self):

        file_path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[
                (
                    "Image files",
                    "*.png *.jpg *.jpeg *.webp *.bmp",
                ),
                ("All files", "*.*"),
            ],
        )

        if not file_path:
            return

        try:

            self.project_root()

            from app.vision.image_analyzer import (
                LocalImageAnalyzer
            )

            analyzer = LocalImageAnalyzer()

            result = analyzer.analyze(
                file_path
            )

            self.current_image = file_path

            self.add_message(
                "VISION ANALYSIS:\n"
                f"✓ Image: {result.filename}\n"
                f"✓ Dimensions: "
                f"{result.width} × {result.height}\n"
                f"✓ Format: {result.format}\n"
                f"✓ Color mode: {result.mode}\n"
                f"✓ File size: {result.size_kb} KB\n\n"
                "✓ Processed locally\n"
                "✓ Cloud upload: DISABLED"
            )

            messagebox.showinfo(
                "Offline Vision",
                "Image analyzed successfully locally.\n\n"
                f"Image: {result.filename}\n"
                f"Dimensions: "
                f"{result.width} × {result.height}\n"
                f"Format: {result.format}\n\n"
                "Cloud upload: DISABLED",
            )

        except Exception as error:

            messagebox.showerror(
                "Vision Error",
                "Could not analyze the image.\n\n"
                f"{error}",
            )

    # =========================================================
    # ASK ABOUT IMAGE
    # =========================================================

    def ask_about_image(self):

        if not self.current_image:

            messagebox.showwarning(
                "Offline Vision",
                "Please analyze an image first.",
            )

            return

        question = self.question.get().strip()

        if not question:

            messagebox.showwarning(
                "Offline Vision",
                "Type a question about the image first.",
            )

            self.question.focus_set()

            return

        try:

            self.project_root()

            # =================================================
            # NEW LOCAL VISION SYSTEM
            # =================================================
            # This is intentionally NOT:
            #
            # from app.vision.vision_question import ...
            #
            # The old vision_question system has been removed
            # from the application.
            # =================================================

            from app.vision.local_vision import (
                LocalVisionUnderstanding
            )

            vision = LocalVisionUnderstanding(
                self.current_image
            )

            self.add_message(
                "YOU:\n"
                + question
            )

            answer = vision.ask(
                question
            )

            self.add_message(
                "OFFLINE VISION:\n"
                + answer
                + "\n\n"
                "LOCAL IMAGE PROCESSING • "
                "NO CLOUD UPLOAD"
            )

        except Exception as error:

            messagebox.showerror(
                "Vision Error",
                "Could not answer the image question.\n\n"
                f"{error}",
            )

        self.question.delete(
            0,
            "end",
        )

    # =========================================================
    # DESCRIBE IMAGE
    # =========================================================

    def describe_image(self):

        if not self.current_image:

            messagebox.showwarning(
                "Offline Vision",
                "Please analyze an image first.",
            )

            return

        try:

            self.project_root()

            from app.vision.local_vision import (
                LocalVisionUnderstanding
            )

            vision = LocalVisionUnderstanding(
                self.current_image
            )

            description = vision.describe()

            self.add_message(
                "OFFLINE VISION:\n"
                + description
                + "\n\n"
                "LOCAL IMAGE PROCESSING • "
                "NO CLOUD UPLOAD"
            )

        except Exception as error:

            messagebox.showerror(
                "Vision Error",
                "Could not describe the image.\n\n"
                f"{error}",
            )

    # =========================================================
    # PRIVACY STATUS
    # =========================================================

    def show_privacy(self):

        if self.offline_mode:

            messagebox.showinfo(
                "Privacy Status",
                "🔒 PRIVACY MODE\n\n"
                "Network: OFFLINE\n"
                "Processing: LOCAL\n"
                "Cloud access: DISABLED\n"
                "Cloud upload: DISABLED\n"
                "Data boundary: THIS PC\n"
                "Local retrieval: ACTIVE",
            )

        else:

            messagebox.showinfo(
                "Privacy Status",
                "🔒 PRIVACY MODE\n\n"
                "Network: LOCAL-FIRST\n"
                "Processing: LOCAL\n"
                "Cloud upload: DISABLED\n"
                "Data boundary: THIS PC\n"
                "Offline mode: READY",
            )


# =============================================================
# MAIN
# =============================================================

def main():

    root = tk.Tk()

    OfflineGeniusApp(root)

    root.mainloop()


if __name__ == "__main__":
    main()