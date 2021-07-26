import os
from tkdesigner.constants import ASSETS_PATH
from tkdesigner.utils import find_between, download_image


def test_assets_path():
    assert ASSETS_PATH == "./assets"


def test_find_between():
    assert find_between("abcdefg", "c", "g") == "def"
    assert find_between("http://someurl.com/?q=somequery",
                        "/",
                        "?"
                        ) == "/someurl.com/"


def test_download_image():
    url = "https://www.python.org/static/opengraph-icon-200x200.png"
    download_image(url, "test.png")
    assert os.path.exists("test.png")
    os.remove("test.png")
