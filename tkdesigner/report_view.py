"""Turn inspection and generation results into a styled report document.

The report is plain prose with a small amount of typographic hierarchy: a title,
a line of counts, one block per frame, and a list of warnings. Colour and weight
carry the structure; there are no badges, boxes, or rules.

This module imports nothing from Tkinter, so the document can be asserted in
tests without a display. `DesignReport.to_text` stays the canonical plain-text
form for the CLI and for "Copy report".
"""

from typing import List, NamedTuple, Optional, Sequence


class Segment(NamedTuple):
    """One run of text and the style tag it renders with."""

    tag: Optional[str]
    text: str


# tag -> style. `font` names a role from `theme.build_fonts`.
TAG_STYLES = {
    "h1": {"font": "title", "fg": "ink_primary", "spacing3": 2},
    "meta": {"font": "label", "fg": "ink_muted"},
    "meta_mono": {"font": "mono_small", "fg": "ink_muted"},
    "counts": {"font": "label", "fg": "ink_secondary", "spacing1": 8},
    "section": {"font": "small_bold", "fg": "ink_muted", "spacing1": 24, "spacing3": 4},
    "frame_name": {"font": "body_bold", "fg": "ink_primary", "spacing1": 14},
    "frame_dim": {"font": "mono_small", "fg": "ink_muted", "spacing1": 14},
    "frame_kinds": {
        "font": "label", "fg": "ink_muted",
        "spacing1": 2, "lmargin1": 16, "lmargin2": 16,
    },
    "warn_text": {
        "font": "label", "fg": "warn",
        "spacing1": 6, "lmargin1": 16, "lmargin2": 16,
    },
    "ok_text": {"font": "label", "fg": "success", "spacing1": 6},
    "err_text": {"font": "body_bold", "fg": "danger", "spacing1": 2},
    "hint_text": {"font": "label", "fg": "ink_secondary", "spacing1": 6},
    "path": {"font": "mono", "fg": "ink_primary", "spacing1": 6},
    "empty_h": {"font": "body_bold", "fg": "ink_secondary", "spacing3": 6},
    "empty_b": {"font": "label", "fg": "ink_muted", "spacing3": 8},
}

# Tags carrying running prose, capped to a comfortable measure on wide windows.
PARAGRAPH_TAGS = ("counts", "frame_kinds", "warn_text", "ok_text", "err_text",
                  "hint_text", "empty_b")

# Compact, consistent names for element kinds. Anything unmapped renders raw.
KIND_LABELS = {
    "button_hover": "hover",
    "checkbutton": "check",
    "combobox": "combo",
    "radiobutton": "radio",
    "rectangle": "rect",
    "tabview": "tabs",
    "text_input": "input",
    "togglebutton": "toggle",
    "listbox": "list",
}


def kind_label(kind: str) -> str:
    """Return the short display name used in an element breakdown."""
    return KIND_LABELS.get(kind, kind)


def kind_summary(kinds: dict) -> str:
    """Return one frame's element mix, most common first."""
    ordered = sorted(kinds.items(), key=lambda item: (-item[1], item[0]))
    return " · ".join(f"{kind_label(kind)} {count}" for kind, count in ordered)


def _modified_date(value: Optional[str]) -> str:
    """Return just the calendar date from a Figma ISO timestamp."""
    if not value:
        return ""
    return str(value).split("T", 1)[0]


def _source_segments(source: dict, template: str) -> List[Segment]:
    """Return the design name and its provenance line."""
    name = source.get("file_name") or source.get("file_key") or "Untitled design"
    segments = [Segment("h1", f"{name}\n")]
    segments.append(Segment("meta_mono", str(source.get("file_key") or "")))
    modified = _modified_date(source.get("last_modified"))
    if modified:
        segments.append(Segment("meta", f" · modified {modified}"))
    if template:
        segments.append(Segment("meta", f" · inspected as {template}"))
    if source.get("selected_node_id"):
        segments.append(Segment("meta", " · selected frame"))
    segments.append(Segment(None, "\n"))
    return segments


def _counts_line(summary: dict) -> List[Segment]:
    """Return the headline totals as one sentence."""
    return [Segment("counts", "{} frames · {} elements · {} image exports\n".format(
        summary.get("frames", 0),
        summary.get("elements", 0),
        summary.get("image_exports", 0),
    ))]


