"""Tkinter Designer desktop application.

The desktop app intentionally shares the same Designer workflow as the CLI.
Network and generation work runs off the Tk event loop so the interface stays
responsive on larger Figma files.

The window is a workbench: a fixed configuration rail on the left holding every
input and both actions, and the design report as the main pane, because the
report is what a user reads on every run after the first. Design tokens live in
`theme`, reusable controls in `widgets`, and the report document in
`report_view`.
"""

import os
from pathlib import Path
from queue import Empty, Queue
import subprocess
import sys
import threading
import tkinter as tk
import tkinter.font as tkfont
from tkinter import filedialog, messagebox
import webbrowser

from . import __version__
from . import report_view
from .designer import Designer
from .theme import (
    COLORS,
    DEFAULT_GEOMETRY,
    MAX_MEASURE,
    MIN_GEOMETRY,
    RAIL_WIDTH,
    SPACE,
    build_fonts,
    shortcut_labels,
)
from .utils import parse_figma_url
from .widgets import (
    CanvasButton,
    ChoiceMenu,
    InputShell,
    Placeholder,
    ProgressIndicator,
    QuietButton,
    SegmentedControl,
    StatusDot,
    field_label,
    make_entry,
    rounded_rect_points,
    section_header,
)

GUIDE_URL = (
    "https://github.com/ParthJadhav/Tkinter-Designer/blob/master/docs/instructions.md"
)

# Kept short enough to render on one line in the rail, so reserving room for
# them below does not inflate the minimum window height.
INVALID_URL = "Not a Figma design URL or file key."
MISSING_URL = "Paste a Figma design URL to continue."
MISSING_TOKEN = "Enter your Figma personal access token."
MISSING_OUTPUT = "Choose an output folder."

# The longest message each field can show, used to reserve room for inline
# validation so the pinned actions never get pushed off a short window.
WIDEST_MESSAGES = {"url": MISSING_URL, "token": MISSING_TOKEN, "output": MISSING_OUTPUT}


def supports_desktop_tk(platform: str, patchlevel: str) -> bool:
    """Reject Apple's deprecated Tk 8.5, which renders blank on modern macOS."""
    if platform != "darwin":
        return True
    try:
        version = tuple(int(part) for part in patchlevel.split(".")[:2])
    except ValueError:
        return False
    return version >= (8, 6)


def middle_truncate(value: str, limit: int = 58) -> str:
    """Shorten a long path for the single-line status strip."""
    if len(value) <= limit:
        return value
    head = (limit - 1) // 2
    tail = limit - 1 - head
    return f"{value[:head]}…{value[-tail:]}"


class FieldError(ValueError):
    """A validation failure that knows which field to point at."""

    def __init__(self, field: str, message: str):
        super().__init__(message)
        self.field = field


class FieldSlot:
    """One labelled input plus the helper line that doubles as its error."""

    def __init__(self, shell, entry, helper, default_helper=""):
        self.shell = shell
        self.entry = entry
        self.helper = helper
        self.default_helper = default_helper
        self.invalid = False

    def show_error(self, message):
        self.invalid = True
        self.shell.set_invalid(True)
        self.helper.configure(text=message, fg=COLORS["danger"])
        self.helper.grid()

    def clear_error(self):
        if not self.invalid:
            return
        self.invalid = False
        self.shell.set_invalid(False)
        self.reset_helper()

    def reset_helper(self):
        self.helper.configure(text=self.default_helper, fg=COLORS["ink_muted"])
        if self.default_helper:
            self.helper.grid()
        else:
            self.helper.grid_remove()

    def set_default_helper(self, text):
        self.default_helper = text
        if not self.invalid:
            self.reset_helper()


