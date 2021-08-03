"""Utility classes and functions for Figma API endpoints.
"""
import requests


class Files:
    """https://www.figma.com/developers/api#files-endpoints
    """

    API_ENDPOINT_URL = "https://api.figma.com/v1"

    def __init__(self, token, file_key):
        self.token = token
        self.file_key = file_key

    def __str__(self):
        return f"Files {{ Token: {self.token}, File: {self.file_key} }}"

    def get_file(self) -> dict:
        try:
            response = requests.get(
                f"{self.API_ENDPOINT_URL}/files/{self.file_key}",
                headers={"X-FIGMA-TOKEN": self.token}
            )
        except ValueError:
            raise RuntimeError(
                "Invalid Input. Please check your input and try again.")
        except requests.ConnectionError:
            raise RuntimeError(
                "Tkinter Designer requires internet access to work.")
        else:
            return response.json()

    def get_image(self, item_id) -> str:
        response = requests.get(
            f"{self.API_ENDPOINT_URL}/images/{self.file_key}?ids={item_id}&scale=2",
            headers={"X-FIGMA-TOKEN": self.token}
        )

        return response.json()["images"][item_id]