def _frame_segments(frames: Sequence[dict]) -> List[Segment]:
    """Return one titled block per frame with its element breakdown beneath."""
    segments = [Segment("section", "FRAMES\n")]
    for frame in frames:
        name = frame.get("name") or "Untitled frame"
        segments.append(Segment("frame_name", name))
        segments.append(
            Segment("frame_dim", f"  {frame.get('width', 0)}×{frame.get('height', 0)}\n")
        )
        kinds = frame.get("element_kinds") or {}
        summary = kind_summary(kinds) if kinds else "no renderable elements"
        segments.append(Segment("frame_kinds", f"{summary}\n"))
    return segments


def _warning_segments(warnings: Sequence[str]) -> List[Segment]:
    """Return the fidelity warnings; the section heading carries the severity."""
    if not warnings:
        return []
    segments = [Segment("section", "WARNINGS\n")]
    for warning in warnings:
        segments.append(Segment("warn_text", f"{warning}\n"))
    return segments


def inspection_segments(report: dict) -> List[Segment]:
    """Return the full document for a successful inspection."""
    source = report.get("source") or {}
    template = (report.get("generation") or {}).get("template") or ""
    segments = _source_segments(source, template)
    segments.extend(_counts_line(report.get("summary") or {}))
    segments.extend(_frame_segments(report.get("frames") or []))
    segments.extend(_warning_segments(report.get("warnings") or []))
    return segments


def generation_segments(output_path: str, code_files: int, asset_files: int) -> List[Segment]:
    """Return the block appended to the report after a successful generate."""
    return [
        Segment("section", "GENERATED\n"),
        Segment("ok_text", "Project generated successfully.\n"),
        Segment("path", f"{output_path}\n"),
        Segment("counts", f"{code_files} code files · {asset_files} assets\n"),
    ]


ERROR_HINTS = (
    ("403", "The personal access token was rejected. Check that it is valid, has "
            "not expired, and can read this file."),
    ("404", "That file could not be found. Check the design URL, and that the "
            "token's account has access to it."),
    ("429", "Figma is rate limiting this token. Wait a moment and try again."),
    ("internet access", "Check your network connection and try again."),
    ("timed out", "Check your network connection and try again."),
)


def error_hint(message: str) -> str:
    """Return an actionable next step for a known failure, else an empty string."""
    lowered = message.lower()
    for marker, hint in ERROR_HINTS:
        if marker in lowered:
            return hint
    return ""


def error_segments(message: str, last_report: Optional[dict] = None) -> List[Segment]:
    """Return the document shown when inspection or generation fails.

    A failure keeps the previous inspection below it. Losing the plan you just
    reviewed because a download failed would make the report untrustworthy.
    """
    segments = [Segment("err_text", f"{message}\n")]
    hint = error_hint(message)
    if hint:
        segments.append(Segment("hint_text", f"{hint}\n"))
    if last_report:
        segments.append(Segment("section", "LAST INSPECTION\n"))
        segments.extend(inspection_segments(last_report))
    return segments


def empty_segments(inspect_hint: str) -> List[Segment]:
    """Return the first-run placeholder document."""
    return [
        Segment("empty_h", "No inspection yet\n"),
        Segment(
            "empty_b",
            "Paste a Figma design URL and token, then press "
            f"{inspect_hint} to preview the frames, elements, image exports, "
            "and fidelity warnings this design will produce.\n",
        ),
        Segment(
            "empty_b",
            "Need a token? Create one in Figma under Settings → Personal access "
            "tokens.",
        ),
    ]


def working_segments(operation: str) -> List[Segment]:
    """Return the placeholder shown while a first run is in flight."""
    headline = "Inspecting design…" if operation == "inspect" else "Generating project…"
    return [
        Segment("empty_h", f"{headline}\n"),
        Segment(
            "empty_b",
            "Reading the file through the Figma API. Large designs with many "
            "image exports can take a moment.",
        ),
    ]


def segments_to_text(segments: Sequence[Segment]) -> str:
    """Return the plain concatenation of a document, for tests and fallbacks."""
    return "".join(segment.text for segment in segments)