class DesignerApp:
    def __init__(self, root):
        self.root = root
        self.events = Queue()
        self.working = False
        self.report_text = ""
        self.last_report = None
        self.generated_path = None
        self.fields = {}

        self.url = tk.StringVar()
        self.token_from_env = bool(os.getenv("FIGMA_TOKEN"))
        self.token = tk.StringVar(value=os.getenv("FIGMA_TOKEN", ""))
        self.output = tk.StringVar(value=str(Path.home() / "TkinterDesigner"))
        self.template = tk.StringVar(value="class")
        self.theme = tk.StringVar(value="clam")
        self.show_token = tk.BooleanVar(value=False)
        self.status = tk.StringVar(value="Ready")

        self.shortcuts = shortcut_labels(sys.platform)
        self._configure_styles()
        self._configure_window()
        self._build_ui()
        self._bind_shortcuts()
        self._finish_layout()
        self.root.after(100, self._poll_events)

    # -- window ----------------------------------------------------------
    def _configure_styles(self):
        default_font = tkfont.nametofont("TkDefaultFont")
        fixed_font = tkfont.nametofont("TkFixedFont")
        self.fonts = build_fonts(
            default_font.actual("family"), fixed_font.actual("family")
        )

    def _configure_window(self):
        self.root.title(f"Tkinter Designer {__version__}")
        self.root.configure(bg=COLORS["bg_app"])
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def _finish_layout(self):
        """Size the window from real font metrics, then centre it."""
        min_width, min_height = self._required_size()
        self.root.minsize(min_width, min_height)
        width = max(DEFAULT_GEOMETRY[0], min_width)
        height = max(DEFAULT_GEOMETRY[1], min_height)
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        width = min(width, screen_width - 40)
        height = min(height, screen_height - 80)
        left = max(0, (screen_width - width) // 2)
        top = max(0, (screen_height - height) // 3)
        self.root.geometry(f"{width}x{height}+{left}+{top}")
        self._show_output_tail()
        self._focus_first()

    def _required_size(self):
        """Return the smallest window that still shows every rail control.

        Font metrics differ across platforms, so the minimum is measured rather
        than hard-coded, and it reserves room for the tallest inline validation
        message so an error can never push the actions out of view.
        """
        base = self._measured_height()
        tallest = base
        for name, message in WIDEST_MESSAGES.items():
            slot = self.fields[name]
            slot.show_error(message)
            tallest = max(tallest, self._measured_height())
            slot.invalid = False
            slot.shell.set_invalid(False)
            slot.reset_helper()
        return max(MIN_GEOMETRY[0], RAIL_WIDTH + 320), max(MIN_GEOMETRY[1], tallest)

    def _measured_height(self):
        self.root.update_idletasks()
        return (
            self.header.winfo_reqheight()
            + self.rail.winfo_reqheight()
            + self.statusbar.winfo_reqheight()
            + 2
        )

    # -- construction ----------------------------------------------------
    def _build_ui(self):
        self._build_header()
        self._hairline(row=1)
        main = tk.Frame(self.root, bg=COLORS["bg_app"])
        main.grid(row=2, column=0, sticky="nsew")
        main.grid_rowconfigure(0, weight=1)
        main.grid_columnconfigure(0, minsize=RAIL_WIDTH)
        main.grid_columnconfigure(2, weight=1)
        self._build_rail(main)
        tk.Frame(main, bg=COLORS["border_hairline"], width=1).grid(
            row=0, column=1, sticky="ns"
        )
        self._build_report(main)
        self._hairline(row=3)
        self._build_statusbar()

    def _hairline(self, row):
        tk.Frame(self.root, bg=COLORS["border_hairline"], height=1).grid(
            row=row, column=0, sticky="ew"
        )

    def _build_header(self):
        header = tk.Frame(self.root, bg=COLORS["bg_app"])
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(3, weight=1)
        self.header = header

        logo = tk.Canvas(
            header, width=22, height=22, bg=COLORS["bg_app"], highlightthickness=0
        )
        logo.grid(row=0, column=0, padx=(SPACE["lg"], SPACE["sm"]), pady=SPACE["md"])
        logo.create_polygon(
            rounded_rect_points(0, 0, 22, 22, 5),
            fill=COLORS["accent"], outline=COLORS["accent"],
        )
        logo.create_text(11, 11, text="Tk", fill="#FFFFFF", font=self.fonts["small_bold"])
        tk.Label(
            header, text="Tkinter Designer", bg=COLORS["bg_app"],
            fg=COLORS["ink_primary"], font=self.fonts["body_bold"],
        ).grid(row=0, column=1, sticky="w")

        QuietButton(
            header, text="Guide ↗", fonts=self.fonts,
            command=lambda: webbrowser.open_new_tab(GUIDE_URL),
        ).grid(row=0, column=4, padx=(SPACE["sm"], SPACE["md"]))

    def _build_rail(self, parent):
        rail = tk.Frame(parent, bg=COLORS["bg_app"])
        rail.grid(row=0, column=0, sticky="nsew")
        rail.grid_columnconfigure(0, weight=1, minsize=RAIL_WIDTH - 2 * SPACE["lg"])
        self.rail = rail
        self.rail_body = tk.Frame(rail, bg=COLORS["bg_app"])
        self.rail_body.grid(
            row=0, column=0, sticky="nsew", padx=SPACE["lg"], pady=SPACE["md"]
        )
        self.rail_body.grid_columnconfigure(0, weight=1)
        rail.grid_rowconfigure(0, weight=1)

        self.row = 0
        self._build_source_section()
        self._build_output_section()
        self.rail_body.grid_rowconfigure(self.row, weight=1, minsize=SPACE["sm"])
        self.row += 1
        self._build_actions()

    def _place(self, widget, *, pady=(0, 0), sticky="ew"):
        widget.grid(row=self.row, column=0, sticky=sticky, pady=pady)
        self.row += 1
        return widget

    def _build_source_section(self):
        body = self.rail_body
        self._place(section_header(body, "SOURCE", self.fonts), pady=(0, SPACE["sm"]))
        self._place(field_label(body, "Figma design URL", self.fonts), pady=(0, SPACE["xs"]))
        self.fields["url"] = self._text_field(
            self.url, placeholder="https://www.figma.com/design/…"
        )
        self._place(
            field_label(body, "Personal access token", self.fonts),
            pady=(SPACE["md"], SPACE["xs"]),
        )
        self.fields["token"] = self._token_field()

    def _build_output_section(self):
        body = self.rail_body
        self._place(
            section_header(body, "OUTPUT", self.fonts), pady=(SPACE["xl"], SPACE["sm"])
        )
        self._place(field_label(body, "Output folder", self.fonts), pady=(0, SPACE["xs"]))
        self.fields["output"] = self._folder_field()
        self.output.trace_add("write", lambda *_a: self._refresh_output_helper())
        self._refresh_output_helper()

        self._place(
            field_label(body, "Code style", self.fonts), pady=(SPACE["md"], SPACE["xs"])
        )
        self.template_control = self._place(
            SegmentedControl(
                body, variable=self.template,
                values=("script", "class", "pages"), fonts=self.fonts,
            )
        )
        self._place(
            field_label(body, "Generated app theme", self.fonts),
            pady=(SPACE["md"], SPACE["xs"]),
        )
        self.theme_control = self._place(
            ChoiceMenu(
                body, variable=self.theme,
                values=("clam", "alt", "default", "classic"), fonts=self.fonts,
            )
        )

    def _helper(self):
        return tk.Label(
            self.rail_body, text="", bg=COLORS["bg_app"], fg=COLORS["ink_muted"],
            font=self.fonts["small"], anchor="w", justify="left",
            wraplength=RAIL_WIDTH - 2 * SPACE["lg"],
        )

    def _text_field(self, variable, *, placeholder=None):
        shell = self._place(InputShell(self.rail_body))
        entry = make_entry(shell.body, variable, self.fonts)
        entry.pack(fill="both", expand=True, padx=9, pady=4)
        shell.track(entry)
        if placeholder:
            Placeholder(entry, variable, placeholder, self.fonts)
        helper = self._place(self._helper(), pady=(SPACE["xs"], 0))
        helper.grid_remove()
        slot = FieldSlot(shell, entry, helper)
        entry.bind("<Key>", lambda _event: slot.clear_error(), add="+")
        return slot

    def _token_field(self):
        shell = self._place(InputShell(self.rail_body))
        entry = make_entry(shell.body, self.token, self.fonts, show="•")
        entry.pack(side="left", fill="both", expand=True, padx=(9, 0), pady=4)
        shell.track(entry)
        self.token_toggle = QuietButton(
            shell.body, text="Show", fonts=self.fonts,
            command=self._toggle_token, background=COLORS["bg_surface"],
        )
        self.token_toggle.pack(side="right", padx=(0, 4))
        shell.track(self.token_toggle)
        helper = self._place(self._helper(), pady=(SPACE["xs"], 0))
        default = "Loaded from FIGMA_TOKEN" if self.token_from_env else ""
        slot = FieldSlot(shell, entry, helper, default_helper=default)
        slot.reset_helper()
        entry.bind("<Key>", lambda _event: slot.clear_error(), add="+")
        return slot

    def _folder_field(self):
        shell = self._place(InputShell(self.rail_body))
        entry = make_entry(shell.body, self.output, self.fonts, role="mono")
        entry.pack(side="left", fill="both", expand=True, padx=(9, 0), pady=4)
        shell.track(entry)
        tk.Frame(shell.body, bg=COLORS["border_hairline"], width=1).pack(
            side="right", fill="y"
        )
        self.browse_button = QuietButton(
            shell.body, text="Browse…", fonts=self.fonts,
            command=self._choose_output, background=COLORS["bg_inset"],
        )
        self.browse_button.configure(padx=12, pady=6)
        self.browse_button.pack(side="right", fill="y")
        shell.track(self.browse_button)
        helper = self._place(self._helper(), pady=(SPACE["xs"], 0))
        slot = FieldSlot(shell, entry, helper)
        entry.bind("<Key>", lambda _event: slot.clear_error(), add="+")
        return slot

    def _build_actions(self):
        self.inspect_button = self._place(
            CanvasButton(
                self.rail_body, text="Inspect design", fonts=self.fonts,
                hint=self.shortcuts["inspect"][1], variant="secondary", height=32,
                command=lambda: self._start("inspect"),
            ),
            pady=(0, SPACE["sm"]),
        )
        self.generate_button = self._place(
            CanvasButton(
                self.rail_body, text="Generate project", fonts=self.fonts,
                hint=self.shortcuts["generate"][1], variant="primary", height=36,
                command=lambda: self._start("generate"),
            )
        )

    def _build_report(self, parent):
        pane = tk.Frame(parent, bg=COLORS["bg_surface"])
        pane.grid(row=0, column=2, sticky="nsew")
        pane.grid_columnconfigure(0, weight=1)
        pane.grid_rowconfigure(1, weight=1)

        header = tk.Frame(pane, bg=COLORS["bg_surface"])
        header.grid(
            row=0, column=0, sticky="ew",
            padx=SPACE["lg"], pady=(SPACE["md"], SPACE["sm"]),
        )
        header.grid_columnconfigure(2, weight=1)
        tk.Label(
            header, text="Design report", bg=COLORS["bg_surface"],
            fg=COLORS["ink_primary"], font=self.fonts["title"],
        ).grid(row=0, column=0, sticky="w")
        self.report_chip = tk.Label(
            header, text="Not inspected", bg=COLORS["neutral_bg"],
            fg=COLORS["neutral_fg"], font=self.fonts["small_bold"], padx=7, pady=2,
        )
        self.report_chip.grid(row=0, column=1, padx=(SPACE["sm"], 0))
        self.copy_button = QuietButton(
            header, text="Copy report", fonts=self.fonts,
            command=self._copy_report, background=COLORS["bg_surface"],
        )
        self.copy_button.grid(row=0, column=3)
        self.copy_button.grid_remove()
        self.open_button = QuietButton(
            header, text="Open folder", fonts=self.fonts,
            command=self._open_output, background=COLORS["bg_surface"],
        )
        self.open_button.grid(row=0, column=4)
        self.open_button.grid_remove()

        body = tk.Frame(pane, bg=COLORS["bg_surface"])
        body.grid(row=1, column=0, sticky="nsew", padx=SPACE["lg"], pady=(0, SPACE["md"]))
        body.grid_rowconfigure(0, weight=1)
        body.grid_columnconfigure(0, weight=1)
        self.report = tk.Text(
            body, wrap="word", relief="flat", borderwidth=0, highlightthickness=0,
            bg=COLORS["bg_surface"], fg=COLORS["ink_secondary"], font=self.fonts["label"],
            padx=0, pady=0, cursor="arrow", state="disabled", takefocus=False,
            spacing2=2, width=1, height=1,
        )
        self.report.grid(row=0, column=0, sticky="nsew")
        self.scrollbar = tk.Scrollbar(body, command=self.report.yview, width=12)
        self.scrollbar.grid(row=0, column=1, sticky="ns", padx=(SPACE["xs"], 0))
        self.scrollbar.grid_remove()
        self.report.configure(yscrollcommand=self._sync_scrollbar)
        self._configure_report_tags()
        self._bind_report_scrolling()
        self.measure_overflow = 0
        self.report.bind("<Configure>", self._cap_prose_measure)
        self._render(report_view.empty_segments(self.shortcuts["inspect"][1]))

    def _configure_report_tags(self):
        for tag, style in report_view.TAG_STYLES.items():
            options = {}
            if "font" in style:
                options["font"] = self.fonts[style["font"]]
            if "fg" in style:
                options["foreground"] = COLORS[style["fg"]]
            if "bg" in style:
                options["background"] = COLORS[style["bg"]]
            for key in ("spacing1", "spacing3", "lmargin1", "lmargin2", "rmargin"):
                if key in style:
                    options[key] = style[key]
            self.report.tag_configure(tag, **options)

    def _cap_prose_measure(self, event):
        """Hold running prose to a readable measure as the pane widens.

        This only rewrites tag margins; the layout itself never reflows.
        """
        overflow = max(0, event.width - MAX_MEASURE)
        if overflow == self.measure_overflow:
            return
        self.measure_overflow = overflow
        for tag in report_view.PARAGRAPH_TAGS:
            self.report.tag_configure(tag, rmargin=overflow)

    def _bind_report_scrolling(self):
        self.report.bind("<MouseWheel>", self._on_wheel)
        self.report.bind("<Button-4>", self._on_wheel)
        self.report.bind("<Button-5>", self._on_wheel)

    def _build_statusbar(self):
        bar = tk.Frame(self.root, bg=COLORS["bg_app"])
        bar.grid(row=4, column=0, sticky="ew")
        bar.grid_columnconfigure(1, weight=1)
        self.statusbar = bar
        self.status_dot = StatusDot(bar)
        self.status_dot.grid(row=0, column=0, padx=(SPACE["lg"], SPACE["sm"]), pady=SPACE["sm"])
        tk.Label(
            bar, textvariable=self.status, bg=COLORS["bg_app"], fg=COLORS["ink_secondary"],
            font=self.fonts["label"], anchor="w",
        ).grid(row=0, column=1, sticky="w")
        self.progress = ProgressIndicator(bar)
        self.progress.grid(row=0, column=2, padx=(SPACE["sm"], SPACE["lg"]))
        self.progress.grid_remove()
        self.version_label = tk.Label(
            bar, text=f"v{__version__}", bg=COLORS["bg_app"], fg=COLORS["ink_muted"],
            font=self.fonts["small"],
        )
        self.version_label.grid(row=0, column=3, padx=(0, SPACE["lg"]))

    def _bind_shortcuts(self):
        bindings = {
            "inspect": lambda _event: self._start("inspect"),
            "generate": lambda _event: self._start("generate"),
            "browse": lambda _event: self._choose_output(),
            "copy": lambda _event: self._copy_report(),
        }
        for name, handler in bindings.items():
            self.root.bind_all(self.shortcuts[name][0], handler)
        for slot in self.fields.values():
            slot.entry.bind("<Return>", lambda _event: self._start("inspect"))

    # -- small helpers ---------------------------------------------------
    def _focus_first(self):
        if self.url.get().strip():
            self.inspect_button.focus_set()
        else:
            self.fields["url"].entry.focus_set()

    def _on_wheel(self, event):
        if event.num == 4:
            units = -3
        elif event.num == 5:
            units = 3
        elif abs(event.delta) >= 120:
            units = -event.delta // 120
        else:
            units = -event.delta
        self.report.yview_scroll(int(units), "units")
        return "break"

    def _sync_scrollbar(self, first, last):
        self.scrollbar.set(first, last)
        if float(first) <= 0.0 and float(last) >= 1.0:
            self.scrollbar.grid_remove()
        else:
            self.scrollbar.grid()

    def _show_output_tail(self):
        """Scroll the path entry to its leaf; the head is never the useful part."""
        self.fields["output"].entry.xview_moveto(1.0)

    def _refresh_output_helper(self):
        value = self.output.get().strip()
        name = Path(value).name if value else ""
        self.fields["output"].set_default_helper(
            f"Creates {name}/build" if name else ""
        )

    def _toggle_token(self):
        self.show_token.set(not self.show_token.get())
        self._apply_token_visibility()

    def _apply_token_visibility(self):
        revealed = self.show_token.get()
        self.fields["token"].entry.configure(show="" if revealed else "•")
        self.token_toggle.configure(text="Hide" if revealed else "Show")

    def _choose_output(self):
        if self.working:
            return
        selected = filedialog.askdirectory(
            initialdir=self.output.get() or str(Path.cwd())
        )
        if selected:
            self.output.set(selected)
            self.fields["output"].clear_error()
            self._show_output_tail()

    def _copy_report(self):
        if not self.report_text:
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(self.report_text)
        self._set_status("success", "Report copied to the clipboard")

    def _open_output(self):
        path = self.generated_path
        if not path:
            return
        try:
            if sys.platform == "darwin":
                subprocess.Popen(["open", str(path)])
            elif os.name == "nt":
                os.startfile(str(path))  # noqa: S606 - platform file manager
            else:
                subprocess.Popen(["xdg-open", str(path)])
        except OSError as exc:
            self._set_status("danger", f"Could not open the folder: {exc}")

    # -- report rendering -------------------------------------------------
    def _render(self, segments, append=False):
        self.report.configure(state="normal")
        if not append:
            self.report.delete("1.0", "end")
        for tag, text in segments:
            self.report.insert("end", text, (tag,) if tag else ())
        self.report.configure(state="disabled")
        if append:
            self.report.see("end")
        else:
            self.report.yview_moveto(0.0)

    def _set_chip(self, text, tone):
        palette = {
            "neutral": (COLORS["neutral_bg"], COLORS["neutral_fg"]),
            "info": (COLORS["info_bg"], COLORS["accent_hover"]),
            "success": (COLORS["success_bg"], COLORS["success"]),
            "danger": (COLORS["danger_bg"], COLORS["danger"]),
        }
        background, foreground = palette[tone]
        self.report_chip.configure(text=text, bg=background, fg=foreground)

    def _set_status(self, tone, message):
        self.status_dot.set_tone(tone)
        self.status.set(message)

    # -- validation and workflow -----------------------------------------
    def _inputs(self):
        if not self.url.get().strip():
            raise FieldError("url", MISSING_URL)
        try:
            reference = parse_figma_url(self.url.get())
        except ValueError as exc:
            raise FieldError("url", INVALID_URL) from exc
        token = self.token.get().strip()
        if not token:
            raise FieldError("token", MISSING_TOKEN)
        raw_output = self.output.get().strip()
        if not raw_output:
            raise FieldError("output", MISSING_OUTPUT)
        try:
            output = Path(raw_output).expanduser().resolve()
        except OSError as exc:
            raise FieldError("output", str(exc)) from exc
        return reference, token, output

    def _report_invalid(self, error):
        slot = self.fields[error.field]
        slot.show_error(str(error))
        slot.entry.focus_set()
        self._set_status("danger", str(error))

    def _confirm_replacement(self, build_path):
        if not (build_path.is_dir() and any(build_path.iterdir())):
            return True, False
        replace = messagebox.askyesno(
            "Replace existing build?",
            "The build folder is not empty. It will only be replaced after "
            "the new project generates successfully.",
        )
        return replace, replace

    def _start(self, operation):
        if self.working:
            return
        try:
            reference, token, output = self._inputs()
        except FieldError as error:
            self._report_invalid(error)
            return

        clean = False
        build_path = output / "build"
        if operation == "generate":
            proceed, clean = self._confirm_replacement(build_path)
            if not proceed:
                return

        self._set_working(True, operation)
        worker = threading.Thread(
            target=self._run_operation,
            args=(
                operation, reference, token, build_path, clean,
                self.template.get(), self.theme.get().strip(),
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
                self.events.put(("inspected", report, "Inspection complete"))
            else:
                result = designer.design(clean=clean)
                self.events.put(("generated", result, "Generation complete"))
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
            self._set_working(False, None)
            handlers = {
                "inspected": self._handle_inspected,
                "generated": self._handle_generated,
                "error": self._handle_error,
            }
            handlers[event](detail, status)
        self.root.after(100, self._poll_events)

    def _handle_inspected(self, report, _status):
        self.report_text = report.to_text()
        self.last_report = report.to_dict()
        self._render(report_view.inspection_segments(self.last_report))
        self._set_chip("Inspected", "success")
        self.copy_button.grid()
        summary = (
            f"{len(report.frames)} frames · {report.element_count} elements · "
            f"{report.image_export_count} image exports"
        )
        self._set_status("success", f"Inspection complete · {summary}")
        self.generate_button.focus_set()

    def _handle_generated(self, result, _status):
        self.generated_path = result.output_path
        if result.report is not None:
            self.report_text = result.report.to_text()
            self.last_report = result.report.to_dict()
            self._render(report_view.inspection_segments(self.last_report))
        self._render(
            report_view.generation_segments(
                str(result.output_path), len(result.code_files), len(result.asset_files)
            ),
            append=result.report is not None,
        )
        self._set_chip("Generated", "success")
        self.copy_button.grid()
        self.open_button.grid()
        self._set_status(
            "success", f"Generated · {middle_truncate(str(result.output_path))}"
        )

    def _handle_error(self, message, status):
        self._render(report_view.error_segments(message, self.last_report))
        self._set_chip("Failed", "danger")
        self._set_status("danger", status)
        self.inspect_button.focus_set()

    # -- busy state -------------------------------------------------------
    def _lockable(self):
        return (
            self.fields["url"].entry,
            self.fields["token"].entry,
            self.fields["output"].entry,
        )

    def _set_working(self, working, operation):
        self.working = working
        for entry in self._lockable():
            entry.configure(
                state="readonly" if working else "normal",
                fg=COLORS["ink_secondary"] if working else COLORS["ink_primary"],
            )
        for shell in (slot.shell for slot in self.fields.values()):
            shell.set_enabled(not working)
        self.token_toggle.set_surface(
            COLORS["bg_inset"] if working else COLORS["bg_surface"]
        )
        for control in (
            self.token_toggle, self.browse_button, self.template_control,
            self.theme_control, self.inspect_button, self.generate_button,
        ):
            control.set_enabled(not working)

        if working:
            self.show_token.set(False)
            self._apply_token_visibility()
            inspecting = operation == "inspect"
            self.inspect_button.set_text("Inspecting…" if inspecting else "Inspect design")
            self.generate_button.set_text(
                "Generate project" if inspecting else "Generating…"
            )
            self._set_chip("Working…", "info")
            if self.last_report is None:
                self._render(report_view.working_segments(operation))
            self._set_status(
                "working",
                "Contacting Figma…" if inspecting else "Generating project…",
            )
            self.version_label.grid_remove()
            self.progress.grid()
            self.progress.start()
        else:
            self.progress.stop()
            self.progress.grid_remove()
            self.version_label.grid()
            self.inspect_button.set_text("Inspect design")
            self.generate_button.set_text("Generate project")


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
