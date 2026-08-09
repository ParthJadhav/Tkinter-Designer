"""Reusable desktop controls built from plain Tkinter primitives.

Every control here paints its own rest/hover/pressed/focused/disabled states so
the interface looks the same on macOS, Windows, and Linux instead of inheriting
three different native themes. Rounded corners exist only where a control is
drawn on a `tk.Canvas`; everything else is an honest rectangle.
"""

import math
import tkinter as tk

from .theme import COLORS


def rounded_rect_points(x0, y0, x1, y1, radius, steps=6):
    """Return polygon points tracing a rectangle with rounded corners.

    Tk has no rounded rectangle. A smoothed polygon distorts the straight
    edges, so the arcs are sampled explicitly and the polygon is drawn crisp.
    """
    radius = max(0, min(radius, (x1 - x0) / 2, (y1 - y0) / 2))
    if radius <= 0:
        return [x0, y0, x1, y0, x1, y1, x0, y1]

    corners = (
        (x1 - radius, y1 - radius, 0),
        (x0 + radius, y1 - radius, 90),
        (x0 + radius, y0 + radius, 180),
        (x1 - radius, y0 + radius, 270),
    )
    points = []
    for center_x, center_y, start in corners:
        for step in range(steps + 1):
            angle = math.radians(start + (90 * step / steps))
            points.extend((
                center_x + radius * math.cos(angle),
                center_y + radius * math.sin(angle),
            ))
    return points


class CanvasButton(tk.Canvas):
    """A rounded action button with a label and an optional shortcut hint."""

    RADIUS = 6

    def __init__(self, parent, *, text, command, fonts, hint="", variant="primary", height=36):
        super().__init__(
            parent,
            # width must be given; an unsized Canvas claims a ~378px default and
            # would silently widen whatever column it sits in.
            width=1,
            height=height,
            bg=COLORS["bg_app"],
            highlightthickness=0,
            takefocus=True,
            cursor="hand2",
        )
        self.command = command
        self.variant = variant
        self.fonts = fonts
        self.label = text
        self.hint = hint
        self.enabled = True
        self.state = "rest"
        self.focused = False
        self._items = []

        self.bind("<Configure>", lambda _event: self._draw())
        self.bind("<Enter>", lambda _event: self._set_state("hover"))
        self.bind("<Leave>", lambda _event: self._set_state("rest"))
        self.bind("<ButtonPress-1>", lambda _event: self._set_state("pressed"))
        self.bind("<ButtonRelease-1>", self._release)
        self.bind("<FocusIn>", lambda _event: self._set_focus(True))
        self.bind("<FocusOut>", lambda _event: self._set_focus(False))
        self.bind("<Return>", self._activate)
        self.bind("<space>", self._activate)

    # -- appearance ------------------------------------------------------
    def _colors(self):
        if not self.enabled:
            if self.variant == "primary":
                return COLORS["disabled_fill"], "", COLORS["ink_disabled"]
            return "#F4F6F8", COLORS["border_hairline"], COLORS["ink_disabled"]
        if self.variant == "primary":
            fill = {
                "rest": COLORS["accent"],
                "hover": COLORS["accent_hover"],
                "pressed": COLORS["accent_pressed"],
            }[self.state]
            return fill, "", "#FFFFFF"
        fill = {
            "rest": COLORS["bg_surface"],
            "hover": "#F4F6F8",
            "pressed": COLORS["bg_hover"],
        }[self.state]
        outline = COLORS["focus"] if self.focused else COLORS["border_control"]
        return fill, outline, COLORS["ink_primary"]

    def _draw(self):
        self.delete("all")
        width = self.winfo_width()
        height = self.winfo_height()
        if width <= 1 or height <= 1:
            return
        fill, outline, text_color = self._colors()
        points = rounded_rect_points(0.5, 0.5, width - 0.5, height - 0.5, self.RADIUS)
        self.create_polygon(
            points, fill=fill, outline=outline or fill, width=1, joinstyle="round"
        )
        if self.focused and self.variant == "primary" and self.enabled:
            inner = rounded_rect_points(2.5, 2.5, width - 2.5, height - 2.5, self.RADIUS - 2)
            self.create_polygon(
                inner, fill="", outline=COLORS["accent_pressed"], width=1, joinstyle="round"
            )
        self.create_text(
            14, height / 2, text=self.label, anchor="w",
            fill=text_color, font=self.fonts["body_bold"],
        )
        if self.hint and self.enabled:
            hint_color = (
                COLORS["accent_hint"] if self.variant == "primary" else COLORS["ink_muted"]
            )
            self.create_text(
                width - 14, height / 2, text=self.hint, anchor="e",
                fill=hint_color, font=self.fonts["small"],
            )

    def _set_state(self, state):
        if self.enabled and self.state != state:
            self.state = state
            self._draw()

    def _set_focus(self, focused):
        self.focused = focused
        self._draw()

    # -- behavior --------------------------------------------------------
    def _release(self, _event=None):
        if not self.enabled:
            return
        self._set_state("hover")
        self.focus_set()
        self.command()

    def _activate(self, _event=None):
        if self.enabled:
            self.command()
        return "break"

    def set_text(self, text):
        self.label = text
        self._draw()

    def set_enabled(self, enabled):
        self.enabled = enabled
        self.state = "rest"
        self.configure(cursor="hand2" if enabled else "arrow", takefocus=bool(enabled))
        self._draw()


