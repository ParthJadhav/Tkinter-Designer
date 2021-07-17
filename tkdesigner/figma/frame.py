from ..constants import ASSETS_PATH
from ..utils import download_image

from .node import Node
from .vector import Rectangle
from .custom import Button, Text, Image, TextEntry

from jinja2 import Template
from pathlib import Path


class Frame(Node):
    def __init__(self, node, figma_file, output_path):
        super().__init__(node)

        self.width, self.height = self.size()
        self.bg_color = self.color()

        self.counter = 0

        self.figma_file = figma_file

        self.output_path: Path = output_path
        self.assets_path: Path = output_path / ASSETS_PATH

        self.output_path.mkdir(exist_ok=True)
        self.assets_path.mkdir(exist_ok=True)

        self.elements = [
            self.create_element(j, id_=str(i))
            for i, j in enumerate(self.children)
        ]

    def create_element(self, element, *, id_=None):
        element_name = element["name"].strip()
        element_type = element["type"].strip()

        print(
            "Creating Element "
            f"{{ name: {element_name}, type: {element_type} }}"
        )

        if element_name == "Rectangle":
            return Rectangle(element, self)

        elif element_name == "Button":
            item_id = element["id"]
            self.counter += 1

            image_url = self.figma_file.get_image(item_id)
            image_path = self.assets_path / f"button_{self.counter}.png"
            download_image(image_url, image_path)

            image_path = image_path.relative_to(self.output_path)

            return Button(
                element, self, image_path, id_=f"{self.counter}")

        elif element_name in ("TextBox", "TextArea"):
            item_id = element["id"]
            self.counter += 1
            image_url = self.figma_file.get_image(item_id)
            image_path = self.assets_path / f"entry_{self.counter}.png"
            download_image(image_url, image_path)

            image_path = image_path.relative_to(self.output_path)

            return TextEntry(
                element, self, image_path, id_=f"{self.counter}")

        elif element_name == "Image":
            item_id = element["id"]
            self.counter += 1
            image_url = self.figma_file.get_image(item_id)
            image_path = self.assets_path / f"entry_{self.counter}.png"
            download_image(image_url, image_path)

            image_path = image_path.relative_to(self.output_path)

            return Image(element, self, image_path, id_=f"{self.counter}")

        elif element_type == "TEXT":
            return Text(element, self)
        else:
            raise NotImplementedError(
                f"Element with the name: `{element_name}` cannot be parsed.")

    @property
    def children(self):
        # TODO: Convert nodes to Node objects before returning a list of them.
        return self.node.get("children")

    def color(self) -> str:
        """Returns HEX form of element RGB color (str)
        """
        try:
            color = self.node["fills"][0]["color"]
            rgba = [int(color.get(i, 0) * 255) for i in "rgba"]
            return f"#{rgba[0]:0X}{rgba[1]:0X}{rgba[2]:0X}"
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
