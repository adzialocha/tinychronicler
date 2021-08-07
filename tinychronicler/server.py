from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from tinychronicler.constants import STATIC_DIR
from tinychronicler.database import database
from tinychronicler.router import router

server = FastAPI()

# Add static files for webpage
server.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Mount routes
server.include_router(router)


@server.on_event("startup")
async def startup():
    await database.connect()


@server.on_event("shutdown")
async def shutdown():
    await database.disconnect()