class QuietButton(tk.Label):
    """A borderless text action for secondary affordances."""

    def __init__(self, parent, *, text, command, fonts, background=None):
        self.background = background or COLORS["bg_app"]
        self.command = command
        self.enabled = True
        super().__init__(
            parent,
            text=text,
            bg=self.background,
            fg=COLORS["ink_secondary"],
            font=fonts["small_bold"],
            padx=8,
            pady=4,
            cursor="hand2",
            takefocus=True,
            highlightthickness=1,
            highlightbackground=self.background,
            highlightcolor=COLORS["focus"],
        )
        self.bind("<Enter>", lambda _event: self._paint(COLORS["bg_inset"], COLORS["ink_primary"]))
        self.bind("<Leave>", lambda _event: self._paint(self.background, COLORS["ink_secondary"]))
        self.bind("<ButtonPress-1>", lambda _event: self._paint(COLORS["bg_pressed"], COLORS["ink_primary"]))
        self.bind("<ButtonRelease-1>", self._release)
        self.bind("<Return>", self._release)
        self.bind("<space>", self._release)

    def _paint(self, background, foreground):
        if self.enabled:
            self.configure(bg=background, fg=foreground)

    def _release(self, _event=None):
        if self.enabled:
            self.focus_set()
            self.command()
        return "break"

    def set_surface(self, color):
        """Follow the surrounding surface, e.g. a field going readonly."""
        self.background = color
        self.configure(bg=color, highlightbackground=color)

    def set_enabled(self, enabled):
        self.enabled = enabled
        self.configure(
            bg=self.background,
            fg=COLORS["ink_secondary"] if enabled else COLORS["ink_disabled"],
            cursor="hand2" if enabled else "arrow",
            takefocus=bool(enabled),
        )


class InputShell(tk.Frame):
    """A 1px border that owns rest, focus, invalid, and disabled coloring."""

    def __init__(self, parent):
        super().__init__(parent, bg=COLORS["border_control"])
        self.invalid = False
        self.focused = False
        self.enabled = True
        self.body = tk.Frame(self, bg=COLORS["bg_surface"])
        self.body.pack(fill="both", expand=True, padx=1, pady=1)

    def _repaint(self):
        if not self.enabled:
            border = COLORS["border_hairline"]
        elif self.invalid:
            border = COLORS["danger"]
        elif self.focused:
            border = COLORS["focus"]
        else:
            border = COLORS["border_control"]
        self.configure(bg=border)
        surface = COLORS["bg_surface"] if self.enabled else COLORS["bg_inset"]
        self.body.configure(bg=surface)
        return surface

    def track(self, widget):
        """Mirror one child widget's focus into the shell border."""
        widget.bind("<FocusIn>", lambda _event: self.set_focused(True), add="+")
        widget.bind("<FocusOut>", lambda _event: self.set_focused(False), add="+")

    def set_focused(self, focused):
        self.focused = focused
        self._repaint()

    def set_invalid(self, invalid):
        self.invalid = invalid
        self._repaint()

    def set_enabled(self, enabled):
        self.enabled = enabled
        self._repaint()


