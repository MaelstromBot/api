from os import getenv

from fastapi import Request
from fastapi.exceptions import HTTPException


class APIAutheticator:
    def __init__(self, request: Request):
        """Authenticate backend API requests.

        Args:
            request (Request): The request to authenticate.
        """

        self.request = request

    def validate(self):
        if self.request.headers.get("Authorization") != getenv("API_TOKEN"):
            raise HTTPException(401, "Invalid auth.")
