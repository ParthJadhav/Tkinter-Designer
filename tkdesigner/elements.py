from tkinter.constants import W
import uuid

from jinja2 import Template
from tkdesigner.template import TEMPLATE


TEXT_INPUT_ELEMENT_TYPES = {
    "TextArea": "Text",
    "TextBox": "Entry"
}


class FigmaFrame:
    """Represents the Figma Frame for which the GUI will be generated.
    
    Attributes:
        width: Width of the window.
        height: Height of the window.
        asset_dir: Where the generated assets are stored.
        elements: Child GUI elements.
        bg_color: Color of the GUI background.
    """
    def __init__(self, width, height, asset_dir, bg_color="#FFFFFF", elements=[]):
        self.width = width
        self.height = height
        self.asset_dir = asset_dir
        self.elements = elements
        self.bg_color = bg_color


    def to_code(self, template=TEMPLATE):
        t = Template(template)
        return t.render(window=self, elements=self.elements)


class FigmaElement:
    """Represents each Figma element in the UI.

    Each element has a position, size, and a unique ID.

    Attributes:
        x: X position coordinate of the element.
        y: Y position coordinate of the element.
        width: Width of the element.
        height: Height of the element.
        id_: ID unique to that element, useful for variable names.
    """

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.id_ = str(uuid.uuid4())[:8]

    def to_code(self):
        raise NotImplementedError("to_code() not implemented on element class.")


class RectangleElement(FigmaElement):
    def __init__(self, x, y, width, height, fill_color):
        super().__init__(x, y, width, height)

        self.fill_color = fill_color

    def to_code(self):
        return f"""
canvas.create_rectangle(
    {self.x},
    {self.y},
    {self.x + self.width},
    {self.y + self.height},
    fill="{self.fill_color}",
    outline="")
"""


class ButtonElement(FigmaElement):
    def __init__(self, x, y, width, height, image_path):
        super().__init__(x, y, width, height)

        self.image_path = image_path

    def to_code(self):
        return f"""
button_image_{self.id_} = PhotoImage(file="{self.image_path}")
button_{self.id_} = Button(
    image=button_image_{self.id_},
    borderwidth=0,
    highlightthickness=0,
    command=lambda _: print("button_{self.id_} clicked"),
    relief="flat")
button_{self.id_}.place(
    x={self.x},
    y={self.y},
    width={self.width},
    height={self.height})
"""

class TextElement(FigmaElement):
    def __init__(self, x, y, width, height, color, font, font_size, text):
        super().__init__(x, y, width, height)

        self.color = color
        self.font = font
        self.font_size = font_size
        self.text = text

    
    def to_code(self):
        return f"""
canvas.create_text(
    {self.x},
    {self.y},
    text="{self.text}",
    fill="{self.color}",
    font=("{self.font}", int({self.font_size}))
)
"""


class TextEntryElement(FigmaElement):
    def __init__(self, x, y, width, height, entry_type, bg_color, image_path, corner_radius):
        super().__init__(x, y, width, height)

        self.entry_type = entry_type
        self.bg_color = bg_color
        self.image_path = image_path
        self.corner_radius = corner_radius


    def to_code(self):
        return f"""
entry_image_{self.id_} = PhotoImage(
    file="{self.image_path}"
)
entry_bg_{self.id_} = canvas.create_image(
    {self.x},
    {self.y},
    image=entry_image_{self.id_}
)
entry_{self.id_} = {self.entry_type}(
    bd=0,
    bg="{self.bg_color}",
    highlightthickness=0
)
entry_{self.id_}.place(
    x={self.x},
    y={self.y},
    width={self.width},
    height={self.height}
)
"""


class ImageElement(FigmaElement):
    def __init__(self, x, y, width, height, image_path):
        super().__init__(x, y, width, height)

        self.image_path = image_path

    
    def to_code(self):
        return f"""
image_image_{self.id_} = PhotoImage(file="{self.image_path}")
image_{self.id_} = canvas.create_image(
    {self.x},
    {self.y},
    image=image_image_{self.id_}
)
"""