def make_entry(parent, variable, fonts, *, role="body", show=None):
    """Return an unadorned entry; the surrounding `InputShell` draws the border."""
    return tk.Entry(
        parent,
        textvariable=variable,
        show=show,
        relief="flat",
        borderwidth=0,
        highlightthickness=0,
        bg=COLORS["bg_surface"],
        fg=COLORS["ink_primary"],
        disabledbackground=COLORS["bg_inset"],
        disabledforeground=COLORS["ink_disabled"],
        readonlybackground=COLORS["bg_inset"],
        insertbackground=COLORS["ink_primary"],
        selectbackground=COLORS["accent"],
        selectforeground="#FFFFFF",
        font=fonts[role],
    )


class Placeholder:
    """Grey hint text shown over an empty, unfocused entry."""

    def __init__(self, entry, variable, text, fonts):
        self.entry = entry
        self.variable = variable
        self.label = tk.Label(
            entry.master,
            text=text,
            bg=COLORS["bg_surface"],
            fg=COLORS["ink_muted"],
            font=fonts["body"],
            anchor="w",
        )
        self.label.bind("<Button-1>", lambda _event: entry.focus_set())
        entry.bind("<FocusIn>", lambda _event: self.refresh(True), add="+")
        entry.bind("<FocusOut>", lambda _event: self.refresh(False), add="+")
        variable.trace_add("write", lambda *_args: self.refresh(None))
        self.refresh(False)

    def refresh(self, focused):
        if focused is None:
            focused = self.entry.focus_get() is self.entry
        if self.variable.get() or focused or str(self.entry["state"]) != "normal":
            self.label.place_forget()
        else:
            self.label.place(in_=self.entry, x=0, y=0, relheight=1.0, relwidth=1.0)


