"""
OFFLINE GENIUS
Private, Multimodal AI Workstation
AI for Everyone — Online when needed, Offline when privacy matters.
"""

import sys
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox


class OfflineGeniusApp:
    """Main desktop application for OFFLINE GENIUS."""

    # =========================================================
    # THEME
    # =========================================================

    BG = "#07111D"
    BG_ALT = "#0B1729"
    PANEL = "#101B2D"
    PANEL_LIGHT = "#152744"
    PANEL_SOFT = "#1B3052"

    TEXT = "#F4F7FF"
    MUTED = "#9DB3D0"

    GREEN = "#36D399"
    BLUE = "#60A5FA"
    PURPLE = "#A78BFA"
    ACCENT = "#FF6B8A"

    BORDER = "#29476E"
    SHADOW = "#040B12"

    def __init__(self, root):
        self.root = root

        # Core services
        self.document_manager = None
        self.answer_generator = None
        self.voice_assistant = None

        # Current workspace state
        self.current_file = None
        self.current_image = None
        self.last_response = ""

        # Offline mode is optional
        self.offline_mode = False

        # =====================================================
        # WINDOW
        # =====================================================

        self.root.title(
            "OFFLINE GENIUS — Private Multimodal AI Workstation"
        )

        self.root.geometry("1140x840")
        self.root.minsize(940, 720)
        self.root.configure(bg=self.BG)

        # =====================================================
        # BUILD UI
        # =====================================================

        self.init_voice()
        self.create_header()
        self.create_dashboard()
        self.create_chat_area()
        self.create_action_panel()
        self.create_footer()

        # Welcome message
        self.add_message(
            "SYSTEM:\n"
            "Welcome to OFFLINE GENIUS.\n\n"
            "AI for everyone — documents, images, questions "
            "and voice from one workspace.\n\n"
            "ONLINE READY • OFFLINE CAPABLE • PRIVACY FIRST"
        )

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
    # VOICE
    # =========================================================

    def init_voice(self):
        """Initialize the local Windows voice assistant."""

        try:
            self.project_root()

            from app.voice.voice_assistant import OfflineVoiceAssistant

            self.voice_assistant = OfflineVoiceAssistant()

        except Exception:
            self.voice_assistant = None

    def speak_text(self, text: str):
        """Speak clean text using the local voice engine."""

        if not self.voice_assistant or not text:
            return

        clean = []

        for line in str(text).split("\n"):
            if (
                "Users\\" not in line
                and "AppData\\" not in line
                and "Document(" not in line
                and "LOCAL RETRIEVAL" not in line
                and "NO CLOUD UPLOAD" not in line
            ):
                clean.append(line.strip())

        clean_text = " ".join(
            line for line in clean if line
        ).strip()

        if not clean_text:
            return

        self.update_voice_status("🔊 SPEAKING...")

        try:
            self.voice_assistant.speak(clean_text)

            self.root.after(
                3000,
                lambda: self.update_voice_status("🎤 SPEAK"),
            )

        except Exception:
            self.update_voice_status("🎤 SPEAK")

    def update_voice_status(self, label_text):
        """Update the voice button text."""

        if hasattr(self, "speak_btn"):
            self.speak_btn.config(text=label_text)

    def speak_last_response(self):
        """Read the latest useful AI response."""

        if not self.voice_assistant:
            messagebox.showwarning(
                "Voice Assistant",
                "Offline voice is not available on this system.",
            )
            return

        if not self.last_response:
            self.speak_text(
                "Offline Genius Voice Assistant Ready."
            )
            return

        self.speak_text(self.last_response)

    # =========================================================
    # BUTTON FACTORY
    # =========================================================

    def make_button(
        self,
        parent,
        text,
        command,
        bg,
        fg,
        hover_bg=None,
        padx=14,
        pady=8,
        font=None,
    ):
        """Create a polished button with hover feedback."""

        if hover_bg is None:
            hover_bg = bg

        if font is None:
            font = ("Segoe UI", 9, "bold")

        button = tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg=fg,
            activebackground=hover_bg,
            activeforeground=fg,
            relief="flat",
            borderwidth=0,
            padx=padx,
            pady=pady,
            font=font,
            cursor="hand2",
        )

        button.bind(
            "<Enter>",
            lambda event, b=button, target=hover_bg:
            b.config(bg=target),
        )

        button.bind(
            "<Leave>",
            lambda event, b=button, target=bg:
            b.config(bg=target),
        )

        return button

    # =========================================================
    # HEADER
    # =========================================================

    def create_header(self):

        header = tk.Frame(
            self.root,
            bg=self.BG,
            padx=25,
            pady=22,
        )

        header.pack(fill="x")

        header_card = tk.Frame(
            header,
            bg=self.PANEL,
            highlightbackground=self.BORDER,
            highlightthickness=1,
            padx=18,
            pady=14,
        )

        header_card.pack(fill="x")

        title_row = tk.Frame(
            header_card,
            bg=self.PANEL,
        )

        title_row.pack(fill="x")

        # Logo
        logo = tk.Frame(
            title_row,
            bg=self.BLUE,
            padx=10,
            pady=9,
        )

        logo.pack(
            side="left",
            padx=(0, 12),
        )

        tk.Label(
            logo,
            text="OG",
            bg=self.BLUE,
            fg="white",
            font=("Segoe UI", 15, "bold"),
        ).pack()

        # Title
        title_stack = tk.Frame(
            title_row,
            bg=self.PANEL,
        )

        title_stack.pack(side="left")

        tk.Label(
            title_stack,
            text="OFFLINE GENIUS",
            bg=self.PANEL,
            fg=self.TEXT,
            font=("Segoe UI", 24, "bold"),
        ).pack(anchor="w")

        tk.Label(
            title_stack,
            text="Private, Multimodal AI Workstation",
            bg=self.PANEL,
            fg=self.MUTED,
            font=("Segoe UI", 9),
        ).pack(
            anchor="w",
            pady=(2, 0),
        )

        # Snapdragon badge
        badge = tk.Frame(
            title_row,
            bg=self.PANEL_LIGHT,
            padx=10,
            pady=6,
            highlightbackground=self.BLUE,
            highlightthickness=1,
        )

        badge.pack(
            side="left",
            padx=14,
        )

        tk.Label(
            badge,
            text="⚡ SNAPDRAGON READY",
            bg=self.PANEL_LIGHT,
            fg=self.BLUE,
            font=("Segoe UI", 8, "bold"),
        ).pack()

        # Status
        self.header_status = tk.Label(
            title_row,
            text="● READY",
            bg=self.PANEL,
            fg=self.GREEN,
            font=("Segoe UI", 10, "bold"),
            padx=10,
            pady=6,
        )

        self.header_status.pack(
            side="right",
            pady=6,
        )

        tk.Label(
            header_card,
            text=(
                "AI FOR EVERYONE  •  ONLINE READY  •  "
                "OFFLINE CAPABLE  •  PRIVACY FIRST"
            ),
            bg=self.PANEL,
            fg=self.MUTED,
            font=("Segoe UI", 9, "bold"),
        ).pack(
            anchor="w",
            pady=(10, 0),
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
            text="WORKSPACE STATUS",
            bg=self.BG,
            fg=self.TEXT,
            font=("Segoe UI", 12, "bold"),
        ).pack(
            anchor="w",
            pady=(0, 8),
        )

        cards = tk.Frame(
            outer,
            bg=self.BG,
        )

        cards.pack(fill="x")

        self.create_status_card(
            cards,
            "🔒 PRIVACY",
            "READY",
            "Privacy-first workspace",
            "privacy",
        )

        self.create_status_card(
            cards,
            "◉ MODE",
            "ONLINE READY",
            "Offline mode available",
            "mode",
        )

        self.create_status_card(
            cards,
            "▣ DOCUMENT",
            "NONE",
            "Add a local document",
            "document",
        )

        self.create_status_card(
            cards,
            "⌁ KNOWLEDGE",
            "0 SECTIONS",
            "Local knowledge available",
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
            padx=16,
            pady=12,
        )

        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5,
            pady=2,
        )

        tk.Label(
            card,
            text=heading,
            bg=self.PANEL,
            fg=self.MUTED,
            font=("Segoe UI", 8, "bold"),
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
            font=("Segoe UI", 13, "bold"),
        )

        value_label.pack(
            anchor="w",
            pady=(4, 1),
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
            pady=12,
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
            text="AI ASSISTANT WORKSPACE",
            bg=self.BG,
            fg=self.TEXT,
            font=("Segoe UI", 12, "bold"),
        ).pack(side="left")

        tk.Label(
            title_row,
            text="MULTIMODAL AI ENGINE",
            bg=self.BG,
            fg=self.BLUE,
            font=("Segoe UI", 8, "bold"),
        ).pack(side="right")

        chat_frame = tk.Frame(
            outer,
            bg=self.PANEL,
            highlightbackground=self.BORDER,
            highlightthickness=1,
            padx=12,
            pady=12,
        )

        chat_frame.pack(
            fill="both",
            expand=True,
            pady=(6, 8),
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

        # Question input
        input_frame = tk.Frame(
            outer,
            bg=self.BG,
        )

        input_frame.pack(
            fill="x",
            pady=(2, 0),
        )

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
            ipady=10,
        )

        self.question.bind(
            "<Return>",
            lambda event: self.ask_ai(),
        )

        self.make_button(
            input_frame,
            text="RUN AI →",
            command=self.ask_ai,
            bg=self.BLUE,
            fg="white",
            hover_bg="#88B9FF",
            padx=18,
            pady=9,
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
            padx=15,
            pady=12,
        )

        panel.pack(fill="x")

        # Row 1
        row1 = tk.Frame(
            panel,
            bg=self.PANEL,
        )

        row1.pack(
            fill="x",
            pady=(0, 5),
        )

        self.offline_button = self.make_button(
            row1,
            text="⚡ GO OFFLINE",
            command=self.go_offline,
            bg=self.GREEN,
            fg="#08130D",
            hover_bg="#5BE3AC",
            padx=14,
            pady=7,
        )

        self.offline_button.pack(
            side="left",
            padx=3,
        )

        self.speak_btn = self.make_button(
            row1,
            text="🎤 SPEAK",
            command=self.speak_last_response,
            bg=self.BLUE,
            fg="white",
            hover_bg="#88B9FF",
            padx=14,
            pady=7,
        )

        self.speak_btn.pack(
            side="left",
            padx=3,
        )

        self.make_button(
            row1,
            text="🔒 PRIVACY STATUS",
            command=self.show_privacy,
            bg=self.PANEL_LIGHT,
            fg=self.TEXT,
            hover_bg=self.BORDER,
            padx=14,
            pady=7,
        ).pack(
            side="right",
            padx=3,
        )

        # Row 2
        row2 = tk.Frame(
            panel,
            bg=self.PANEL,
        )

        row2.pack(fill="x")

        self.make_button(
            row2,
            text="＋ ADD DOC",
            command=self.add_document,
            bg=self.PANEL_LIGHT,
            fg=self.TEXT,
            hover_bg=self.BORDER,
            padx=14,
            pady=7,
        ).pack(
            side="left",
            padx=3,
        )

        self.make_button(
            row2,
            text="◈ ANALYZE IMAGE",
            command=self.analyze_image,
            bg=self.PANEL_LIGHT,
            fg=self.TEXT,
            hover_bg=self.BORDER,
            padx=14,
            pady=7,
        ).pack(
            side="left",
            padx=3,
        )

        self.make_button(
            row2,
            text="◉ ASK IMAGE",
            command=self.ask_about_image,
            bg=self.PURPLE,
            fg="white",
            hover_bg="#B49BFF",
            padx=14,
            pady=7,
        ).pack(
            side="left",
            padx=3,
        )

        self.make_button(
            row2,
            text="👁 DESCRIBE IMAGE",
            command=self.describe_image,
            bg=self.PANEL_LIGHT,
            fg=self.TEXT,
            hover_bg=self.BORDER,
            padx=14,
            pady=7,
        ).pack(
            side="left",
            padx=3,
        )

    # =========================================================
    # FOOTER
    # =========================================================

    def create_footer(self):

        footer = tk.Frame(
            self.root,
            bg="#050C16",
            padx=25,
            pady=8,
            highlightbackground=self.BORDER,
            highlightthickness=1,
        )

        footer.pack(
            fill="x",
            side="bottom",
        )

        tk.Label(
            footer,
            text=(
                "SYSTEM READY  •  MULTIMODAL WORKSPACE  •  "
                "PRIVACY FIRST"
            ),
            bg="#050C16",
            fg=self.MUTED,
            font=("Segoe UI", 8, "bold"),
        ).pack(side="left")

        tk.Label(
            footer,
            text="OFFLINE GENIUS v1.0 • SNAPDRAGON READY",
            bg="#050C16",
            fg=self.BLUE,
            font=("Segoe UI", 8, "bold"),
        ).pack(side="right")

    # =========================================================
    # CHAT OUTPUT
    # =========================================================

    def add_message(self, message):

        self.chat.config(state="normal")

        self.chat.insert(
            "end",
            message + "\n\n",
        )

        self.chat.config(
            state="disabled"
        )

        self.chat.see("end")

        # Save latest useful AI response
        lines = [
            line.strip()
            for line in str(message).split("\n")
            if line.strip()
        ]

        if lines:

            first = lines[0]

            if first in (
                "OFFLINE GENIUS:",
                "OFFLINE VISION:",
            ):

                answer = "\n".join(
                    lines[1:]
                ).strip()

                if answer:
                    self.last_response = answer

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
                f"ANSWER GENERATOR ERROR:\n{error}"
            )

            return False

    # =========================================================
    # AI QUESTION ROUTING
    # =========================================================

    def ask_ai(self):

        question = self.question.get().strip()

        if not question:
            return

        # Image mode
        if self.current_image:

            try:

                self.project_root()

                from app.vision.local_vision import (
                    LocalVisionUnderstanding
                )

                vision = LocalVisionUnderstanding(
                    self.current_image
                )

                self.add_message(
                    "YOU:\n" + question
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

                self.last_response = answer

                self.speak_text(answer)

            except Exception as error:

                self.add_message(
                    f"VISION ERROR:\n{error}"
                )

            self.question.delete(
                0,
                "end",
            )

            return

        # Normal AI mode
        self.add_message(
            "YOU:\n" + question
        )

        if self.document_manager is None:

            msg = (
                "I don't have a document in the "
                "Knowledge Vault yet.\n\n"
                "Add a document to ask questions "
                "about your own files."
            )

            self.add_message(
                "OFFLINE GENIUS:\n" + msg
            )

            self.last_response = msg

            self.speak_text(msg)

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

                msg = (
                    "I couldn't find enough information "
                    "in your local documents."
                )

                self.add_message(
                    "OFFLINE GENIUS:\n" + msg
                )

                self.last_response = msg

                self.speak_text(msg)

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

            answer = answer_result.answer

            self.add_message(
                "OFFLINE GENIUS:\n" + answer
            )

            self.last_response = answer

            self.add_message(
                "SOURCE:\n"
                + answer_result.source
                + "\n\n"
                "LOCAL RETRIEVAL • NO CLOUD UPLOAD"
            )

            self.speak_text(answer)

        except Exception as error:

            self.add_message(
                f"KNOWLEDGE VAULT ERROR:\n{error}"
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
                "OFFLINE MODE is already active."
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
            text="Network-isolated workspace"
        )

        self.privacy_value.config(
            text="LOCAL ONLY",
            fg=self.GREEN,
        )

        self.privacy_detail.config(
            text="Cloud access disabled"
        )

        self.offline_button.config(
            text="✓ OFFLINE ACTIVE",
            bg=self.GREEN,
        )

        self.add_message(
            "SYSTEM:\n"
            "✓ OFFLINE MODE activated.\n"
            "✓ Internet-dependent features are not required.\n"
            "✓ Local Knowledge Vault remains available.\n"
            "✓ Documents and images remain on this PC."
        )

    # =========================================================
    # DOCUMENTS
    # =========================================================

    def add_document(self):

        file_path = filedialog.askopenfilename(
            title="Select a document",

            filetypes=[
                ("PDF files", "*.pdf"),
                ("Text files", "*.txt"),
                ("Markdown files", "*.md"),
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
                self.document_manager = DocumentManager()

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

                display_name = (
                    path.name[:12] + "..."
                    if len(path.name) > 12
                    else path.name
                )

                self.document_value.config(
                    text=display_name
                )

                self.document_detail.config(
                    text="Processed on-device"
                )

                section_count = (
                    self.document_manager.count()
                )

                self.sections_value.config(
                    text=f"{section_count} SECTIONS",
                    fg=self.BLUE,
                )

                self.add_message(
                    "KNOWLEDGE VAULT:\n"
                    "✓ Document indexed locally.\n"
                    f"File: {path.name}\n"
                    "✓ Ready for private document Q&A."
                )

                messagebox.showinfo(
                    "Knowledge Vault",
                    "Document successfully processed locally."
                )

            else:

                messagebox.showwarning(
                    "Knowledge Vault",
                    "Could not process document."
                )

        except Exception as error:

            messagebox.showerror(
                "Document Error",
                "Could not process document:\n\n"
                + str(error),
            )

    # =========================================================
    # IMAGE ANALYSIS
    # =========================================================

    def analyze_image(self):

        file_path = filedialog.askopenfilename(
            title="Select an image",

            filetypes=[
                (
                    "Image files",
                    "*.png *.jpg *.jpeg *.webp *.bmp"
                ),
                (
                    "All files",
                    "*.*"
                ),
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
                f"✓ Resolution: "
                f"{result.width} × {result.height}\n"
                f"✓ Format: {result.format}\n"
                f"✓ Size: {result.size_kb} KB\n\n"
                "✓ Image remains on this PC."
            )

            messagebox.showinfo(
                "Offline Vision",
                "Image analyzed locally."
            )

        except Exception as error:

            messagebox.showerror(
                "Vision Error",
                "Could not analyze image:\n\n"
                + str(error),
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

            from app.vision.local_vision import (
                LocalVisionUnderstanding
            )

            vision = LocalVisionUnderstanding(
                self.current_image
            )

            self.add_message(
                "YOU:\n" + question
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

            self.last_response = answer

            self.speak_text(answer)

        except Exception as error:

            messagebox.showerror(
                "Vision Error",
                str(error),
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

            self.last_response = description

            self.speak_text(description)

        except Exception as error:

            messagebox.showerror(
                "Vision Error",
                str(error),
            )

    # =========================================================
    # PRIVACY
    # =========================================================

    def show_privacy(self):

        messagebox.showinfo(
            "Privacy & AI Modes",

            "🔒 OFFLINE GENIUS PRIVACY\n\n"

            "AI MODE:\n"
            "Online-ready + Offline-capable\n\n"

            "DOCUMENTS:\n"
            "Local files can be processed on this PC.\n\n"

            "IMAGES:\n"
            "Local image analysis is supported.\n\n"

            "VOICE:\n"
            "Windows built-in offline speech.\n\n"

            "OFFLINE MODE:\n"
            "Use GO OFFLINE when you want the workspace "
            "to operate without relying on internet services.\n\n"

            "SNAPDRAGON:\n"
            "Architecture is designed to be optimized "
            "for compatible Snapdragon-powered PCs.\n\n"

            "PRIVACY:\n"
            "The prototype's local workflows do not "
            "upload documents or images to a cloud service."
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