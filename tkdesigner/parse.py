"""
Module to handle parsing Figma elements.
"""

import os
from typing import Dict, List
import uuid

import requests

from tkdesigner import elements


class FigmaParser():
    def __init__(self, token: str, file_id: str, asset_dir: str):
        self.token = token
        self.file_id = file_id
        self.asset_dir = asset_dir

        
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

    
    def download_image(self, item_id):
        """
        Download the image for the `item_id` and save it to the asset directory.

        Returns:
            The file path of the saved image.
        """

        def generate_image_id(length=16):
            return str(uuid.uuid4())[:16]

        response = requests.get(
            f"https://api.figma.com/v1/images/{self.file_id}?ids={item_id}",
            headers={"X-FIGMA-TOKEN": f"{self.token}"})

        image_response = requests.get(response.json()["images"][item_id])
        image_path = os.path.join(self.asset_dir, f"img-{generate_image_id()}.png")
        with open(image_path, "wb") as file:
            file.write(image_response.content)
        
        return image_path

    
    def parse_gui(self, data):
        frame_data = data["document"]["children"][0]["children"][0]

        width, height = self.get_dimensions(frame_data)

        try:
            bg_color = self.get_color(frame_data)
        except Exception:
            # If the background colour can't be parsed, fallback to white
            bg_color = "#FFFFFF"

        parsed_elements: List[elements.Element] = []
        for element_data in frame_data["children"]:
            element_name = element_data["name"]
            element_type = element_data["type"]

            parsed_element = None
            if element_name == "Rectangle":
                parsed_element = self.parse_rectangle_element(element_data, frame_data)
            elif element_name == "Button":
                parsed_element = self.parse_button_element(element_data, frame_data)
            elif element_name in ("TextBox", "TextArea"):
                parsed_element = self.parse_text_entry(element_data, frame_data)
            elif element_name == "Image":
                parsed_element = self.parse_image_element(element_data, frame_data)
            elif element_type == "TEXT":
                parsed_element = self.parse_text_element(element_data, frame_data)
            else:
                raise NotImplementedError(f"Element with the name: `{element_name}` cannot be parsed.")

            parsed_elements.append(parsed_element)

        return elements.FigmaFrame(
            width,
            height,
            self.asset_dir,
            bg_color,
            parsed_elements)
            

    def parse_frame(self, frame_data: dict):
        width, height = self.get_dimensions(frame_data)

        try:
            bg_color = self.get_color(frame_data)
        except Exception:
            # If the background colour can't be parsed, fallback to white
            bg_color = "#FFFFFF"

        return elements.FigmaFrame(width, height, self.asset_dir, bg_color)


    def parse_rectangle_element(self, element_data, frame_data):
        x, y = self.get_coordinates(element_data, frame_data)
        width, height = self.get_dimensions(element_data)
        fill_color = self.get_color(element_data)

        return elements.RectangleElement(x, y, width, height, fill_color)


    def parse_button_element(self, element_data, frame_data):
        x, y = self.get_coordinates(element_data, frame_data)
        width, height = self.get_dimensions(element_data)
        item_id = element_data["id"]

        image_path = self.download_image(item_id)

        return elements.ButtonElement(x, y, width, height, image_path)

    def parse_text_element(self, element_data, frame_data):
        x, y = self.get_coordinates(element_data, frame_data)
        width, height = self.get_dimensions(element_data)
        color = self.get_color(element_data)
        font, font_size = self.get_text_properties(element_data)
        text = element_data["characters"]
        text = text.replace("\n", "\\n")

        x, y = x + (width / 2), y + (height / 2)

        return elements.TextElement(x, y, width, height, color, font, font_size, text)


    def parse_text_entry(self, element_data, frame_data):
        x, y = self.get_coordinates(element_data, frame_data)
        width, height = self.get_dimensions(element_data)
        x, y = x + (width / 2), y + (height / 2)
        bg_color = self.get_color(element_data)

        item_id = element_data["id"]

        image_path = self.download_image(item_id)

        try:
            corner_radius = element_data["cornerRadius"]
        except KeyError:
            corner_radius = 0

        if corner_radius > height / 2:
            corner_radius = height / 2

        width = width - (corner_radius * 2)
        height = height - 2

        x, y = self.get_coordinates(element_data, frame_data)
        x = x + corner_radius

        return elements.TextEntryElement(x, y, width, height, elements.TEXT_INPUT_ELEMENT_TYPES[element_data["name"]], bg_color, image_path, corner_radius)

    def parse_image_element(self, element_data, frame_data):
        x, y = self.get_coordinates(element_data, frame_data)
        width, height = self.get_dimensions(element_data)
        x, y = x + (width / 2), y + (height / 2)
        item_id = element_data["id"]

        image_path = self.download_image(item_id)

        return elements.ImageElement(x, y, width, height, image_path)
