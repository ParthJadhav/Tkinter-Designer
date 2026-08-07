"""Utility classes and functions for Figma API endpoints."""

from typing import Iterable

import requests

from tkdesigner import __version__


class FigmaAPIError(RuntimeError):
    """Raised when the Figma API returns an error response."""


class Files:
    """https://www.figma.com/developers/api#files-endpoints
    """

    API_ENDPOINT_URL = "https://api.figma.com/v1"

    def __init__(self, token, file_key):
        self.token = token
        self.file_key = file_key
        self._image_urls = {}

    def __str__(self):
        return f"Files {{ Token: configured, File: {self.file_key} }}"

    def _get_json(self, path, *, params=None) -> dict:
        try:
            response = requests.get(
                f"{self.API_ENDPOINT_URL}{path}",
                headers={
                    "X-FIGMA-TOKEN": self.token,
                    "User-Agent": f"Tkinter-Designer/{__version__}",
                },
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
            raise FigmaAPIError(
                self._format_error(
                    response.status_code,
                    payload,
                    headers=getattr(response, "headers", {}),
                )
            )

        if not isinstance(payload, dict):
            raise FigmaAPIError("Figma returned an unexpected response.")

        return payload

    def _format_error(self, status_code, payload, *, headers=None) -> str:
        message = payload.get("err") or payload.get("message") or payload.get("status")
        if status_code == 401:
            return "Figma rejected the token. Create a new personal access token and try again."
        if status_code == 403:
            return "Figma denied access to this file. Check that the file is shared with the token owner."
        if status_code == 404:
            return "Figma could not find that file. Check the file URL."
        if status_code == 429:
            retry_after = (headers or {}).get("Retry-After")
            wait_hint = (
                f" Retry after {retry_after} seconds."
                if retry_after else " Wait for the limit to reset."
            )
            return f"Figma API rate limit exceeded.{wait_hint}"
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

    def get_images(self, item_ids: Iterable[str]) -> dict:
        """Resolve many export URLs with a small number of API requests.

        Figma accepts comma-separated node IDs. Batching here replaces the old
        one-request-per-element behavior, which was both slow and prone to rate
        limiting on real designs.
        """
        unique_ids = list(dict.fromkeys(str(item_id) for item_id in item_ids))
        missing_ids = [
            item_id for item_id in unique_ids if item_id not in self._image_urls
        ]

        chunk_size = 100
        for index in range(0, len(missing_ids), chunk_size):
            chunk = missing_ids[index:index + chunk_size]
            payload = self._get_json(
                f"/images/{self.file_key}",
                params={"ids": ",".join(chunk), "scale": 2, "format": "png"},
            )
            images = payload.get("images") or {}
            self._image_urls.update(
                {item_id: images.get(item_id) for item_id in chunk}
            )

        return {item_id: self._image_urls.get(item_id) for item_id in unique_ids}

    def get_image(self, item_id) -> str:
        image_url = self.get_images([item_id]).get(item_id)
        if not image_url:
            raise FigmaAPIError(
                f"Figma could not export image data for element `{item_id}`.")

        return image_url
