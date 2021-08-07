from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_pagination import add_pagination

from .constants import STATIC_DIR
from .database import database
from .router import router

server = FastAPI()

# Add static files for webpage
server.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Mount routes
server.include_router(router)

# Install FastAPI pagination extension
add_pagination(server)


@server.on_event("startup")
async def startup():
    await database.connect()


@server.on_event("shutdown")
async def shutdown():
    await database.disconnect()
