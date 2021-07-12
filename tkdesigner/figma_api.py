from tkdesigner import errors
import requests


class FigmaUser:
    API_ENDPOINT = "https://api.figma.com/v1"

    def __init__(self, token):
        self.token = token

    def __str__(self):
        return f"FigmaUser {{ Token: {self.token} }} "

    def get_files(self, file_key):
        try:
            response = requests.get(
                f"{self.API_ENDPOINT}/files/{file_key}",
                headers={"X-FIGMA-TOKEN": self.token}
            )
        except ValueError as e:
            raise errors.UserError(
                e, "Invalid Input. Please check your input and try again.")
        except requests.ConnectionError as e:
            raise errors.UserError(
                e, "Tkinter Designer requires internet access to work.")
        else:
            return response.json()

    def get_images(self, file_key, item_id):
        response = requests.get(
            f"{self.API_ENDPOINT}/images/{file_key}?ids={item_id}",
            headers={"X-FIGMA-TOKEN": self.token}
        )

        return response.json()["images"][item_id]
