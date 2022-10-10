from fastapi.staticfiles import StaticFiles
from fastapi_offline import FastAPIOffline
from fastapi_pagination import add_pagination

from tinychronicler.constants import STATIC_DIR, UPLOADS_DIR, SAMPLES_DIR
from tinychronicler.database import database
from tinychronicler.io.midi import open_midi_ports, close_midi_ports

from .files import create_uploads_dir
from .router import router
from .ws import WebSocketConnectionManager

# Use FastAPIOffline as we don't want to load OpenAPI static files from CDNs
server = FastAPIOffline()

# Add static files for webpage
server.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Server audio samples for MIDI instruments
server.mount("/samples",
             StaticFiles(directory=SAMPLES_DIR), name="samples")

# Serve uploaded user files
create_uploads_dir()
server.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")

# Mount routes
server.include_router(router)

# Install FastAPI pagination extension after mounting routes
add_pagination(server)


@server.on_event("startup")
async def startup():
    # This is a little strange, but the connection manager is a singleton and
    # we have to make sure to initialise it _after_ the underlying asyncio
    # event loop is established by the fastapi runtime.
    WebSocketConnectionManager()

    # Connect to the database
    await database.connect()

    # _Now_ start the MIDI runtime. We have to make sure its _after_ the
    # connection manager. As the MIDI methods also use it
    open_midi_ports()


@server.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    close_midi_ports()
