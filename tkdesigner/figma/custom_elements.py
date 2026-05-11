from .vector_elements import Vector, Rectangle
from ..utils import contrasting_text_color, python_string_literal

TEXT_INPUT_ELEMENT_TYPES = {
    "textarea": "Text",
    "textbox": "Entry"
}


class Button(Rectangle):
    def __init__(self, node, frame, image_path, *, id_):
        super().__init__(node, frame)
        self.image_path = image_path
        self.id_ = id_
        frame.hover_targets[(self.x, self.y)] = self.id_

    def to_code(self):
        return f"""
button_image_{self.id_} = load_photo_image(
    relative_to_assets("{self.image_path}"))
button_{self.id_} = ImageButton(
    window,
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


# EXPERIMENTAL FEATURE
class ButtonHover(Rectangle):
    def __init__(self, node, frame, image_path):
        super().__init__(node, frame)
        self.image_path = image_path
        self.has_target = False

        if (self.x, self.y) in frame.hover_targets:
            self.id_ = frame.hover_targets[(self.x, self.y)]
            self.has_target = True
        else:
            print(
                "`ButtonHover` element must be placed on top of Button "
                "element with the same position.\n"
                "`ButtonHover` element will not be rendered")

    def to_code(self):
        if self.has_target:
            return f"""
button_image_hover_{self.id_} = load_photo_image(
    relative_to_assets("{self.image_path}"))

def button_{self.id_}_hover(e):
    button_{self.id_}.config(
        image=button_image_hover_{self.id_}
    )
def button_{self.id_}_leave(e):
    button_{self.id_}.config(
        image=button_image_{self.id_}
    )

button_{self.id_}.bind('<Enter>', button_{self.id_}_hover)
button_{self.id_}.bind('<Leave>', button_{self.id_}_leave)

"""
        else:
            return ""


class Text(Vector):
    def __init__(self, node, frame):
        super().__init__(node)

        self.x, self.y = self.position(frame)
        self.width, self.height = self.size()

        self.text_color = self.color()
        self.font, self.font_size, self.font_weight, self.font_slant = self.font_property()
        self.text = python_string_literal(self.characters)

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
        return self.node.get("style") or {}

    @property
    def character_style_overrides(self):
        return self.node.get("characterStyleOverrides")

    @property
    def style_override_table(self):
        # TODO: Native conversion
        return self.node.get("styleOverrideTable")

    def font_property(self):
        style = self.node.get("style") or {}

        font_name = style.get("fontFamily") or style.get("fontPostScriptName")
        if font_name is None:
            font_name = "Arial"

        font_name = font_name.replace("-", " ")
        font_size = style.get("fontSize", 12)
        font_weight = "bold" if style.get("fontWeight", 400) >= 600 else "normal"
        font_slant = "italic" if style.get("italic") else "roman"
        return font_name, font_size, font_weight, font_slant

    def to_code(self):
        return f"""
