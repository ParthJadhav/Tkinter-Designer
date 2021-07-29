from .node import Node


class Vector(Node):
    def __init__(self, node):
        super().__init__(node)

    def color(self):
        try:
            color = self.node["fills"][0]["color"]
            rgba = [int(color.get(i, 0) * 255) for i in "rgba"]
            # return tuple(rgba)
            return f"#{rgba[0]:0X}{rgba[1]:0X}{rgba[2]:0X}"
        except Exception:
            return "#FFFFFF"

    def size(self):
        bbox = self.node["absoluteBoundingBox"]
        width = bbox["width"]
        height = bbox["height"]
        return width, height

    def position(self, frame):
        # Returns element coordinates as x (int) and y (int)
        bbox = self.node["absoluteBoundingBox"]
        x = bbox["x"]
        y = bbox["y"]

        frame_bbox = frame.node["absoluteBoundingBox"]
        frame_x = frame_bbox["x"]
        frame_y = frame_bbox["y"]

        x = abs(x - frame_x)
        y = abs(y - frame_y)
        return x, y

    # Returns a two-letter string as a parameter for the 'anchor' property of
    # a Tkinter Text widget. The string is a combination of the Figma properties
    # textAlignHorizontal and textAlingVertical
    def alignment(self):
        align_translate = {
            "LEFT-TOP": "NW",
            "CENTER-TOP": "N",
            "RIGHT-TOP": "NE",
            "LEFT-CENTER": "W",
            "CENTER-CENTER": "CENTER",
            "RIGHT-CENTER": "E",
            "LEFT-BOTTOM": "SW",
            "CENTER-BOTTOM": "S",
            "RIGHT-BOTTOM": "SE"
        }
        halign = self.style["textAlignHorizontal"]
        valign = self.style["textAlignVertical"]
        return(align_translate[f"{halign}-{valign}"])


class Star(Vector):
    def __init__(self, node):
        super().__init__(node)


class Line(Vector):
    def __init__(self, node):
        super().__init__(node)


class Ellipse(Vector):
    def __init__(self, node):
        super().__init__(node)


class RegularPolygon(Vector):
    def __init__(self, node):
        super().__init__(node)


class Rectangle(Vector):
    def __init__(self, node, frame):
        super().__init__(node)
        self.x, self.y = self.position(frame)
        self.width, self.height = self.size()
        self.fill_color = self.color()

    @property
    def corner_radius(self):
        return self.node.get("cornerRadius")

    @property
    def rectangle_corner_radii(self):
        return self.node.get("rectangleCornerRadii")

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


class UnknownElement(Vector):
    def __init__(self, node, frame):
        super().__init__(node)
        self.x, self.y = self.position(frame)
        self.width, self.height = self.size()

    def to_code(self):
        return f"""
canvas.create_rectangle(
    {self.x},
    {self.y},
    {self.x + self.width},
    {self.y + self.height},
    fill="#000000",
    outline="")
"""
