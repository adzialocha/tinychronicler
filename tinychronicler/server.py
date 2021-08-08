from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_pagination import add_pagination

from .constants import STATIC_DIR, UPLOADS_DIR
from .database import database
from .files import create_uploads_dir
from .router import router

server = FastAPI()

# Add static files for webpage
server.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Serve uploaded user files
create_uploads_dir()
server.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")

# Mount routes
server.include_router(router)

# Install FastAPI pagination extension after mounting routes
add_pagination(server)


@server.on_event("startup")
async def startup():
    await database.connect()


@server.on_event("shutdown")
async def shutdown():
    await database.disconnect()
