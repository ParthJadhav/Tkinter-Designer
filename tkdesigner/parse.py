"""
Module to handle parsing Figma elements.
"""

import os
from tkdesigner.constants import ASSETS_PATH
from typing import Counter, List, Type
import uuid
from enum import Enum

import requests

from tkdesigner import elements


class Elements(Enum):
    RECTANGLE = 0
    BUTTON = 1
    TEXT = 2
    TEXTENTRY = 3
    IMAGE = 4


class ElementCounter():
    """Manages counting elements to generate unique incremental IDs."""

    def __init__(self, elements: List[Elements]):
        self.counter = {element_type: 1 for element_type in elements}

    def get_and_increment(self, element: Elements):
        curr_value = self.counter.get(element)

        if curr_value is None:
            raise ValueError(
                f"There is no counter for the element type {element.name}. Make sure that "
                "all element types to be counted are passed to the `ElementCounter` constructor.")

        self.counter[element] += 1

        return curr_value


class FigmaParser():
    """Parses Figma GUI data.
    
    Will mostly be used for the `.parse_gui()` method as an entrypoint to parsing
    Figma documents and its elements.
    """

    # List of currently supported element types by the parser. Must be updated
    # when adding new element types.
    SUPPORTED_ELEMENTS = [
        Elements.RECTANGLE,
        Elements.BUTTON,
        Elements.TEXT,
        Elements.TEXTENTRY,
        Elements.IMAGE
    ]

    def __init__(self, token: str, file_id: str, output_path: str):
        self.token = token
        self.file_id = file_id
        self.output_path = output_path
        
        self.counter = ElementCounter(self.SUPPORTED_ELEMENTS)
        
        
    def get_color(self, element_data: dict):
        # Returns HEX form of element RGB color (str)
        el_r = element_data["fills"][0]["color"]['r'] * 255
        el_g = element_data["fills"][0]["color"]['g'] * 255
        el_b = element_data["fills"][0]["color"]['b'] * 255

        hex_code = ('#%02x%02x%02x' % (round(el_r), round(el_g), round(el_b)))

        return hex_code


    def get_coordinates(self, element_data: dict, frame_data: dict):
        # Returns element coordinates as x (int) and y (int)
        element_x = int(element_data["absoluteBoundingBox"]["x"])
        element_y = int(element_data["absoluteBoundingBox"]["y"])
        window_x = int(frame_data["absoluteBoundingBox"]["x"])
        window_y = int(frame_data["absoluteBoundingBox"]["y"])

        element_x = abs(element_x - window_x)
        element_y = abs(element_y - window_y)

        return element_x, element_y


    def get_dimensions(self, element_data: dict):
        # Return element dimensions as width (int) and height (int)
        height = int(element_data["absoluteBoundingBox"]["height"])
        width = int(element_data["absoluteBoundingBox"]["width"])

        return width, height


    def get_text_properties(self, element_data: dict):
        # Return element font and fontSize (str)
        font = element_data["style"]["fontPostScriptName"]
        fontSize = element_data["style"]["fontSize"]

        return font, fontSize

    
    def download_image(self, item_id, item_type, item_count):
        """
        Download the image for the `item_id` and save it to the asset directory.

        Returns:
            The path to the image relative to the assets directory.
        """

        def generate_image_id(type,count):
            return type+"-"+str(count)

        response = requests.get(
            f"https://api.figma.com/v1/images/{self.file_id}?ids={item_id}",
            headers={"X-FIGMA-TOKEN": f"{self.token}"})

        image_response = requests.get(response.json()["images"][item_id])
        image_path = f"{generate_image_id(item_type,item_count)}-img.png"
        output_image_path = os.path.join(self.output_path, ASSETS_PATH, image_path)
        with open(output_image_path, "wb") as file:
            file.write(image_response.content)
        
        return image_path

    
    def parse_element(self, element_data, frame_data) -> Type[elements.FigmaElement]:
        """Parse element according to it's name and/or type.
        
        Arguments:
            element_data: The Figma document data for the element.
            frame_data: The Figma frame data that contains the element.

        Returns:
            A FigmaElement subclass, depending on the type of element data passed in.

        Raises:
            NotImplementedError: If the element passed in is not supported by the parser.
        """
        element_name = element_data["name"]
        element_type = element_data["type"]

        if element_name == "Rectangle":
            return self.parse_rectangle_element(element_data, frame_data)
        elif element_name == "Button":
            return self.parse_button_element(element_data, frame_data)
        elif element_name in ("TextBox", "TextArea"):
            return self.parse_text_entry(element_data, frame_data)
        elif element_name == "Image":
            return self.parse_image_element(element_data, frame_data)
        elif element_type == "TEXT":
            return self.parse_text_element(element_data, frame_data)
        else:
            raise NotImplementedError(f"Element with the name: `{element_name}` cannot be parsed.")

    
    def parse_gui(self, data):
        """Takes the entire Figma document `data` and parses each element.
        
        Generally this would be the entry point to parsing Figma GUIs.
        """
        frame_data = data["document"]["children"][0]["children"][0]

        width, height = self.get_dimensions(frame_data)

        try:
            bg_color = self.get_color(frame_data)
        except Exception:
            # If the background colour can't be parsed, fallback to white
            bg_color = "#FFFFFF"

        parsed_elements: List[elements.Element] = []
        for element_data in frame_data["children"]:
            parsed_elements.append(self.parse_element(element_data, frame_data))

        return elements.FigmaFrame(
            width,
            height,
            bg_color,
            parsed_elements)
            

    def parse_frame(self, frame_data: dict):
        width, height = self.get_dimensions(frame_data)

        try:
            bg_color = self.get_color(frame_data)
        except Exception:
            # If the background colour can't be parsed, fallback to white
            bg_color = "#FFFFFF"

        return elements.FigmaFrame(width, height, bg_color)


    def parse_rectangle_element(self, element_data, frame_data):
        x, y = self.get_coordinates(element_data, frame_data)
        width, height = self.get_dimensions(element_data)
        fill_color = self.get_color(element_data)

        return elements.RectangleElement(
            self.counter.get_and_increment(Elements.RECTANGLE),
            x,
            y,
            width,
            height,
            fill_color)


    def parse_button_element(self, element_data, frame_data):
        x, y = self.get_coordinates(element_data, frame_data)
        width, height = self.get_dimensions(element_data)
        item_id = element_data["id"]
        counter = self.counter.get_and_increment(Elements.BUTTON)

        image_path = self.download_image(item_id,"button", counter)

        return elements.ButtonElement(
            counter,
            x,
            y,
            width,
            height,
            image_path)


    def parse_text_element(self, element_data, frame_data):
        x, y = self.get_coordinates(element_data, frame_data)
        width, height = self.get_dimensions(element_data)
        color = self.get_color(element_data)
        font, font_size = self.get_text_properties(element_data)
        text = element_data["characters"]
        text = text.replace("\n", "\\n")

        # x, y = x + (width / 2), y + (height / 2)

        return elements.TextElement(
            self.counter.get_and_increment(Elements.TEXT),
            x,
            y,
            width,
            height,
            color,
            font,
            font_size,
            text)


    def parse_text_entry(self, element_data, frame_data):
        x, y = self.get_coordinates(element_data, frame_data)
        width, height = self.get_dimensions(element_data)
        x, y = x + (width / 2), y + (height / 2)
        bg_color = self.get_color(element_data)
        counter = self.counter.get_and_increment(Elements.TEXTENTRY)

        item_id = element_data["id"]

        image_path = self.download_image(item_id,"entry", counter)

        try:
            corner_radius = element_data["cornerRadius"]
        except KeyError:
            corner_radius = 0

        if corner_radius > height / 2:
            corner_radius = height / 2

        entry_width = width - (corner_radius * 2)
        entry_height = height - 2

        entry_x, entry_y = self.get_coordinates(element_data, frame_data)
        entry_x = entry_x + corner_radius

        return elements.TextEntryElement(
            counter,
            x, 
            y, 
            width, 
            height, 
            entry_x, 
            entry_y, 
            entry_width, 
            entry_height, 
            elements.TEXT_INPUT_ELEMENT_TYPES[element_data["name"]], 
            bg_color, 
            image_path, 
            corner_radius)

    def parse_image_element(self, element_data, frame_data):
        x, y = self.get_coordinates(element_data, frame_data)
        width, height = self.get_dimensions(element_data)
        x, y = x + (width / 2), y + (height / 2)
        item_id = element_data["id"]
        counter = self.counter.get_and_increment(Elements.IMAGE)

        image_path = self.download_image(item_id,"image", counter)

        return elements.ImageElement(
            counter,
            x,
            y,
            width,
            height,
            image_path)