class SegmentedControl(tk.Frame):
    """A single-tab-stop choice control that keeps every option visible."""

    def __init__(self, parent, *, variable, values, fonts, command=None):
        super().__init__(
            parent,
            bg=COLORS["border_control"],
            takefocus=True,
            highlightthickness=0,
        )
        self.variable = variable
        self.values = tuple(values)
        self.fonts = fonts
        self.command = command
        self.enabled = True
        self.segments = {}

        body = tk.Frame(self, bg=COLORS["border_hairline"])
        body.pack(fill="both", expand=True, padx=1, pady=1)
        for index, value in enumerate(self.values):
            body.grid_columnconfigure(index * 2, weight=1, uniform="segment")
            cell = tk.Frame(body, bg=COLORS["bg_inset"])
            cell.grid(row=0, column=index * 2, sticky="nsew")
            label = tk.Label(
                cell, text=value, bg=COLORS["bg_inset"], fg=COLORS["ink_secondary"],
                font=fonts["label"], pady=5, cursor="hand2",
            )
            label.pack(fill="both", expand=True)
            underline = tk.Frame(cell, bg=COLORS["bg_inset"], height=2)
            underline.pack(fill="x", side="bottom")
            self.segments[value] = (cell, label, underline)
            for widget in (cell, label):
                widget.bind("<Button-1>", lambda _event, choice=value: self.select(choice))
                widget.bind("<Enter>", lambda _event, choice=value: self._hover(choice, True))
                widget.bind("<Leave>", lambda _event, choice=value: self._hover(choice, False))
            if index < len(self.values) - 1:
                tk.Frame(body, bg=COLORS["border_hairline"], width=1).grid(
                    row=0, column=index * 2 + 1, sticky="ns"
                )

        self.bind("<FocusIn>", lambda _event: self._focus_border(True))
        self.bind("<FocusOut>", lambda _event: self._focus_border(False))
        self.bind("<Left>", lambda _event: self._step(-1))
        self.bind("<Right>", lambda _event: self._step(1))
        variable.trace_add("write", lambda *_args: self._repaint())
        self._repaint()

    def _focus_border(self, focused):
        self.configure(bg=COLORS["focus"] if focused else COLORS["border_control"])

    def _hover(self, value, entering):
        if not self.enabled or value == self.variable.get():
            return
        cell, label, underline = self.segments[value]
        background = COLORS["bg_hover"] if entering else COLORS["bg_inset"]
        for widget in (cell, label, underline):
            widget.configure(bg=background)

    def _step(self, delta):
        if not self.enabled:
            return "break"
        try:
            index = self.values.index(self.variable.get())
        except ValueError:
            index = 0
        self.select(self.values[(index + delta) % len(self.values)])
        return "break"

    def select(self, value):
        if self.enabled and value in self.segments:
            self.focus_set()
            self.variable.set(value)
            if self.command:
                self.command(value)

    def _repaint(self):
        current = self.variable.get()
        for value, (cell, label, underline) in self.segments.items():
            selected = value == current
            if not self.enabled:
                # Values stay legible while working; only the unchosen options
                # recede. A fully dimmed control reads as broken, not busy.
                foreground = (
                    COLORS["ink_secondary"] if selected else COLORS["ink_disabled"]
                )
                background = COLORS["bg_inset"]
            elif selected:
                background, foreground = COLORS["bg_surface"], COLORS["ink_primary"]
            else:
                background, foreground = COLORS["bg_inset"], COLORS["ink_secondary"]
            cell.configure(bg=background)
            label.configure(
                bg=background, fg=foreground,
                font=self.fonts["label_bold"] if selected else self.fonts["label"],
            )
            if not selected:
                underline.configure(bg=background)
            else:
                underline.configure(
                    bg=COLORS["accent"] if self.enabled else COLORS["border_control"]
                )

    def set_enabled(self, enabled):
        self.enabled = enabled
        cursor = "hand2" if enabled else "arrow"
        for _cell, label, _underline in self.segments.values():
            label.configure(cursor=cursor)
        self.configure(takefocus=bool(enabled))
        self._repaint()


class ChoiceMenu(tk.Frame):
    """A collapsed menu that delegates the option list to Tk."""

    def __init__(self, parent, *, variable, values, fonts):
        super().__init__(parent, bg=COLORS["border_control"], takefocus=True)
        self.variable = variable
        self.enabled = True
        body = tk.Frame(self, bg=COLORS["bg_surface"])
        body.pack(fill="both", expand=True, padx=1, pady=1)

        self.menu = tk.Menu(
            self, tearoff=False, bg=COLORS["bg_surface"], fg=COLORS["ink_primary"],
            activebackground=COLORS["accent"], activeforeground="#FFFFFF", font=fonts["body"],
        )
        for value in values:
            self.menu.add_radiobutton(label=value, value=value, variable=variable)

        self.value_label = tk.Label(
            body, textvariable=variable, anchor="w", bg=COLORS["bg_surface"],
            fg=COLORS["ink_primary"], font=fonts["body"], padx=10, pady=6, cursor="hand2",
        )
        self.value_label.pack(side="left", fill="both", expand=True)
        # height must be given explicitly; an unsized Canvas defaults to ~264px.
        self.chevron = tk.Canvas(
            body, width=28, height=1, bg=COLORS["bg_surface"],
            highlightthickness=0, cursor="hand2",
        )
        self.chevron.pack(side="right", fill="y")
        self.chevron.bind("<Configure>", lambda _event: self._draw_chevron())

        self.body = body
        for widget in (self, body, self.value_label, self.chevron):
            widget.bind("<Button-1>", self._open)
        self.bind("<FocusIn>", lambda _event: self._focus_border(True))
        self.bind("<FocusOut>", lambda _event: self._focus_border(False))
        for sequence in ("<Return>", "<space>", "<Down>"):
            self.bind(sequence, self._open)

    def _draw_chevron(self):
        self.chevron.delete("all")
        width = self.chevron.winfo_width()
        height = self.chevron.winfo_height()
        if width <= 1 or height <= 1:
            return
        center_x, center_y = width / 2, height / 2
        color = COLORS["ink_muted"] if self.enabled else COLORS["ink_disabled"]
        self.chevron.create_line(
            center_x - 5, center_y - 2, center_x, center_y + 3, center_x + 5, center_y - 2,
            fill=color, width=2, capstyle="round", joinstyle="round",
        )

    def _focus_border(self, focused):
        self.configure(bg=COLORS["focus"] if focused else COLORS["border_control"])

    def _open(self, _event=None):
        if not self.enabled:
            return "break"
        self.focus_set()
        try:
            self.menu.tk_popup(self.winfo_rootx(), self.winfo_rooty() + self.winfo_height())
        finally:
            self.menu.grab_release()
        return "break"

    def set_enabled(self, enabled):
        self.enabled = enabled
        surface = COLORS["bg_surface"] if enabled else COLORS["bg_inset"]
        foreground = COLORS["ink_primary"] if enabled else COLORS["ink_secondary"]
        cursor = "hand2" if enabled else "arrow"
        self.body.configure(bg=surface)
        self.value_label.configure(bg=surface, fg=foreground, cursor=cursor)
        self.chevron.configure(bg=surface, cursor=cursor)
        self.configure(takefocus=bool(enabled))
        self._draw_chevron()


