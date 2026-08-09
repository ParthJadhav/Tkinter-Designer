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
import tkinter.font as tkfont
from tkinter import filedialog, messagebox
import webbrowser

from . import __version__
from .designer import Designer
from .utils import parse_figma_url


COLORS = {
    "background": "#F6F7FB",
    "surface": "#FFFFFF",
    "surface_subtle": "#F8FAFC",
    "sidebar": "#2867E8",
    "sidebar_dark": "#1F58CB",
    "sidebar_text": "#FFFFFF",
    "sidebar_muted": "#C9D8FF",
    "text": "#172033",
    "muted": "#667085",
    "border": "#DCE1EA",
    "border_strong": "#B9C1CF",
    "brand": "#2867E8",
    "brand_hover": "#1F58CB",
    "brand_pressed": "#1949AC",
    "focus": "#155EEF",
    "disabled": "#98A2B3",
    "success": "#067647",
    "danger": "#B42318",
}


class ActionButton(tk.Label):
    """Flat, keyboard-accessible action with consistent cross-platform styling."""

    def __init__(
        self,
        parent,
        *,
        text,
        command,
        font,
        variant="secondary",
        compact=False,
    ):
        self.command = command
        self.enabled = True
        self.variant = variant
        self.palette = self._palette(variant)
        super().__init__(
            parent,
            text=text,
            bg=self.palette["background"],
            fg=self.palette["foreground"],
            activebackground=self.palette["hover"],
            activeforeground=self.palette["foreground"],
            font=font,
            padx=10 if compact else 16,
            pady=7 if compact else 10,
            cursor="hand2",
            takefocus=True,
            highlightthickness=1,
            highlightbackground=self.palette["border"],
            highlightcolor=COLORS["focus"],
            borderwidth=0,
            relief="flat",
        )
        self.bind("<Enter>", lambda _event: self._paint("hover"))
        self.bind("<Leave>", lambda _event: self._paint("background"))
        self.bind("<ButtonPress-1>", lambda _event: self._paint("pressed"))
        self.bind("<ButtonRelease-1>", self._click)
        self.bind("<Return>", self._click)
        self.bind("<space>", self._click)

    @staticmethod
    def _palette(variant):
        if variant == "primary":
            return {
                "background": COLORS["brand"],
                "hover": COLORS["brand_hover"],
                "pressed": COLORS["brand_pressed"],
                "foreground": "#FFFFFF",
                "border": COLORS["brand"],
            }
        if variant == "ghost":
            return {
                "background": COLORS["surface"],
                "hover": COLORS["surface_subtle"],
                "pressed": "#EEF2F7",
                "foreground": COLORS["text"],
                "border": COLORS["surface"],
            }
        return {
            "background": "#EEF2F7",
            "hover": "#E4E9F1",
            "pressed": "#D9E0EA",
            "foreground": COLORS["text"],
            "border": COLORS["border_strong"],
        }

    def _paint(self, state):
        if self.enabled:
            self.configure(bg=self.palette[state])

    def _click(self, _event=None):
        if self.enabled:
            self.focus_set()
            self.configure(bg=self.palette["hover"])
            self.command()

    def set_enabled(self, enabled):
        self.enabled = enabled
        if enabled:
            self.configure(
                bg=self.palette["background"],
                fg=self.palette["foreground"],
                cursor="hand2",
            )
        else:
            self.configure(
                bg=COLORS["surface_subtle"],
                fg=COLORS["disabled"],
                cursor="arrow",
            )


class ChoiceMenu(tk.Frame):
    """A light, consistent collapsed menu that delegates choices to Tk."""

    def __init__(self, parent, *, variable, values, font):
        super().__init__(
            parent,
            bg=COLORS["surface"],
            cursor="hand2",
            takefocus=True,
            highlightthickness=1,
            highlightbackground=COLORS["border_strong"],
            highlightcolor=COLORS["focus"],
        )
        self.variable = variable
        self.menu = tk.Menu(
            self,
            tearoff=False,
            bg=COLORS["surface"],
            fg=COLORS["text"],
            activebackground=COLORS["brand"],
            activeforeground="#FFFFFF",
            font=font,
        )
        for value in values:
            self.menu.add_radiobutton(
                label=value,
                value=value,
                variable=variable,
            )

        label = tk.Label(
            self,
            textvariable=variable,
            anchor="w",
            bg=COLORS["surface"],
            fg=COLORS["text"],
            font=font,
            padx=11,
            pady=8,
            cursor="hand2",
        )
        label.pack(side="left", fill="both", expand=True)
        arrow = tk.Label(
            self,
            text="⌄",
            bg=COLORS["surface"],
            fg=COLORS["muted"],
            font=font,
            padx=10,
            cursor="hand2",
        )
        arrow.pack(side="right", fill="y")
        for widget in (self, label, arrow):
            widget.bind("<Button-1>", self._open)
        self.bind("<Return>", self._open)
        self.bind("<space>", self._open)

    def _open(self, _event=None):
        self.focus_set()
        try:
            self.menu.tk_popup(
                self.winfo_rootx(),
                self.winfo_rooty() + self.winfo_height(),
            )
        finally:
            self.menu.grab_release()