canvas.create_text(
    {self.x},
    {self.y},
    anchor="nw",
    text={self.text},
    fill="{self.text_color}",
    font=("{self.font}", {int(self.font_size)} * -1, "{self.font_weight}", "{self.font_slant}")
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
image_image_{self.id_} = load_photo_image(
    relative_to_assets("{self.image_path}"))
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
        self.fg_color = contrasting_text_color(self.bg_color)

        corner_radius = self.get("cornerRadius", 0)
        corner_radius = min(corner_radius, height / 2)
        self.entry_width = width - (corner_radius * 2)
        self.entry_height = height - 2

        self.entry_x, self.entry_y = self.position(frame)
        self.entry_x += corner_radius

        self.entry_type = TEXT_INPUT_ELEMENT_TYPES.get(self.get("name", "").lower())

    def to_code(self):
        return f"""
entry_image_{self.id_} = load_photo_image(
    relative_to_assets("{self.image_path}"))
entry_bg_{self.id_} = canvas.create_image(
    {self.x},
    {self.y},
    image=entry_image_{self.id_}
)
entry_{self.id_} = {self.entry_type}(
    window,
    bd=0,
    bg="{self.bg_color}",
    fg="{self.fg_color}",
    insertbackground="{self.fg_color}",
    highlightthickness=0
)
entry_{self.id_}.place(
    x={self.entry_x},
    y={self.entry_y},
    width={self.entry_width},
    height={self.entry_height}
)
"""


class RasterElement(Image):
    pass


class NativeWidget(Rectangle):
    widget_name = "Widget"

    def __init__(self, node, frame, *, id_):
        super().__init__(node, frame)
        self.id_ = id_
        self.bg_color = frame.bg_color


class CheckButton(NativeWidget):
    def to_code(self):
        return f"""
check_var_{self.id_} = BooleanVar(value=False)
checkbutton_{self.id_} = Checkbutton(
    window,
    text="",
    variable=check_var_{self.id_},
    bg="{self.bg_color}",
    activebackground="{self.bg_color}",
    borderwidth=0,
    highlightthickness=0
)
checkbutton_{self.id_}.place(
    x={self.x},
    y={self.y},
    width={self.width},
    height={self.height}
)
"""


class RadioButton(NativeWidget):
    def to_code(self):
        return f"""
radio_var_{self.id_} = StringVar(value="")
radiobutton_{self.id_} = Radiobutton(
    window,
    text="",
    variable=radio_var_{self.id_},
    value="{self.id_}",
    bg="{self.bg_color}",
    activebackground="{self.bg_color}",
    borderwidth=0,
    highlightthickness=0
)
radiobutton_{self.id_}.place(
    x={self.x},
    y={self.y},
    width={self.width},
    height={self.height}
)
"""


class ComboBox(NativeWidget):
    def to_code(self):
        return f"""
combobox_{self.id_} = ttk.Combobox(window, values=())
combobox_{self.id_}.place(
    x={self.x},
    y={self.y},
    width={self.width},
    height={self.height}
)
"""


class ListBox(NativeWidget):
    def to_code(self):
        return f"""
listbox_{self.id_} = Listbox(window, borderwidth=0, highlightthickness=0)
listbox_{self.id_}.place(
    x={self.x},
    y={self.y},
    width={self.width},
    height={self.height}
)
"""


class ToggleButton(CheckButton):
    def to_code(self):
        return f"""
toggle_var_{self.id_} = BooleanVar(value=False)
togglebutton_{self.id_} = Checkbutton(
    window,
    text="",
    variable=toggle_var_{self.id_},
    indicatoron=False,
    bg="{self.bg_color}",
    activebackground="{self.bg_color}",
    borderwidth=0,
    highlightthickness=0
)
togglebutton_{self.id_}.place(
    x={self.x},
    y={self.y},
    width={self.width},
    height={self.height}
)
"""


class Table(NativeWidget):
    def to_code(self):
        return f"""
table_{self.id_} = ttk.Treeview(
    window,
    columns=("Column 1", "Column 2"),
    show="headings"
)
table_{self.id_}.heading("Column 1", text="Column 1")
table_{self.id_}.heading("Column 2", text="Column 2")
table_{self.id_}.place(
    x={self.x},
    y={self.y},
    width={self.width},
    height={self.height}
)
"""


class TabView(NativeWidget):
    def to_code(self):
        return f"""
tabs_{self.id_} = ttk.Notebook(window)
tab_{self.id_}_1 = Frame(tabs_{self.id_})
tab_{self.id_}_2 = Frame(tabs_{self.id_})
tabs_{self.id_}.add(tab_{self.id_}_1, text="Tab 1")
tabs_{self.id_}.add(tab_{self.id_}_2, text="Tab 2")
tabs_{self.id_}.place(
    x={self.x},
    y={self.y},
    width={self.width},
    height={self.height}
)
"""