class ProgressIndicator(tk.Canvas):
    """An indeterminate sweep; the Figma fetch reports no real progress."""

    WIDTH = 120
    SWEEP = 28

    def __init__(self, parent):
        super().__init__(
            parent, width=self.WIDTH, height=4, bg=COLORS["bg_app"], highlightthickness=0
        )
        self.running = False
        self.position = 0
        self.after_id = None
        self.create_rectangle(0, 0, self.WIDTH, 4, fill=COLORS["border_hairline"], outline="")
        self.bar = self.create_rectangle(
            -self.SWEEP, 0, 0, 4, fill=COLORS["accent"], outline=""
        )

    def start(self):
        if not self.running:
            self.running = True
            self.position = 0
            self._tick()

    def stop(self):
        self.running = False
        if self.after_id is not None:
            self.after_cancel(self.after_id)
            self.after_id = None
        self.coords(self.bar, -self.SWEEP, 0, 0, 4)

    def _tick(self):
        if not self.running:
            return
        self.position = (self.position + 4) % (self.WIDTH + self.SWEEP)
        left = self.position - self.SWEEP
        self.coords(self.bar, left, 0, left + self.SWEEP, 4)
        self.after_id = self.after(30, self._tick)


class StatusDot(tk.Canvas):
    """An 8px state light for the status strip."""

    TONES = {
        "idle": COLORS["ink_disabled"],
        "working": COLORS["accent"],
        "success": COLORS["success"],
        "danger": COLORS["danger"],
    }

    def __init__(self, parent):
        super().__init__(parent, width=8, height=8, bg=COLORS["bg_app"], highlightthickness=0)
        self.dot = self.create_oval(0, 0, 8, 8, fill=self.TONES["idle"], outline="")

    def set_tone(self, tone):
        self.itemconfigure(self.dot, fill=self.TONES[tone])


def section_header(parent, text, fonts, background=None):
    """Return an overline label followed by a hairline rule."""
    background = background or COLORS["bg_app"]
    holder = tk.Frame(parent, bg=background)
    tk.Label(
        holder, text=text, bg=background, fg=COLORS["ink_muted"], font=fonts["small_bold"]
    ).pack(side="left")
    tk.Frame(holder, bg=COLORS["border_hairline"], height=1).pack(
        side="left", fill="x", expand=True, padx=(8, 0)
    )
    return holder


def field_label(parent, text, fonts, background=None):
    """Return the standard label that sits above a control."""
    return tk.Label(
        parent,
        text=text,
        bg=background or COLORS["bg_app"],
        fg=COLORS["ink_secondary"],
        font=fonts["label"],
        anchor="w",
    )
