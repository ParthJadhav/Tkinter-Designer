from ..constants import ASSETS_PATH
from ..utils import download_image, paint_to_hex, python_string_literal

from .node import Node
from .endpoints import FigmaAPIError
from .schema import classify_element, image_export_ids, iter_renderable_nodes
from .vector_elements import Line, Rectangle, UnknownElement
from .custom_elements import (
    Button,
    ButtonHover,
    CheckButton,
    ComboBox,
    Image,
    ListBox,
    RadioButton,
    RasterElement,
    Text,
    TextEntry,
    ToggleButton,
    Table,
    TabView,
)

from jinja2 import Template
import logging
from pathlib import Path


LOGGER = logging.getLogger("tkdesigner.generation")


class Frame(Node):
    def __init__(self, node, figma_file, output_path, frameCount=0, *, theme=""):
        super().__init__(node)

        self.width, self.height = self.size()
        self.bg_color = self.color()
        self.title_literal = python_string_literal(
            self.name or "Tkinter Designer App")

        self.counter = {}
        self.hover_targets = {}
        self.theme = theme

        self.figma_file = figma_file

        self.output_path: Path = output_path
        self.assets_path: Path = output_path / ASSETS_PATH / f"frame{frameCount}"

        self.output_path.mkdir(parents=True, exist_ok=True)
        self.assets_path.mkdir(parents=True, exist_ok=True)

        self.elements = [
            self.create_element(child)
            for child in self.iter_renderable_children(self.children)
        ]

    def iter_renderable_children(self, children):
        yield from iter_renderable_nodes(children)

    @staticmethod
    def image_export_ids(frame_node):
        """Return all assets that can be fetched in one Figma API request."""
        return image_export_ids(frame_node.get("children") or [])

    def element_size(self, element):
        bbox = element["absoluteBoundingBox"]
        return bbox["width"], bbox["height"]

    def download_element_image(self, element, file_name):
        item_id = element["id"]
        image_url = self.figma_file.get_image(item_id)
        image_path = self.assets_path / file_name
        download_image(image_url, image_path, size=self.element_size(element))
        return image_path.relative_to(self.assets_path)

    def create_element(self, element):
        element_name = element["name"].strip().lower()
        element_type = element["type"].strip().lower()
        element_kind = classify_element(element)

        LOGGER.info(
            "Creating Element "
            f"{{ name: {element_name}, type: {element_type} }}"
        )

        image_elements = {
            "button": (Button, "button"),
            "button_hover": (ButtonHover, "button_hover"),
            "text_input": (TextEntry, "entry"),
            "image": (Image, "image"),
        }
        native_elements = {
            "checkbutton": CheckButton,
            "radiobutton": RadioButton,
            "combobox": ComboBox,
            "listbox": ListBox,
            "togglebutton": ToggleButton,
            "table": Table,
            "tabview": TabView,
        }
        vector_elements = {
            "rectangle": Rectangle,
            "line": Line,
            "text": Text,
        }

        if element_kind in image_elements:
            element_class, filename = image_elements[element_kind]
            return self._create_image_element(element, element_class, filename)
        if element_kind in native_elements:
            return self._create_native_element(element, native_elements[element_kind])
        if element_kind in vector_elements:
            return vector_elements[element_kind](element, self)
        return self._create_raster_element(element, element_name)

    def _next_id(self, element_class):
        self.counter[element_class] = self.counter.get(element_class, 0) + 1
        return str(self.counter[element_class])

    def _create_image_element(self, element, element_class, filename):
        element_id = self._next_id(element_class)
        image_path = self.download_element_image(
            element, f"{filename}_{element_id}.png")
        if element_class is ButtonHover:
            return ButtonHover(element, self, image_path)
        return element_class(element, self, image_path, id_=element_id)

    def _create_native_element(self, element, element_class):
        return element_class(element, self, id_=self._next_id(element_class))

    def _create_raster_element(self, element, element_name):
        element_id = self._next_id(RasterElement)
        try:
            image_path = self.download_element_image(
                element, f"element_{element_id}.png")
            return RasterElement(element, self, image_path, id_=element_id)
        except FigmaAPIError as exc:
            if "could not export image data" not in str(exc):
                raise
            LOGGER.warning(
                f"Element with the name: `{element_name}` cannot be parsed. "
                "It will be displayed as a black rectangle.")
            return UnknownElement(element, self)

    @property
    def children(self):
        # TODO: Convert nodes to Node objects before returning a list of them.
        return self.node.get("children")

    def color(self) -> str:
        """Returns HEX form of element RGB color (str)."""
        return paint_to_hex(self.node.get("fills"), fallback="#FFFFFF")

    def size(self) -> tuple:
        """Returns element dimensions as width (int) and height (int)
        """
        bbox = self.node["absoluteBoundingBox"]
        width = bbox["width"]
        height = bbox["height"]
        return int(width), int(height)

    def to_code(self, template):
        t = Template(template)
        assets_path = self.assets_path.relative_to(self.output_path)
        return t.render(
            window=self,
            elements=self.elements,
            assets_path=assets_path,
            theme=self.theme,
        )


# Frame Subclasses


class Group(Frame):
    def __init__(self, node):
        super().__init__(node)


class Component(Frame):
    def __init__(self, node):
        super().__init__(node)


class ComponentSet(Frame):
    def __init__(self, node):
        super().__init__(node)


class Instance(Frame):
    def __init__(self, node):
        super().__init__(node)

    @property
    def component_id(self) -> str:
        self.node.get("componentId")
