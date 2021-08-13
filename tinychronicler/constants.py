import logging
from typing import Dict

from uvicorn.logging import TRACE_LOG_LEVEL

# Image dimensions of file thumbnails
THUMBNAIL_SIZE = 1600, 1600

# MIME file types
ALLOWED_MIME_TYPES_AUDIO = ["audio/mpeg", "audio/x-wav"]
ALLOWED_MIME_TYPES_VIDEO = ["video/mp4", "video/mpeg"]
ALLOWED_MIME_TYPES_IMAGE = ["image/jpeg", "image/png"]

ALLOWED_MIME_TYPES = (
    ALLOWED_MIME_TYPES_IMAGE
    + ALLOWED_MIME_TYPES_VIDEO
    + ALLOWED_MIME_TYPES_AUDIO
)

# Log level options
LOG_LEVELS: Dict[str, int] = {
    "critical": logging.CRITICAL,
    "error": logging.ERROR,
    "warning": logging.WARNING,
    "info": logging.INFO,
    "debug": logging.DEBUG,
    "trace": TRACE_LOG_LEVEL,
}

# Path of SQLite database file
DATABASE_URL = "sqlite:///./tinychronicler-development.sqlite3"

# Path to jinja2 templates directory
TEMPLATES_DIR = "tinychronicler/web/templates"

# Path to static files served by http server
STATIC_DIR = "tinychronicler/web/static"

# Path to directory for uploaded user files
UPLOADS_DIR = "uploads"

# Path to musical "modules" directory
MIDI_MODULES_DIR = "midi"
