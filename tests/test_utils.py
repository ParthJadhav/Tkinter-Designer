import io

from PIL import Image

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


def test_download_image_is_resized_without_network(monkeypatch, tmp_path):
    content = io.BytesIO()
    Image.new("RGB", (20, 20), "red").save(content, format="PNG")
    image_bytes = content.getvalue()

    class Response:
        content = image_bytes

        @staticmethod
        def raise_for_status():
            return None

    monkeypatch.setattr(
        "tkdesigner.utils.requests.get", lambda *args, **kwargs: Response())
    target = tmp_path / "asset.png"

    download_image("https://example.com/asset.png", target, size=(10, 12))

    with Image.open(target) as image:
        assert image.size == (10, 12)
