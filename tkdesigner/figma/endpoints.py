"""Utility classes and functions for Figma API endpoints."""

import requests


class FigmaAPIError(RuntimeError):
    """Raised when the Figma API returns an error response."""


class Files:
    """https://www.figma.com/developers/api#files-endpoints
    """

    API_ENDPOINT_URL = "https://api.figma.com/v1"

    def __init__(self, token, file_key):
        self.token = token
        self.file_key = file_key

    def __str__(self):
        return f"Files {{ Token: {self.token}, File: {self.file_key} }}"

    def _get_json(self, path, *, params=None) -> dict:
        try:
            response = requests.get(
                f"{self.API_ENDPOINT_URL}{path}",
                headers={"X-FIGMA-TOKEN": self.token},
                params=params,
                timeout=30,
            )
        except requests.ConnectionError:
            raise RuntimeError(
                "Tkinter Designer requires internet access to work.")
        except requests.RequestException as exc:
            raise RuntimeError(f"Could not connect to Figma: {exc}") from exc

        try:
            payload = response.json()
        except ValueError as exc:
            raise FigmaAPIError(
                f"Figma returned an invalid response with status "
                f"{response.status_code}.") from exc

        if response.status_code >= 400:
            raise FigmaAPIError(self._format_error(response.status_code, payload))

        if not isinstance(payload, dict):
            raise FigmaAPIError("Figma returned an unexpected response.")

        return payload

    def _format_error(self, status_code, payload) -> str:
        message = payload.get("err") or payload.get("message") or payload.get("status")
        if status_code == 401:
            return "Figma rejected the token. Create a new personal access token and try again."
        if status_code == 403:
            return "Figma denied access to this file. Check that the file is shared with the token owner."
        if status_code == 404:
            return "Figma could not find that file. Check the file URL."
        if status_code == 429:
            return "Figma API rate limit exceeded. Wait for the limit to reset or use a token with quota."
        if message:
            return f"Figma API error ({status_code}): {message}"
        return f"Figma API error ({status_code})."

    def get_file(self) -> dict:
        payload = self._get_json(f"/files/{self.file_key}")
        if "document" not in payload:
            raise FigmaAPIError(
                "Figma response did not include a document. Check the token, "
                "file URL, and API quota.")
        return payload

    def get_image(self, item_id) -> str:
        payload = self._get_json(
            f"/images/{self.file_key}",
            params={"ids": item_id, "scale": 2, "format": "png"},
        )

        image_url = payload.get("images", {}).get(item_id)
        if not image_url:
            raise FigmaAPIError(
                f"Figma could not export image data for element `{item_id}`.")

        return image_url
