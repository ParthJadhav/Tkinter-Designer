"""Read-only design inspection and generation previews."""

from collections import Counter
from dataclasses import asdict, dataclass
import json
from typing import Iterable, Optional, Tuple

from .figma.schema import classify_element, iter_renderable_nodes


@dataclass(frozen=True)
class FrameSummary:
    """A compact description of one Figma frame."""

    id: str
    name: str
    width: int
    height: int
    elements: int
    element_kinds: dict


@dataclass(frozen=True)
class DesignReport:
    """A serializable preview of what Tkinter Designer will generate."""

    file_key: str
    file_name: str
    selected_node_id: Optional[str]
    last_modified: Optional[str]
    template: str
    frames: Tuple[FrameSummary, ...]
    warnings: Tuple[str, ...]

    @property
    def element_count(self) -> int:
        return sum(frame.elements for frame in self.frames)

    @property
    def image_export_count(self) -> int:
        export_kinds = {"button", "button_hover", "image", "raster", "text_input"}
        return sum(
            count
            for frame in self.frames
            for kind, count in frame.element_kinds.items()
            if kind in export_kinds
        )

    def to_dict(self) -> dict:
        return {
            "source": {
                "file_key": self.file_key,
                "file_name": self.file_name,
                "selected_node_id": self.selected_node_id,
                "last_modified": self.last_modified,
            },
            "generation": {"template": self.template},
            "summary": {
                "frames": len(self.frames),
                "elements": self.element_count,
                "image_exports": self.image_export_count,
            },
            "frames": [asdict(frame) for frame in self.frames],
            "warnings": list(self.warnings),
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, sort_keys=True)

    def to_text(self) -> str:
        source = self.file_name or self.file_key
        lines = [
            f"Design: {source}",
            f"Plan: {len(self.frames)} frame(s), {self.element_count} element(s), "
            f"{self.image_export_count} image export(s)",
            f"Template: {self.template}",
            "",
        ]
        for index, frame in enumerate(self.frames, start=1):
            kinds = ", ".join(
                f"{kind}={count}"
                for kind, count in sorted(frame.element_kinds.items())
            ) or "empty"
            lines.append(
                f"{index}. {frame.name} ({frame.width}x{frame.height}) — {kinds}"
            )
        if self.warnings:
            lines.extend(["", "Warnings:"])
            lines.extend(f"- {warning}" for warning in self.warnings)
        return "\n".join(lines)


def build_design_report(
    *,
    file_data: dict,
    file_key: str,
    selected_node_id: Optional[str],
    template: str,
    frame_nodes: Iterable[dict],
) -> DesignReport:
    """Build a report from already-fetched Figma data without exporting assets."""
    frames = []
    warnings = []
    frame_sizes = set()

    for frame_node in frame_nodes:
        bbox = frame_node.get("absoluteBoundingBox") or {}
        width = int(round(float(bbox.get("width", 0))))
        height = int(round(float(bbox.get("height", 0))))
        frame_sizes.add((width, height))
        counts = Counter(
            classify_element(node)
            for node in iter_renderable_nodes(frame_node.get("children") or [])
        )
        summary = FrameSummary(
            id=str(frame_node.get("id") or ""),
            name=str(frame_node.get("name") or "Untitled frame"),
            width=width,
            height=height,
            elements=sum(counts.values()),
            element_kinds=dict(sorted(counts.items())),
        )
        frames.append(summary)
        if summary.elements == 0:
            warnings.append(f"Frame `{summary.name}` has no renderable elements.")

    raster_count = sum(frame.element_kinds.get("raster", 0) for frame in frames)
    if raster_count:
        warnings.append(
            f"{raster_count} complex or unsupported element(s) will be preserved "
            "as raster images."
        )
    if template == "pages" and len(frame_sizes) > 1:
        warnings.append(
            "Page frames use different dimensions; the first frame defines the "
            "application window size."
        )

    return DesignReport(
        file_key=file_key,
        file_name=str(file_data.get("name") or ""),
        selected_node_id=selected_node_id,
        last_modified=file_data.get("lastModified"),
        template=template,
        frames=tuple(frames),
        warnings=tuple(warnings),
    )
