from ..constants import ASSETS_PATH
from ..utils import download_image

from .node import Node
from .vector_elements import Rectangle, UnknownElement
from .custom_elements import Button, Text, Image, TextEntry

from jinja2 import Template
from pathlib import Path


class Frame(Node):
    def __init__(self, node, figma_file, output_path):
        super().__init__(node)

        self.width, self.height = self.size()
        self.bg_color = self.color()

        self.counter = {}

        self.figma_file = figma_file

        self.output_path: Path = output_path
        self.assets_path: Path = output_path / ASSETS_PATH

        self.output_path.mkdir(parents=True, exist_ok=True)
        self.assets_path.mkdir(parents=True, exist_ok=True)

        self.elements = [
            self.create_element(child)
            for child in self.children
            if Node(child).visible
        ]

    def create_element(self, element):
        element_name = element["name"].strip()
        element_type = element["type"].strip()

        print(
            "Creating Element "
            f"{{ name: {element_name}, type: {element_type} }}"
        )

        if element_name == "Rectangle":
            return Rectangle(element, self)

        elif element_name == "Button":
            self.counter[Button] = self.counter.get(Button, 0) + 1

            item_id = element["id"]
            image_url = self.figma_file.get_image(item_id)
            image_path = (
                self.assets_path / f"button_{self.counter[Button]}.png")
            download_image(image_url, image_path)

            image_path = image_path.relative_to(self.assets_path)

            return Button(
                element, self, image_path, id_=f"{self.counter[Button]}")

        elif element_name in ("TextBox", "TextArea"):
            self.counter[TextEntry] = self.counter.get(TextEntry, 0) + 1

            item_id = element["id"]
            image_url = self.figma_file.get_image(item_id)
            image_path = (
                self.assets_path / f"entry_{self.counter[TextEntry]}.png")
            download_image(image_url, image_path)

            image_path = image_path.relative_to(self.assets_path)

            return TextEntry(
                element, self, image_path, id_=f"{self.counter[TextEntry]}")

        elif element_name == "Image":
            self.counter[Image] = self.counter.get(Image, 0) + 1

            item_id = element["id"]
            image_url = self.figma_file.get_image(item_id)
            image_path = self.assets_path / f"image_{self.counter[Image]}.png"
            download_image(image_url, image_path)

            image_path = image_path.relative_to(self.assets_path)

            return Image(
                element, self, image_path, id_=f"{self.counter[Image]}")

        elif element_type == "TEXT":
            return Text(element, self)

        else:
            print(
                f"Element with the name: `{element_name}` cannot be parsed. "
                "Would be displayed as Black Rectangle")
            return UnknownElement(element, self)

    @property
    def children(self):
        # TODO: Convert nodes to Node objects before returning a list of them.
        return self.node.get("children")

    def color(self) -> str:
        """Returns HEX form of element RGB color (str)
        """
        try:
            color = self.node["fills"][0]["color"]
            r, g, b, *_ = [int(color.get(i, 0) * 255) for i in "rgba"]
            return f"#{r:02X}{g:02X}{b:02X}"
        except Exception:
            return "#FFFFFF"

    def size(self) -> tuple:
        """Returns element dimensions as width (int) and height (int)
        """
        bbox = self.node["absoluteBoundingBox"]
        width = bbox["width"]
        height = bbox["height"]
        return int(width), int(height)

    def to_code(self, template):
        t = Template(template)
        return t.render(
            window=self, elements=self.elements, assets_path=ASSETS_PATH)


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
