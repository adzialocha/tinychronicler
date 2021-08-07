from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from tinychronicler.api import api
from tinychronicler.database import database
from tinychronicler.web import web

from .constants import STATIC_DIR

server = FastAPI()

# Add static files for webpage
server.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Mount routes
server.include_router(web)
server.include_router(api)


@server.on_event("startup")
async def startup():
    await database.connect()


@server.on_event("shutdown")
async def shutdown():
    await database.disconnect()
