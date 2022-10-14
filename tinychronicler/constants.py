import logging
from enum import Enum
from typing import Dict

from uvicorn.logging import TRACE_LOG_LEVEL

# Image dimensions of file thumbnails
THUMBNAIL_SIZE = 1600, 1600

# MIME file types
ALLOWED_MIME_TYPES_AUDIO = [
    "audio/mpeg",
    "audio/x-wav",
]
ALLOWED_MIME_TYPES_VIDEO = [
    "video/mp4",
    "video/mpeg",
    "video/quicktime",
    "video/x-msvideo",
    "video/x-matroska",
    "video/x-ms-wmv",
]
ALLOWED_MIME_TYPES_IMAGE = [
    "image/jpeg",
    "image/png",
]

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

# Paths to trained machine learning model for speech recognition
MODEL_PATHS = {
    "cn": "models/vosk-model-small-cn-0.22",
    "de": "models/vosk-model-small-de-0.15",
    "en": "models/vosk-model-small-en-us-0.15",
    "es": "models/vosk-model-small-es-0.42",
    "fr": "models/vosk-model-small-fr-0.22",
    "it": "models/vosk-model-small-it-0.22",
    "ja": "models/vosk-model-small-ja-0.22",
    "pl": "models/vosk-model-small-pl-0.22",
    "ru": "models/vosk-model-small-ru-0.22",
}


class LanguageEnum(str, Enum):
    # Enum of possible language selections
    chinese = "cn"
    german = "de"
    english = "en"
    spanish = "es"
    french = "fr"
    italian = "it"
    japanese = "ja"
    polish = "pl"
    russian = "ru"


# Grid size of the composition (in seconds)
GRID_SIZE = 0.0625  # 32th note in 120bpm (quarters)

# Duration of each module
#
# Maybe this little chart helps:
#
# 120bpm quarters
# Note Duration (seconds)
# -----------------------
# 1    2.0
# 2    1.0
# 4    0.5
# 8    0.25
# 16   0.125
# 32   0.0625
MODULE_DURATION = 0.375  # @TODO 2 bars, 120bpm (quarters)

# Define the MIDI modules for the first voice. We manually specify the duration
# as guessing it is always somewhat not working when we want to end with a
# pause.
MIDI_MODULES_1 = [
    {
        "file": "module-3notes-1.mid",
        "duration": MODULE_DURATION,
        "character": "A",
    },
    {
        "file": "module-3notes-2.mid",
        "duration": MODULE_DURATION,
        "character": "B",
    },
    {
        "file": "module-3notes-3.mid",
        "duration": MODULE_DURATION,
        "character": "C",
    },
]

# Define the MIDI modules for the second voice
MIDI_MODULES_2 = [
    {
        "file": "module-3notes-4.mid",
        "duration": MODULE_DURATION,
        "character": "D",
    },
    {
        "file": "module-3notes-5.mid",
        "duration": MODULE_DURATION,
        "character": "E",
    },
    {
        "file": "module-3notes-6.mid",
        "duration": MODULE_DURATION,
        "character": "F",
    },
    {
        "file": "module-3notes-7.mid",
        "duration": MODULE_DURATION,
        "character": "G",
    },
]
