"""
Small utility functions.
"""
import requests


def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)

        return s[start:end]
    except ValueError:
        return ""


def download_image(url, image_path):
    response = requests.get(url)
    with open(image_path, "wb") as file:
        file.write(response.content)
