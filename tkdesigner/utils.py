"""
Small utility functions.
"""
import requests
from PIL import Image
import io


def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)

        return s[start:end]
    except ValueError:
        return ""


def download_image(url, image_path):
    response = requests.get(url)
    content = io.BytesIO(response.content)
    im = Image.open(content)
    im = im.resize((round(im.size[0]*0.5), round(im.size[1]*0.5)), Image.ANTIALIAS)
    with open(image_path, "wb") as file:
        im.save(file)
