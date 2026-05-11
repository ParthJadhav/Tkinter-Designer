from .node import Node
from ..utils import paint_to_hex


class Vector(Node):
    def __init__(self, node):
        super().__init__(node)

    def color(self) -> str:
        """Returns HEX form of element RGB color (str)."""
        return paint_to_hex(self.node.get("fills"), fallback="#FFFFFF")

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

        x = x - frame_x
        y = y - frame_y
        return x, y


class Star(Vector):
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

    def corner_radius_value(self):
        radius = self.corner_radius
        if radius is None:
            radii = self.rectangle_corner_radii or []
            radius = min(radii) if radii else 0
        return max(0, min(float(radius or 0), self.width / 2, self.height / 2))

    def to_code(self):
        radius = self.corner_radius_value()
        if radius:
            return f"""
create_rounded_rectangle(
    canvas,
    {self.x},
    {self.y},
    {self.x + self.width},
    {self.y + self.height},
    {radius},
    fill="{self.fill_color}",
    outline="")
"""

        return f"""
canvas.create_rectangle(
    {self.x},
    {self.y},
    {self.x + self.width},
    {self.y + self.height},
    fill="{self.fill_color}",
    outline="")
"""


class Line(Rectangle):
    def __init__(self, node, frame):
        super().__init__(node, frame)

    def color(self) -> str:
        """Returns HEX form of element RGB color (str)."""
        return paint_to_hex(self.node.get("strokes"), fallback="#FFFFFF")

    def size(self):
        width, height = super().size()
        return width + self.node["strokeWeight"], height + self.node["strokeWeight"]

    def position(self, frame):
        x, y = super().position(frame)
        return x - self.node["strokeWeight"], y - self.node["strokeWeight"]


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
