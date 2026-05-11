import os
from tkdesigner.constants import ASSETS_PATH
from tkdesigner.utils import find_between, download_image, parse_figma_url


def test_assets_path():
    assert ASSETS_PATH == "./assets"


def test_find_between():
    assert find_between("abcdefg", "c", "g") == "def"
    assert find_between("http://someurl.com/?q=somequery",
                        "/",
                        "?"
                        ) == "/someurl.com/"


def test_parse_figma_url_supports_current_figma_links():
    reference = parse_figma_url(
        "https://www.figma.com/design/ABCdef123456/My-App?"
        "node-id=4-41&t=token")

    assert reference.file_key == "ABCdef123456"
    assert reference.node_id == "4:41"


def test_parse_figma_url_supports_legacy_file_links():
    reference = parse_figma_url(
        "https://www.figma.com/file/W3ekOTW6bFvGiUrndEpC4S/"
        "Untitled?node-id=4%3A41")

    assert reference.file_key == "W3ekOTW6bFvGiUrndEpC4S"
    assert reference.node_id == "4:41"


def test_download_image():
    url = "https://www.python.org/static/opengraph-icon-200x200.png"
    download_image(url, "test.png")
    assert os.path.exists("test.png")
    os.remove("test.png")
