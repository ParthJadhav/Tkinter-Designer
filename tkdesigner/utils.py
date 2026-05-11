"""Small utility functions."""

from dataclasses import dataclass
import io
import json
import re
from typing import Iterable, Optional
from urllib.parse import parse_qs, unquote, urlparse

import requests
from PIL import Image


@dataclass(frozen=True)
class FigmaFileReference:
    file_key: str
    node_id: Optional[str] = None


def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)

        return s[start:end]
    except ValueError:
        return ""


def parse_figma_url(value: str) -> FigmaFileReference:
    """Extract a Figma file key and optional selected node id from a URL."""
    value = value.strip()
    if re.fullmatch(r"[0-9A-Za-z]+", value):
        return FigmaFileReference(file_key=value)

    parsed = urlparse(value)
    if not parsed.scheme:
        parsed = urlparse(f"https://{value}")

    host = parsed.netloc.lower()
    if host not in {"figma.com", "www.figma.com"}:
        raise ValueError("Invalid Figma URL host.")

    parts = [unquote(part) for part in parsed.path.split("/") if part]
    file_key = None
    for marker in ("file", "design"):
        if marker in parts:
            marker_index = parts.index(marker)
            if marker_index + 1 < len(parts):
                file_key = parts[marker_index + 1]
                break

    if not file_key or not re.fullmatch(r"[0-9A-Za-z]+", file_key):
        raise ValueError("Invalid Figma file URL.")

    query = parse_qs(parsed.query)
    node_id = query.get("node-id", [None])[0]
    if node_id:
        node_id = unquote(node_id).replace("-", ":")

    return FigmaFileReference(file_key=file_key, node_id=node_id)


def _resampling_filter():
    return getattr(getattr(Image, "Resampling", Image), "LANCZOS")


def download_image(url, image_path, size=None):
    if not url or not isinstance(url, str):
        raise RuntimeError("Figma did not return an image URL for this element.")

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
    except requests.ConnectionError as exc:
        raise RuntimeError("Tkinter Designer requires internet access to download images.") from exc
    except requests.RequestException as exc:
        raise RuntimeError(f"Could not download image asset: {exc}") from exc

    content = io.BytesIO(response.content)
    im = Image.open(content).convert("RGBA")
    if size:
        width, height = size
        width = max(1, int(round(width)))
        height = max(1, int(round(height)))
        if im.size != (width, height):
            im = im.resize((width, height), _resampling_filter())
    with open(image_path, "wb") as file:
        im.save(file, format="PNG")


def color_to_hex(color: Optional[dict], fallback: str = "#FFFFFF") -> str:
    if not isinstance(color, dict):
        return fallback

    try:
        r, g, b = [round(float(color.get(channel, 0)) * 255) for channel in "rgb"]
    except (TypeError, ValueError):
        return fallback

    return f"#{max(0, min(255, r)):02X}{max(0, min(255, g)):02X}{max(0, min(255, b)):02X}"


def paint_to_hex(paints: Optional[Iterable[dict]], fallback: str = "#FFFFFF") -> str:
    if not paints:
        return fallback

    for paint in paints:
        if not isinstance(paint, dict) or not paint.get("visible", True):
            continue
        if paint.get("type") == "SOLID":
            return color_to_hex(paint.get("color"), fallback=fallback)

    return fallback


def contrasting_text_color(background_hex: str) -> str:
    value = background_hex.strip().lstrip("#")
    if len(value) != 6:
        return "#000716"
    try:
        r, g, b = (int(value[index:index + 2], 16) for index in (0, 2, 4))
    except ValueError:
        return "#000716"

    luminance = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255
    return "#FFFFFF" if luminance < 0.45 else "#000716"


def python_string_literal(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)
