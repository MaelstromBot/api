from os import getenv

from fastapi import Request, WebSocket
from fastapi.exceptions import HTTPException

from .database import Database


class APIAutheticator:
    def __init__(self, request: Request, db: Database):
        """Authenticate backend API requests.

        Args:
            request (Request): The request to authenticate.
            db (Database): The database to use for auth lookups.
        """

        self.request = request

    def validate(self):
        if self.request.headers.get("Authorization") != getenv("API_TOKEN"):
            raise HTTPException(401, "Invalid auth.")

    @staticmethod
    async def validate_ws(ws: WebSocket):
        if ws.headers.get("Authorization") != getenv("API_TOKEN"):
            await ws.close(4001)
            return False
        await ws.accept()
        return True
