from dotenv import load_dotenv
from aiohttp import ClientSession
from fastapi import FastAPI, Request, Response

from src.database import Database
from src.auth import APIAutheticator


load_dotenv()

app = FastAPI(docs_url=None)
db = Database()
session = ClientSession()

@app.on_event("startup")
async def startup() -> None:
    """Connect the database on startup."""

    await db.setup()

@app.middleware("http")
async def attach(request: Request, call_next) -> Response:
    """Attach the database and ClientSession to the request."""

    request.state.db = db
    request.state.session = session

    return await call_next(request)

@app.middleware("http")
async def authenticate(request: Request, call_next) -> Response:
    """Authenticate a backend API request."""

    request.state.auth = APIAutheticator(request)

    return await call_next(request)

@app.get("/")
async def ping(request: Request) -> dict:
    """Ping the API. Returns a static response."""

    return {"status": "ok"}
