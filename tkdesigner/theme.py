"""Design tokens for the desktop application.

Colors, spacing, and type roles live here so the workspace, the reusable
widgets, and the report renderer cannot drift apart. Nothing in this module
imports Tkinter, which keeps the tokens testable without a display.
"""

COLORS = {
    # Surfaces
    "bg_app": "#FAFAFB",
    "bg_surface": "#FFFFFF",
    "bg_inset": "#F2F4F7",
    "bg_hover": "#ECEEF1",
    "bg_pressed": "#E4E7EC",
    # Ink
    "ink_primary": "#1A1D23",
    "ink_secondary": "#52596A",
    "ink_muted": "#8A91A0",
    "ink_disabled": "#98A2B3",
    # Lines
    "border_hairline": "#E4E7EC",
    "border_control": "#C6CBD4",
    # Accent
    "accent": "#2867E8",
    "accent_hover": "#1F58CB",
    "accent_pressed": "#1949AC",
    "accent_hint": "#A8C0F5",
    "focus": "#155EEF",
    # Feedback
    "success": "#17803D",
    "success_bg": "#E8F5EC",
    "warn": "#B54708",
    "warn_bg": "#FCEBDB",
    "danger": "#C0362C",
    "danger_bg": "#FDECEA",
    "info_bg": "#E8EEFC",
    "neutral_bg": "#EEF1F5",
    "neutral_fg": "#667085",
    "disabled_fill": "#E9EBEF",
}

# The only spacing values the interface is allowed to use.
SPACE = {"xs": 4, "sm": 8, "md": 12, "lg": 16, "xl": 24}

# Fixed geometry, in pixels.
RAIL_WIDTH = 324
DEFAULT_GEOMETRY = (920, 640)
MIN_GEOMETRY = (800, 560)
# Longest comfortable line for running prose in the report pane. Wider windows
# give their extra width to margin rather than to unreadable line lengths.
MAX_MEASURE = 660

# Point sizes per type role. Weight is limited to normal/bold by Tk.
TYPE_SCALE = {
    "title": (13, "bold"),
    "body_bold": (11, "bold"),
    "body": (11, "normal"),
    "label": (10, "normal"),
    "label_bold": (10, "bold"),
    "small": (9, "normal"),
    "small_bold": (9, "bold"),
}

# Roles that must render in the fixed-width family.
MONO_SCALE = {"mono": (10, "normal"), "mono_small": (9, "normal")}


def build_fonts(family: str, fixed_family: str) -> dict:
    """Return the full role -> font tuple mapping for one platform's fonts."""
    fonts = {
        role: (family, size) if weight == "normal" else (family, size, weight)
        for role, (size, weight) in TYPE_SCALE.items()
    }
    fonts.update({
        role: (fixed_family, size)
        for role, (size, _weight) in MONO_SCALE.items()
    })
    return fonts


def shortcut_labels(platform: str) -> dict:
    """Return the modifier bindings and their printable hints for a platform."""
    if platform == "darwin":
        return {
            "inspect": ("<Command-i>", "⌘I"),
            "generate": ("<Command-Return>", "⌘↩"),
            "browse": ("<Command-o>", "⌘O"),
            "copy": ("<Command-Shift-KeyPress-C>", "⌘⇧C"),
        }
    return {
        "inspect": ("<Control-i>", "Ctrl+I"),
        "generate": ("<Control-Return>", "Ctrl+↩"),
        "browse": ("<Control-o>", "Ctrl+O"),
        "copy": ("<Control-Shift-KeyPress-C>", "Ctrl+Shift+C"),
    }
