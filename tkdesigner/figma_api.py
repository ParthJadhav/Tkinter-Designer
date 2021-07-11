import requests

from tkdesigner import utils, errors


class FigmaUser:
    def __init__(self, token):
        self.token = token

    def get_files(self, file_key):
        try:
            response = requests.get(
                f"{self.API_URL}/files/{file_key}",
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

    def get_images(self, file_key, ids):
        response = requests.get(
            f"{self.API_URL}/images/{file_key}?ids={ids}",
            headers={"X-FIGMA-TOKEN": self.token}
        )

        return response.json()


def get_file_and_id(token, url):
    token = token.strip()
    url = url.strip()
    file_id = utils.find_between(url, "file/", "/")
    user = FigmaUser(token)
    response_json = user.get_files(file_id)
    return response_json, file_id
