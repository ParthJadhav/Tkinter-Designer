from .vector_elements import Vector, Rectangle

TEXT_INPUT_ELEMENT_TYPES = {
    "TextArea": "Text",
    "TextBox": "Entry"
}


class Button(Rectangle):
    def __init__(self, node, frame, image_path, *, id_):
        super().__init__(node, frame)
        self.image_path = image_path
        self.id_ = id_

    def to_code(self):
        return f"""
button_image_{self.id_} = PhotoImage(
    file=relative_to_assets("{self.image_path}"))
button_{self.id_} = Button(
    image=button_image_{self.id_},
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_{self.id_} clicked"),
    relief="flat"
)
button_{self.id_}.place(
    x={self.x},
    y={self.y},
    width={self.width},
    height={self.height}
)
"""


class Text(Vector):
    def __init__(self, node, frame):
        super().__init__(node)

        self.x, self.y = self.position(frame)
        self.width, self.height = self.size()

        self.text_color = self.color()
        self.font, self.font_size = self.font_property()
        self.text = self.characters.replace("\n", "\\n")

    @property
    def characters(self) -> str:
        string: str = self.node.get("characters")
        text_case: str = self.style.get("textCase", "ORIGINAL")

        if text_case == "UPPER":
            string = string.upper()
        elif text_case == "LOWER":
            string = string.lower()
        elif text_case == "TITLE":
            string = string.title()

        return string

    @property
    def style(self):
        # TODO: Native conversion
        return self.node.get("style")

    @property
    def character_style_overrides(self):
        return self.node.get("characterStyleOverrides")

    @property
    def style_override_table(self):
        # TODO: Native conversion
        return self.node.get("styleOverrideTable")

    def font_property(self):
        style = self.node.get("style")

        font_name = style.get("fontPostScriptName")
        if font_name is None:
            font_name = style["fontFamily"]

        font_name = font_name.replace('-', ' ')
        font_size = style["fontSize"]
        return font_name, font_size

    def to_code(self):
        return f"""
canvas.create_text(
    {self.x},
    {self.y},
    anchor="nw",
    text="{self.text}",
    fill="{self.text_color}",
    font=("{self.font}", {int(self.font_size)} * -1)
)
"""


class Image(Vector):
    def __init__(self, node, frame, image_path, *, id_):
        super().__init__(node)

        self.x, self.y = self.position(frame)

        width, height = self.size()
        self.x += width // 2
        self.y += height // 2

        self.image_path = image_path
        self.id_ = id_

    def to_code(self):
        return f"""
image_image_{self.id_} = PhotoImage(
    file=relative_to_assets("{self.image_path}"))
image_{self.id_} = canvas.create_image(
    {self.x},
    {self.y},
    image=image_image_{self.id_}
)
"""


class TextEntry(Vector):
    def __init__(self, node, frame, image_path, *, id_):
        super().__init__(node)

        self.id_ = id_
        self.image_path = image_path

        self.x, self.y = self.position(frame)
        width, height = self.size()
        self.x += width / 2
        self.y += height / 2

        self.bg_color = self.color()

        corner_radius = self.get("cornerRadius", 0)
        if corner_radius > height / 2:
            corner_radius = height / 2

        self.entry_width = width - (corner_radius * 2)
        self.entry_height = height - 2

        self.entry_x, self.entry_y = self.position(frame)
        self.entry_x += corner_radius

        self.entry_type = TEXT_INPUT_ELEMENT_TYPES.get(self.get("name"))

    def to_code(self):
        return f"""
entry_image_{self.id_} = PhotoImage(
    file=relative_to_assets("{self.image_path}"))
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
    x={self.entry_x},
    y={self.entry_y},
    width={self.entry_width},
    height={self.entry_height}
)
"""
