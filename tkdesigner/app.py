"""Tkinter Designer desktop application.

The desktop app intentionally shares the same Designer workflow as the CLI.
Network and generation work runs off the Tk event loop so the interface stays
responsive on larger Figma files.
"""

import os
from pathlib import Path
from queue import Empty, Queue
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import webbrowser

from . import __version__
from .designer import Designer
from .utils import parse_figma_url


COLORS = {
    "background": "#F4F6FA",
    "surface": "#FFFFFF",
    "text": "#182230",
    "muted": "#667085",
    "border": "#D0D5DD",
    "brand": "#2563EB",
    "brand_hover": "#1D4ED8",
    "success": "#067647",
    "danger": "#B42318",
}


def supports_desktop_tk(platform: str, patchlevel: str) -> bool:
    """Reject Apple's deprecated Tk 8.5, which renders blank on modern macOS."""
    if platform != "darwin":
        return True
    try:
        version = tuple(int(part) for part in patchlevel.split(".")[:2])
    except ValueError:
        return False
    return version >= (8, 6)


class DesignerApp:
    def __init__(self, root):
        self.root = root
        self.events = Queue()
        self.working = False

        self.url = tk.StringVar()
        self.token = tk.StringVar(value=os.getenv("FIGMA_TOKEN", ""))
        self.output = tk.StringVar(value=str(Path.cwd()))
        self.template = tk.StringVar(value="class")
        self.theme = tk.StringVar(value="clam")
        self.show_token = tk.BooleanVar(value=False)
        self.status = tk.StringVar(value="Ready to inspect a design")

        self._configure_window()
        self._configure_styles()
        self._build_ui()
        self.root.after(100, self._poll_events)

    def _configure_window(self):
        self.root.title(f"Tkinter Designer {__version__}")
        self.root.geometry("960x720")
        self.root.minsize(820, 620)
        self.root.configure(bg=COLORS["background"])

    def _configure_styles(self):
        style = ttk.Style(self.root)
        if "clam" in style.theme_names():
            style.theme_use("clam")
        style.configure("App.TFrame", background=COLORS["background"])
        style.configure("Card.TFrame", background=COLORS["surface"])
        style.configure(
            "Title.TLabel",
            background=COLORS["background"],
            foreground=COLORS["text"],
            font=("TkDefaultFont", 24, "bold"),
        )
        style.configure(
            "Subtitle.TLabel",
            background=COLORS["background"],
            foreground=COLORS["muted"],
            font=("TkDefaultFont", 11),
        )
        style.configure(
            "Section.TLabel",
            background=COLORS["surface"],
            foreground=COLORS["text"],
            font=("TkDefaultFont", 12, "bold"),
        )
        style.configure(
            "Field.TLabel",
            background=COLORS["surface"],
            foreground=COLORS["muted"],
        )
        style.configure(
            "Primary.TButton",
            background=COLORS["brand"],
            foreground="#FFFFFF",
            borderwidth=0,
            padding=(18, 11),
            font=("TkDefaultFont", 10, "bold"),
        )
        style.map(
            "Primary.TButton",
            background=[("active", COLORS["brand_hover"]), ("disabled", "#98A2B3")],
        )
        style.configure("Secondary.TButton", padding=(16, 10))
        style.configure(
            "Status.TLabel",
            background=COLORS["background"],
            foreground=COLORS["muted"],
        )

    def _build_ui(self):
        shell = ttk.Frame(self.root, style="App.TFrame", padding=(36, 28))
        shell.pack(fill="both", expand=True)
        shell.columnconfigure(0, weight=1)
        shell.rowconfigure(2, weight=1)

        header = ttk.Frame(shell, style="App.TFrame")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header.columnconfigure(0, weight=1)
        ttk.Label(header, text="Tkinter Designer", style="Title.TLabel").grid(
            row=0, column=0, sticky="w")
        ttk.Label(
            header,
            text="Inspect first. Generate confidently.",
            style="Subtitle.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(4, 0))
        ttk.Button(
            header,
            text="Guide",
            command=lambda: webbrowser.open_new_tab(
                "https://github.com/ParthJadhav/Tkinter-Designer/blob/master/docs/instructions.md"
            ),
        ).grid(row=0, column=1, rowspan=2, sticky="e")

        form = ttk.Frame(shell, style="Card.TFrame", padding=24)
        form.grid(row=1, column=0, sticky="ew")
        form.columnconfigure(0, weight=1)
        ttk.Label(form, text="Design source", style="Section.TLabel").grid(
            row=0, column=0, columnspan=3, sticky="w", pady=(0, 16))

        self._field_label(form, "Figma design URL", 1)
        self.url_entry = ttk.Entry(form, textvariable=self.url)
        self.url_entry.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(5, 14))

        self._field_label(form, "Personal access token", 3)
        self.token_entry = ttk.Entry(form, textvariable=self.token, show="•")
        self.token_entry.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(5, 14))
        ttk.Checkbutton(
            form,
            text="Show",
            variable=self.show_token,
            command=self._toggle_token,
        ).grid(row=4, column=2, padx=(10, 0), sticky="w")

        self._field_label(form, "Output folder", 5)
        self.output_entry = ttk.Entry(form, textvariable=self.output)
        self.output_entry.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(5, 14))
        ttk.Button(form, text="Browse…", command=self._choose_output).grid(
            row=6, column=2, padx=(10, 0), sticky="ew")

        options = ttk.Frame(form, style="Card.TFrame")
        options.grid(row=7, column=0, columnspan=3, sticky="ew")
        options.columnconfigure((0, 1), weight=1)
        ttk.Label(options, text="Code style", style="Field.TLabel").grid(
            row=0, column=0, sticky="w")
        ttk.Label(options, text="ttk theme", style="Field.TLabel").grid(
            row=0, column=1, sticky="w", padx=(12, 0))
        ttk.Combobox(
            options,
            textvariable=self.template,
            values=("script", "class", "pages"),
            state="readonly",
        ).grid(row=1, column=0, sticky="ew", pady=(5, 0))
        ttk.Combobox(
            options,
            textvariable=self.theme,
            values=("clam", "alt", "default", "classic"),
        ).grid(row=1, column=1, sticky="ew", padx=(12, 0), pady=(5, 0))

        result_card = ttk.Frame(shell, style="Card.TFrame", padding=24)
        result_card.grid(row=2, column=0, sticky="nsew", pady=(16, 0))
        result_card.columnconfigure(0, weight=1)
        result_card.rowconfigure(1, weight=1)
        ttk.Label(result_card, text="Design report", style="Section.TLabel").grid(
            row=0, column=0, sticky="w", pady=(0, 10))
        self.report = tk.Text(
            result_card,
            height=9,
            wrap="word",
            relief="flat",
            bg="#F8FAFC",
            fg=COLORS["text"],
            padx=14,
            pady=12,
            font=("TkFixedFont", 10),
            state="disabled",
        )
        self.report.grid(row=1, column=0, sticky="nsew")

        footer = ttk.Frame(shell, style="App.TFrame")
        footer.grid(row=3, column=0, sticky="ew", pady=(16, 0))
        footer.columnconfigure(1, weight=1)
        self.inspect_button = ttk.Button(
            footer,
            text="Inspect design",
            style="Secondary.TButton",
            command=lambda: self._start("inspect"),
        )
        self.inspect_button.grid(row=0, column=0)
        self.progress = ttk.Progressbar(footer, mode="indeterminate", length=120)
        self.progress.grid(row=0, column=1, padx=14, sticky="w")
        self.generate_button = ttk.Button(
            footer,
            text="Generate project",
            style="Primary.TButton",
            command=lambda: self._start("generate"),
        )
        self.generate_button.grid(row=0, column=2)
        ttk.Label(footer, textvariable=self.status, style="Status.TLabel").grid(
            row=1, column=0, columnspan=3, sticky="w", pady=(10, 0))

        self.url_entry.focus_set()

    @staticmethod
    def _field_label(parent, text, row):
        ttk.Label(parent, text=text, style="Field.TLabel").grid(
            row=row, column=0, columnspan=3, sticky="w")

    def _toggle_token(self):
        self.token_entry.configure(show="" if self.show_token.get() else "•")

    def _choose_output(self):
        selected = filedialog.askdirectory(initialdir=self.output.get() or str(Path.cwd()))
        if selected:
            self.output.set(selected)

    def _inputs(self):
        reference = parse_figma_url(self.url.get())
        token = self.token.get().strip()
        if not token:
            raise ValueError("Enter a Figma personal access token.")
        output = Path(self.output.get().strip()).expanduser().resolve()
        if not self.output.get().strip():
            raise ValueError("Choose an output folder.")
        return reference, token, output

    def _start(self, operation):
        if self.working:
            return
        try:
            reference, token, output = self._inputs()
        except (OSError, ValueError) as exc:
            messagebox.showerror("Check the design details", str(exc))
            return

        build_path = output / "build"
        clean = False
        if (
            operation == "generate"
            and build_path.is_dir()
            and any(build_path.iterdir())
        ):
            clean = messagebox.askyesno(
                "Replace existing build?",
                "The build folder is not empty. It will only be replaced after "
                "the new project generates successfully.",
            )
            if not clean:
                return

        self._set_working(True, "Inspecting Figma…" if operation == "inspect" else "Generating project…")
        worker = threading.Thread(
            target=self._run_operation,
            args=(
                operation,
                reference,
                token,
                build_path,
                clean,
                self.template.get(),
                self.theme.get().strip(),
            ),
            daemon=True,
        )
        worker.start()

    def _run_operation(
        self, operation, reference, token, build_path, clean, template, theme
    ):
        try:
            designer = Designer(
                token,
                reference.file_key,
                build_path,
                node_id=reference.node_id,
                template_style=template,
                theme=theme,
            )
            if operation == "inspect":
                report = designer.inspect()
                self.events.put(("success", report.to_text(), "Inspection complete"))
            else:
                result = designer.design(clean=clean)
                report = result.report.to_text() if result.report else "Generation complete"
                detail = (
                    f"{report}\n\nGenerated project: {result.output_path}\n"
                    f"Code files: {len(result.code_files)} · Assets: {len(result.asset_files)}"
                )
                self.events.put(("success", detail, f"Generated at {result.output_path}"))
        except Exception as exc:
            self.events.put(("error", str(exc), "Generation failed"))

    def _poll_events(self):
        try:
            event, detail, status = self.events.get_nowait()
        except Empty:
            pass
        else:
            self._set_working(False, status)
            if event == "success":
                self._set_report(detail)
            else:
                messagebox.showerror("Tkinter Designer", detail)
        self.root.after(100, self._poll_events)

    def _set_report(self, value):
        self.report.configure(state="normal")
        self.report.delete("1.0", "end")
        self.report.insert("1.0", value)
        self.report.configure(state="disabled")

    def _set_working(self, working, status):
        self.working = working
        self.status.set(status)
        state = "disabled" if working else "normal"
        self.inspect_button.configure(state=state)
        self.generate_button.configure(state=state)
        if working:
            self.progress.start(12)
        else:
            self.progress.stop()


def main():
    root = tk.Tk()
    patchlevel = str(root.tk.call("info", "patchlevel"))
    if not supports_desktop_tk(sys.platform, patchlevel):
        message = (
            f"Tkinter Designer requires Tk 8.6 or newer on macOS; this Python "
            f"uses Tk {patchlevel}. Install a current Python distribution with "
            "modern Tk support, recreate the virtual environment, and try again."
        )
        root.withdraw()
        print(f"error: {message}", file=sys.stderr)
        try:
            messagebox.showerror("Tkinter Designer", message, parent=root)
        finally:
            root.destroy()
        return 1
    DesignerApp(root)
    root.mainloop()
    return 0


if __name__ == "__main__":
    main()
