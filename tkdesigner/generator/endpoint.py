import requests
# import re


class FigmaAPI:
    API_URL = "https://api.figma.com/v1"

    def __init__(self, token):
        self.token = token.strip()

    def get_files(self, file_key):
        response = requests.get(
            f"{self.API_URL}/files/{file_key}",
            headers={"X-FIGMA-TOKEN": self.token}
        )

        return response.json()

    def get_images(self, file_key, ids):
        response = requests.get(
            f"{self.API_URL}/images/{file_key}?ids={ids}",
            headers={"X-FIGMA-TOKEN": self.token}
        )

        return response.json()

    # @staticmethod
    # def extract(file_url: str):
    #     file_url = file_url.strip()
    #     match = re.fullmatch(
    #         r"https://www.figma.com/file/[^/]+(/[^/]+)?",
    #         file_url
    #     )
    #     match.groups()
