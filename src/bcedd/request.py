"""Handles HTTP requests."""
from typing import Optional

import requests


class RequestHandler:
    """Handles HTTP requests."""

    def __init__(
        self,
        url: str,
        headers: Optional[dict[str, str]] = None,
        data: Optional["bytes"] = None,
    ):
        """Initializes a new instance of the RequestHandler class.

        Args:
            url (str): URL to request.
            headers (Optional[dict[str, str]], optional): Headers to send with the request. Defaults to None.
            data (Optional[bytes], optional): Data to send with the request. Defaults to None.
        """
        if data is None:
            data = bytes()
        self.url = url
        self.headers = headers
        self.data = data

    def get(self) -> requests.Response:
        """Sends a GET request.

        Returns:
            requests.Response: Response from the server.
        """
        return requests.get(self.url, headers=self.headers, timeout=30)

    def post(self) -> requests.Response:
        """Sends a POST request.

        Returns:
            requests.Response: Response from the server.
        """
        return requests.post(self.url, headers=self.headers, data=self.data, timeout=30)
