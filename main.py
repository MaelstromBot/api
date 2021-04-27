from asyncio import sleep

from dotenv import load_dotenv
from aiohttp import ClientSession
from fastapi import FastAPI, Request, Response, WebSocket

from src.database import Database
from src.ws import WebSocketManager
from src.auth import APIAutheticator


load_dotenv()

app = FastAPI(docs_url=None)
db = Database()
session = ClientSession()
wsm = WebSocketManager()

@app.on_event("startup")
async def startup() -> None:
    """Connect the database on startup."""

    await db.setup()

@app.middleware("http")
async def attach(request: Request, call_next) -> Response:
    """Attach the database, ws and ClientSession to the request."""

    request.state.db = db
    request.state.ws = wsm
    request.state.session = session

    return await call_next(request)

@app.middleware("http")
async def authenticate(request: Request, call_next) -> Response:
    """Authenticate a backend API request."""

    request.state.auth = APIAutheticator(request, db)

    return await call_next(request)

@app.get("/")
async def ping(request: Request) -> dict:
    """Ping the API. Returns a static response."""

    return {"status": "ok"}

@app.websocket("/")
async def ws_connect(ws: WebSocket) -> None:
    """Connect to the websocket."""

    if not await APIAutheticator.validate_ws(ws):
        return

    await wsm.connect(ws)

    await wsm.heartbeat()
