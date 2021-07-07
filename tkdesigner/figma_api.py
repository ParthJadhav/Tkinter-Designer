import requests

from tkdesigner import utils, errors, parse


def get_file_and_id(token, url):
    token = token.strip()
    url = url.strip()
    file_id = utils.find_between(url, "file/", "/")

    try:
        response = requests.get(
            f"https://api.figma.com/v1/files/{file_id}",
            headers={"X-FIGMA-TOKEN": token})
    except ValueError as e:
        raise errors.UserError(e, "Invalid Input. Please check your input and try again.")
    except requests.ConnectionError as e:
        raise errors.UserError(e, "Tkinter Designer requires internet access to work.")

    return response.json(), file_id