class ProgressIndicator(tk.Canvas):
    """Small determinate-looking activity bar without platform theme leakage."""

    def __init__(self, parent):
        super().__init__(
            parent,
            width=84,
            height=6,
            bg=COLORS["surface"],
            highlightthickness=0,
        )
        self.running = False
        self.position = 0
        self.after_id = None
        self.create_rectangle(0, 1, 84, 5, fill="#E7EBF2", outline="")
        self.bar = self.create_rectangle(-24, 1, 0, 5, fill=COLORS["brand"], outline="")

    def start(self, _interval=None):
        if not self.running:
            self.running = True
            self.position = 0
            self._tick()

    def stop(self):
        self.running = False
        if self.after_id is not None:
            self.after_cancel(self.after_id)
            self.after_id = None
        self.coords(self.bar, -24, 1, 0, 5)

    def _tick(self):
        if not self.running:
            return
        self.position = (self.position + 4) % 108
        left = self.position - 24
        self.coords(self.bar, left, 1, left + 24, 5)
        self.after_id = self.after(32, self._tick)


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
        self.output = tk.StringVar(value=str(Path.home() / "TkinterDesigner"))
        self.template = tk.StringVar(value="class")
        self.theme = tk.StringVar(value="clam")
        self.show_token = tk.BooleanVar(value=False)
        self.status = tk.StringVar(value="Ready to inspect a design")
        self.report_state = tk.StringVar(value="Not inspected")

        self._configure_window()
        self._configure_styles()
        self._build_ui()
        self.root.after(100, self._poll_events)

    def _configure_window(self):
        self.root.title(f"Tkinter Designer {__version__}")
        self.root.geometry("980x760")
        self.root.minsize(900, 680)
        self.root.configure(bg=COLORS["background"])

    def _configure_styles(self):
        default_font = tkfont.nametofont("TkDefaultFont")
        family = default_font.actual("family")
        self.fonts = {
            "brand": (family, 15, "bold"),
            "display": (family, 25, "bold"),
            "title": (family, 20, "bold"),
            "heading": (family, 12, "bold"),
            "body": (family, 10),
            "body_bold": (family, 10, "bold"),
            "label": (family, 9, "bold"),
            "small": (family, 9),
        }

    def _build_ui(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self._build_sidebar()

        workspace = tk.Frame(self.root, bg=COLORS["surface"], padx=34, pady=28)
        workspace.grid(row=0, column=1, sticky="nsew")
        workspace.grid_columnconfigure(0, weight=1)
        workspace.grid_rowconfigure(6, weight=1)

        header = tk.Frame(workspace, bg=COLORS["surface"])
        header.grid(row=0, column=0, sticky="ew", pady=(0, 22))
        header.grid_columnconfigure(0, weight=1)
        tk.Label(
            header,
            text="Generate a project",
            bg=COLORS["surface"],
            fg=COLORS["text"],
            font=self.fonts["title"],
        ).grid(row=0, column=0, sticky="w")
        tk.Label(
            header,
            text="Connect a Figma design, review the plan, then create clean Tkinter code.",
            bg=COLORS["surface"],
            fg=COLORS["muted"],
            font=self.fonts["body"],
        ).grid(row=1, column=0, sticky="w", pady=(5, 0))
        ActionButton(
            header,
            text="Open guide  ↗",
            command=lambda: webbrowser.open_new_tab(
                "https://github.com/ParthJadhav/Tkinter-Designer/blob/master/docs/instructions.md"
            ),
            font=self.fonts["body_bold"],
            variant="ghost",
            compact=True,
        ).grid(row=0, column=1, rowspan=2, sticky="e")

        self._section_heading(workspace, "Figma source", 1)
        source = tk.Frame(workspace, bg=COLORS["surface"])
        source.grid(row=2, column=0, sticky="ew", pady=(10, 20))
        source.grid_columnconfigure(0, weight=1)

        self._field_label(source, "Figma design URL", 0)
        self.url_entry = self._entry(source, self.url)
        self.url_entry.grid(row=1, column=0, sticky="ew", pady=(6, 12), ipady=8)

        token_header = tk.Frame(source, bg=COLORS["surface"])
        token_header.grid(row=2, column=0, sticky="ew")
        token_header.grid_columnconfigure(0, weight=1)
        self._field_label(token_header, "Personal access token", 0)
        self.token_toggle = ActionButton(
            token_header,
            text="Show",
            command=self._toggle_token_visibility,
            font=self.fonts["small"],
            variant="ghost",
            compact=True,
        )
        self.token_toggle.grid(row=0, column=1, sticky="e")
        self.token_entry = self._entry(source, self.token, show="•")
        self.token_entry.grid(row=3, column=0, sticky="ew", pady=(4, 0), ipady=8)

        self._section_heading(workspace, "Project settings", 3)
        settings = tk.Frame(workspace, bg=COLORS["surface"])
        settings.grid(row=4, column=0, sticky="ew", pady=(10, 20))
        settings.grid_columnconfigure((0, 1), weight=1)

        self._field_label(settings, "Output folder", 0, columnspan=2)
        output_row = tk.Frame(settings, bg=COLORS["surface"])
        output_row.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(6, 5))
        output_row.grid_columnconfigure(0, weight=1)
        self.output_entry = self._entry(output_row, self.output)
        self.output_entry.grid(row=0, column=0, sticky="ew", ipady=8)
        ActionButton(
            output_row,
            text="Browse…",
            command=self._choose_output,
            font=self.fonts["body_bold"],
            compact=True,
        ).grid(row=0, column=1, padx=(8, 0), sticky="ns")
        tk.Label(
            settings,
            text="A build folder will be created inside this location.",
            bg=COLORS["surface"],
            fg=COLORS["muted"],
            font=self.fonts["small"],
        ).grid(row=2, column=0, columnspan=2, sticky="w", pady=(0, 11))

        self._field_label(settings, "Code style", 3)
        self._field_label(settings, "Generated app theme", 3, column=1)
        ChoiceMenu(
            settings,
            variable=self.template,
            values=("script", "class", "pages"),
            font=self.fonts["body"],
        ).grid(row=4, column=0, sticky="ew", pady=(6, 0), padx=(0, 6))
        ChoiceMenu(
            settings,
            variable=self.theme,
            values=("clam", "alt", "default", "classic"),
            font=self.fonts["body"],
        ).grid(row=4, column=1, sticky="ew", pady=(6, 0), padx=(6, 0))

        self._build_report(workspace)
        self._build_footer(workspace)
        self.url_entry.focus_set()

    def _build_sidebar(self):
        sidebar = tk.Frame(self.root, bg=COLORS["sidebar"], width=276)
        sidebar.grid(row=0, column=0, sticky="ns")
        sidebar.grid_propagate(False)
        sidebar.grid_columnconfigure(0, weight=1)
        sidebar.grid_rowconfigure(7, weight=1)

        brand = tk.Frame(sidebar, bg=COLORS["sidebar"])
        brand.grid(row=0, column=0, sticky="ew", padx=28, pady=(30, 0))
        tk.Label(
            brand,
            text="Tk",
            bg=COLORS["sidebar_text"],
            fg=COLORS["sidebar"],
            font=self.fonts["body_bold"],
            padx=7,
            pady=5,
        ).grid(row=0, column=0)
        tk.Label(
            brand,
            text="Tkinter Designer",
            bg=COLORS["sidebar"],
            fg=COLORS["sidebar_text"],
            font=self.fonts["brand"],
        ).grid(row=0, column=1, padx=(10, 0), sticky="w")

        tk.Label(
            sidebar,
            text="From Figma\nto Tkinter.",
            justify="left",
            bg=COLORS["sidebar"],
            fg=COLORS["sidebar_text"],
            font=self.fonts["display"],
        ).grid(row=1, column=0, sticky="w", padx=28, pady=(48, 10))
        tk.Label(
            sidebar,
            text="Inspect first. Generate clean, portable Python.",
            justify="left",
            anchor="w",
            wraplength=214,
            bg=COLORS["sidebar"],
            fg=COLORS["sidebar_muted"],
            font=self.fonts["body"],
        ).grid(row=2, column=0, sticky="w", padx=28)

        steps = tk.Frame(sidebar, bg=COLORS["sidebar"])
        steps.grid(row=3, column=0, sticky="ew", padx=28, pady=(42, 0))
        self._sidebar_step(steps, 1, "Connect", "Paste your URL and token.", 0)
        self._sidebar_step(steps, 2, "Inspect", "Preview frames and warnings.", 1)
        self._sidebar_step(steps, 3, "Generate", "Create the Tkinter project.", 2)

        tk.Label(
            sidebar,
            text=f"Version {__version__}",
            bg=COLORS["sidebar"],
            fg=COLORS["sidebar_muted"],
            font=self.fonts["small"],
        ).grid(row=8, column=0, sticky="sw", padx=28, pady=26)

    def _sidebar_step(self, parent, number, title, detail, row):
        item = tk.Frame(parent, bg=COLORS["sidebar"])
        item.grid(row=row, column=0, sticky="ew", pady=(0, 20))
        marker = tk.Canvas(
            item,
            width=28,
            height=28,
            bg=COLORS["sidebar"],
            highlightthickness=0,
        )
        marker.grid(row=0, column=0, rowspan=2, sticky="n")
        marker.create_oval(2, 2, 26, 26, fill=COLORS["sidebar_dark"], outline="#6F9AFA")
        marker.create_text(14, 14, text=str(number), fill="#FFFFFF", font=self.fonts["small"])
        tk.Label(
            item,
            text=title,
            bg=COLORS["sidebar"],
            fg=COLORS["sidebar_text"],
            font=self.fonts["body_bold"],
        ).grid(row=0, column=1, sticky="w", padx=(11, 0))
        tk.Label(
            item,
            text=detail,
            anchor="w",
            bg=COLORS["sidebar"],
            fg=COLORS["sidebar_muted"],
            font=self.fonts["small"],
        ).grid(row=1, column=1, sticky="w", padx=(11, 0), pady=(2, 0))

    def _build_report(self, workspace):
        report_header = tk.Frame(workspace, bg=COLORS["surface"])
        report_header.grid(row=5, column=0, sticky="new")
        report_header.grid_columnconfigure(0, weight=1)
        tk.Label(
            report_header,
            text="Design report",
            bg=COLORS["surface"],
            fg=COLORS["text"],
            font=self.fonts["heading"],
        ).grid(row=0, column=0, sticky="w")
        self.report_badge = tk.Label(
            report_header,
            textvariable=self.report_state,
            bg="#EEF4FF",
            fg=COLORS["brand_hover"],
            font=self.fonts["small"],
            padx=8,
            pady=3,
        )
        self.report_badge.grid(row=0, column=1, sticky="e")

        report_surface = tk.Frame(
            workspace,
            bg=COLORS["border"],
            highlightthickness=0,
        )
        report_surface.grid(row=6, column=0, sticky="nsew", pady=(9, 0))
        report_surface.grid_rowconfigure(0, weight=1)
        report_surface.grid_columnconfigure(0, weight=1)
        self.report = tk.Text(
            report_surface,
            height=6,
            wrap="word",
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            bg=COLORS["surface_subtle"],
            fg=COLORS["text"],
            padx=14,
            pady=12,
            font=self.fonts["body"],
            cursor="arrow",
            state="disabled",
        )
        self.report.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
        self._set_report(
            "No inspection yet\n\nPaste a Figma design URL and token, then inspect "
            "to preview frames, elements, assets, and fidelity warnings."
        )

    def _build_footer(self, workspace):
        footer = tk.Frame(workspace, bg=COLORS["surface"])
        footer.grid(row=7, column=0, sticky="ew", pady=(18, 0))
        footer.grid_columnconfigure(1, weight=1)
        self.status_dot = tk.Canvas(
            footer,
            width=12,
            height=12,
            bg=COLORS["surface"],
            highlightthickness=0,
        )
        self.status_dot.grid(row=0, column=0, sticky="w")
        self.status_indicator = self.status_dot.create_oval(
            3, 3, 9, 9, fill=COLORS["success"], outline=""
        )
        tk.Label(
            footer,
            textvariable=self.status,
            bg=COLORS["surface"],
            fg=COLORS["muted"],
            font=self.fonts["small"],
        ).grid(row=0, column=1, sticky="w", padx=(5, 0))
        self.progress = ProgressIndicator(footer)
        self.progress.grid(row=0, column=2, padx=(10, 16))
        self.progress.grid_remove()
        self.inspect_button = ActionButton(
            footer,
            text="Inspect design",
            command=lambda: self._start("inspect"),
            font=self.fonts["body_bold"],
        )
        self.inspect_button.grid(row=0, column=3, padx=(0, 8))
        self.generate_button = ActionButton(
            footer,
            text="Generate project",
            command=lambda: self._start("generate"),
            font=self.fonts["body_bold"],
            variant="primary",
        )
        self.generate_button.grid(row=0, column=4)

    def _section_heading(self, parent, text, row):
        heading = tk.Frame(parent, bg=COLORS["surface"])
        heading.grid(row=row, column=0, sticky="ew")
        heading.grid_columnconfigure(1, weight=1)
        tk.Label(
            heading,
            text=text,
            bg=COLORS["surface"],
            fg=COLORS["text"],
            font=self.fonts["heading"],
        ).grid(row=0, column=0, sticky="w")
        tk.Frame(heading, bg=COLORS["border"], height=1).grid(
            row=0, column=1, sticky="ew", padx=(12, 0)
        )

    def _field_label(self, parent, text, row, column=0, columnspan=1):
        tk.Label(
            parent,
            text=text,
            bg=COLORS["surface"],
            fg=COLORS["muted"],
            font=self.fonts["label"],
        ).grid(row=row, column=column, columnspan=columnspan, sticky="w")

    def _entry(self, parent, variable, *, show=None):
        return tk.Entry(
            parent,
            textvariable=variable,
            show=show,
            relief="flat",
            borderwidth=0,
            highlightthickness=1,
            highlightbackground=COLORS["border_strong"],
            highlightcolor=COLORS["focus"],
            bg=COLORS["surface"],
            fg=COLORS["text"],
            insertbackground=COLORS["text"],
            selectbackground=COLORS["brand"],
            selectforeground="#FFFFFF",
            font=self.fonts["body"],
        )

    def _toggle_token_visibility(self):
        self.show_token.set(not self.show_token.get())
        self._toggle_token()

    def _toggle_token(self):
        self.token_entry.configure(show="" if self.show_token.get() else "•")
        self.token_toggle.configure(text="Hide" if self.show_token.get() else "Show")

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
            status = (
                "Inspection failed"
                if operation == "inspect" else "Generation failed"
            )
            self.events.put(("error", str(exc), status))

    def _poll_events(self):
        try:
            event, detail, status = self.events.get_nowait()
        except Empty:
            pass
        else:
            self._set_working(False, status)
            if event == "success":
                self._set_report(detail)
                self._set_report_state(
                    "Inspected" if status == "Inspection complete" else "Generated",
                    "success",
                )
            else:
                self._set_report_state("Needs attention", "danger")
                self.status_dot.itemconfigure(
                    self.status_indicator, fill=COLORS["danger"]
                )
                messagebox.showerror("Tkinter Designer", detail)
        self.root.after(100, self._poll_events)

    def _set_report(self, value):
        self.report.configure(state="normal")
        self.report.delete("1.0", "end")
        self.report.insert("1.0", value)
        self.report.configure(state="disabled")

    def _set_report_state(self, value, tone):
        palette = {
            "info": ("#EEF4FF", COLORS["brand_hover"]),
            "success": ("#ECFDF3", COLORS["success"]),
            "danger": ("#FEF3F2", COLORS["danger"]),
        }
        background, foreground = palette[tone]
        self.report_state.set(value)
        self.report_badge.configure(bg=background, fg=foreground)

    def _set_working(self, working, status):
        self.working = working
        self.status.set(status)
        self.inspect_button.set_enabled(not working)
        self.generate_button.set_enabled(not working)
        if working:
            self._set_report_state("Working", "info")
            self.status_dot.itemconfigure(
                self.status_indicator, fill=COLORS["brand"]
            )
            self.progress.grid()
            self.progress.start(12)
        else:
            self.progress.stop()
            self.progress.grid_remove()
            self.status_dot.itemconfigure(
                self.status_indicator, fill=COLORS["success"]
            )


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
