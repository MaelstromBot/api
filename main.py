from fastapi import FastAPI, Request, Response
from dotenv import load_dotenv

from src.auth import APIAutheticator


load_dotenv()

app = FastAPI(docs_url=None)

@app.middleware("http")
async def authenticate(request: Request, call_next) -> Response:
    """Authenticate a backend API request."""

    request.state.auth = APIAutheticator(request)

    return await call_next(request)
