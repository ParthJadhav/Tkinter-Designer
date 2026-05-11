from ..constants import ASSETS_PATH
from ..utils import download_image, paint_to_hex

from .node import Node
from .endpoints import FigmaAPIError
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
from pathlib import Path


class Frame(Node):
    def __init__(self, node, figma_file, output_path, frameCount=0, *, theme=""):
        super().__init__(node)

        self.width, self.height = self.size()
        self.bg_color = self.color()

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
        for child in children or []:
            node = Node(child)
            if not node.visible or "absoluteBoundingBox" not in child:
                continue

            name = child.get("name", "").strip().lower()
            node_type = child.get("type", "").strip().lower()
            has_children = bool(child.get("children"))

            if self.is_supported_element(name, node_type):
                yield child
            elif has_children and node_type in {
                "frame",
                "group",
                "section",
                "component",
                "component_set",
                "instance",
            }:
                yield from self.iter_renderable_children(child.get("children"))
            else:
                yield child

    def is_supported_element(self, element_name, element_type):
        if element_name in {
            "button",
            "buttonhover",
            "textbox",
            "textarea",
            "image",
            "rectangle",
            "line",
            "checkbox",
            "checkbutton",
            "radiobutton",
            "radio",
            "combobox",
            "listbox",
            "toggle",
            "togglebutton",
            "table",
            "tabview",
            "tabs",
            "notebook",
        }:
            return True
        return element_type in {"rectangle", "line", "text"}

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

        print(
            "Creating Element "
            f"{{ name: {element_name}, type: {element_type} }}"
        )

        if element_name == "button":
            self.counter[Button] = self.counter.get(Button, 0) + 1

            image_path = self.download_element_image(
                element, f"button_{self.counter[Button]}.png")

            return Button(
                element, self, image_path, id_=f"{self.counter[Button]}")

        # EXPERIMENTAL FEATURE
        elif element_name == "buttonhover":
            self.counter[ButtonHover] = self.counter.get(ButtonHover, 0) + 1

            image_path = self.download_element_image(
                element, f"button_hover_{self.counter[ButtonHover]}.png")

            return ButtonHover(
                element, self, image_path)

        elif element_name in ("textbox", "textarea"):
            self.counter[TextEntry] = self.counter.get(TextEntry, 0) + 1

            image_path = self.download_element_image(
                element, f"entry_{self.counter[TextEntry]}.png")

            return TextEntry(
                element, self, image_path, id_=f"{self.counter[TextEntry]}")

        elif element_name == "image":
            self.counter[Image] = self.counter.get(Image, 0) + 1

            image_path = self.download_element_image(
                element, f"image_{self.counter[Image]}.png")

            return Image(
                element, self, image_path, id_=f"{self.counter[Image]}")

        elif element_name in ("checkbox", "checkbutton"):
            self.counter[CheckButton] = self.counter.get(CheckButton, 0) + 1
            return CheckButton(
                element, self, id_=f"{self.counter[CheckButton]}")

        elif element_name in ("radiobutton", "radio"):
            self.counter[RadioButton] = self.counter.get(RadioButton, 0) + 1
            return RadioButton(
                element, self, id_=f"{self.counter[RadioButton]}")

        elif element_name == "combobox":
            self.counter[ComboBox] = self.counter.get(ComboBox, 0) + 1
            return ComboBox(
                element, self, id_=f"{self.counter[ComboBox]}")

        elif element_name == "listbox":
            self.counter[ListBox] = self.counter.get(ListBox, 0) + 1
            return ListBox(
                element, self, id_=f"{self.counter[ListBox]}")

        elif element_name in ("toggle", "togglebutton"):
            self.counter[ToggleButton] = self.counter.get(ToggleButton, 0) + 1
            return ToggleButton(
                element, self, id_=f"{self.counter[ToggleButton]}")

        elif element_name == "table":
            self.counter[Table] = self.counter.get(Table, 0) + 1
            return Table(
                element, self, id_=f"{self.counter[Table]}")

        elif element_name in ("tabview", "tabs", "notebook"):
            self.counter[TabView] = self.counter.get(TabView, 0) + 1
            return TabView(
                element, self, id_=f"{self.counter[TabView]}")

        if element_name == "rectangle" or element_type == "rectangle":
            return Rectangle(element, self)

        if element_name == "line" or element_type == "line":
            return Line(element, self)

        elif element_type == "text":
            return Text(element, self)

        else:
            try:
                self.counter[RasterElement] = self.counter.get(RasterElement, 0) + 1
                image_path = self.download_element_image(
                    element, f"element_{self.counter[RasterElement]}.png")
                return RasterElement(
                    element, self, image_path, id_=f"{self.counter[RasterElement]}")
            except FigmaAPIError as exc:
                if "could not export image data" not in str(exc):
                    raise
                print(
                    f"Element with the name: `{element_name}` cannot be parsed. "
                    "Would be displayed as Black Rectangle")
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
