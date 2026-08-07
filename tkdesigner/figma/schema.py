"""Shared rules for translating Figma nodes into Tkinter elements.

Keeping these rules outside the renderer means inspection and generation always
agree about what will happen to a node.
"""

from typing import Iterable, Iterator

from .node import Node


CONTAINER_NODE_TYPES = {
    "frame",
    "group",
    "section",
    "component",
    "component_set",
    "instance",
}

NAMED_ELEMENT_KINDS = {
    "button": "button",
    "buttonhover": "button_hover",
    "textbox": "text_input",
    "textarea": "text_input",
    "image": "image",
    "checkbox": "checkbutton",
    "checkbutton": "checkbutton",
    "radiobutton": "radiobutton",
    "radio": "radiobutton",
    "combobox": "combobox",
    "listbox": "listbox",
    "toggle": "togglebutton",
    "togglebutton": "togglebutton",
    "table": "table",
    "tabview": "tabview",
    "tabs": "tabview",
    "notebook": "tabview",
    "rectangle": "rectangle",
    "line": "line",
}

NATIVE_WIDGET_KINDS = {
    "checkbutton",
    "radiobutton",
    "combobox",
    "listbox",
    "togglebutton",
    "table",
    "tabview",
}

IMAGE_EXPORT_KINDS = {
    "button",
    "button_hover",
    "image",
    "raster",
    "text_input",
}


def node_name(node: dict) -> str:
    return str(node.get("name") or "").strip().lower()


def node_type(node: dict) -> str:
    return str(node.get("type") or "").strip().lower()


def _opacity(value) -> float:
    return 1.0 if value is None else float(value)


def has_complex_appearance(node: dict) -> bool:
    """Return whether native Canvas drawing would visibly lose fidelity."""
    if _opacity(node.get("opacity", 1)) != 1:
        return True
    if any(
        effect.get("visible", True)
        for effect in node.get("effects") or []
        if isinstance(effect, dict)
    ):
        return True

    paints = list(node.get("fills") or []) + list(node.get("strokes") or [])
    for paint in paints:
        if not isinstance(paint, dict) or not paint.get("visible", True):
            continue
        color = paint.get("color") or {}
        if (
            paint.get("type") != "SOLID"
            or _opacity(paint.get("opacity", 1)) != 1
            or _opacity(color.get("a", 1)) != 1
        ):
            return True
    return False


def classify_element(node: dict) -> str:
    """Return the renderer kind used for one visible, renderable node."""
    name = node_name(node)
    kind = NAMED_ELEMENT_KINDS.get(name)
    if kind is not None:
        if kind in {"rectangle", "line"} and has_complex_appearance(node):
            return "raster"
        return kind

    kind = node_type(node)
    if kind == "rectangle":
        return "raster" if has_complex_appearance(node) else "rectangle"
    if kind == "line":
        return "raster" if has_complex_appearance(node) else "line"
    if kind == "text":
        return "raster" if has_complex_appearance(node) else "text"
    return "raster"


def is_directly_renderable(node: dict) -> bool:
    name = node_name(node)
    kind = node_type(node)
    if kind in CONTAINER_NODE_TYPES and has_complex_appearance(node):
        return True
    return name in NAMED_ELEMENT_KINDS or kind in {
        "rectangle",
        "line",
        "text",
    }


def iter_renderable_nodes(children: Iterable[dict]) -> Iterator[dict]:
    """Flatten structural Figma containers without flattening named widgets."""
    for child in children or []:
        wrapped = Node(child)
        if not wrapped.visible or "absoluteBoundingBox" not in child:
            continue

        if is_directly_renderable(child):
            yield child
            continue

        if child.get("children") and node_type(child) in CONTAINER_NODE_TYPES:
            yield from iter_renderable_nodes(child.get("children") or [])
            continue

        yield child


def image_export_ids(children: Iterable[dict]) -> list:
    """Return unique node IDs that need raster data from Figma."""
    result = []
    seen = set()
    for node in iter_renderable_nodes(children):
        node_id = node.get("id")
        should_export = (
            bool(node_id)
            and node_id not in seen  # noqa: W503
            and classify_element(node) in IMAGE_EXPORT_KINDS  # noqa: W503
        )
        if should_export:
            result.append(node_id)
            seen.add(node_id)
    return result
