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
    "ar": "models/vosk-model-ar-mgb2-0.4",
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
    arabic = "ar"
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
MODULE_DURATION = 4.0  # 2 bars, 120bpm (quarters)

# Define the MIDI modules for the first voice. We manually specify the duration
# as guessing it is always somewhat not working when we want to end with a
# pause.
MIDI_MODULES_1 = [
    {
        "file": "human/Mod-1.mid",
        "duration": MODULE_DURATION,
        "character": "a",
    },
    {
        "file": "human/Mod-2.mid",
        "duration": MODULE_DURATION,
        "character": "b",
    },
    {
        "file": "human/Mod-3.mid",
        "duration": MODULE_DURATION,
        "character": "c",
    },
    {
        "file": "human/Mod-4.mid",
        "duration": MODULE_DURATION,
        "character": "d",
    },
    {
        "file": "human/Mod-5.mid",
        "duration": MODULE_DURATION,
        "character": "e",
    },
    {
        "file": "human/Mod-6.mid",
        "duration": MODULE_DURATION,
        "character": "f",
    },
    {
        "file": "human/Mod-7.mid",
        "duration": MODULE_DURATION,
        "character": "g",
    },
    {
        "file": "human/Mod-8.mid",
        "duration": MODULE_DURATION,
        "character": "h",
    },
    {
        "file": "human/Mod-9.mid",
        "duration": MODULE_DURATION,
        "character": "i",
    },
    {
        "file": "human/Mod-10.mid",
        "duration": MODULE_DURATION,
        "character": "j",
    },
    {
        "file": "human/Mod-11.mid",
        "duration": MODULE_DURATION,
        "character": "k",
    },
    {
        "file": "human/Mod-12.mid",
        "duration": MODULE_DURATION,
        "character": "l",
    },
    {
        "file": "human/Mod-13.mid",
        "duration": MODULE_DURATION,
        "character": "m",
    },
    {
        "file": "human/Mod-14.mid",
        "duration": MODULE_DURATION,
        "character": "n",
    },
    {
        "file": "human/Mod-15.mid",
        "duration": MODULE_DURATION,
        "character": "o",
    },
    {
        "file": "human/Mod-16.mid",
        "duration": MODULE_DURATION,
        "character": "p",
    },
    {
        "file": "human/Mod-17.mid",
        "duration": MODULE_DURATION,
        "character": "q",
    },
    {
        "file": "human/Mod-18.mid",
        "duration": MODULE_DURATION,
        "character": "r",
    },
]

# Define the MIDI modules for the second voice
MIDI_MODULES_2 = [
    {
        "file": "robot/TC-Mod-1.mid",
        "duration": MODULE_DURATION,
        "character": "A",
    },
    {
        "file": "robot/TC-Mod-2.mid",
        "duration": MODULE_DURATION,
        "character": "B",
    },
    {
        "file": "robot/TC-Mod-3.mid",
        "duration": MODULE_DURATION,
        "character": "C",
    },
    {
        "file": "robot/TC-Mod-4.mid",
        "duration": MODULE_DURATION,
        "character": "D",
    },
    {
        "file": "robot/TC-Mod-5.mid",
        "duration": MODULE_DURATION,
        "character": "E",
    },
    {
        "file": "robot/TC-Mod-6.mid",
        "duration": MODULE_DURATION,
        "character": "F",
    },
    {
        "file": "robot/TC-Mod-7.mid",
        "duration": MODULE_DURATION,
        "character": "G",
    },
    {
        "file": "robot/TC-Mod-8.mid",
        "duration": MODULE_DURATION,
        "character": "H",
    },
    {
        "file": "robot/TC-Mod-9.mid",
        "duration": MODULE_DURATION,
        "character": "I",
    },
    {
        "file": "robot/TC-Mod-10.mid",
        "duration": MODULE_DURATION,
        "character": "J",
    },
    {
        "file": "robot/TC-Mod-11.mid",
        "duration": MODULE_DURATION,
        "character": "K",
    },
    {
        "file": "robot/TC-Mod-12.mid",
        "duration": MODULE_DURATION,
        "character": "L",
    },
    {
        "file": "robot/TC-Mod-13.mid",
        "duration": MODULE_DURATION,
        "character": "M",
    },
    {
        "file": "robot/TC-Mod-14.mid",
        "duration": MODULE_DURATION,
        "character": "N",
    },
    {
        "file": "robot/TC-Mod-15.mid",
        "duration": MODULE_DURATION,
        "character": "O",
    },
    {
        "file": "robot/TC-Mod-16.mid",
        "duration": MODULE_DURATION,
        "character": "P",
    },
    {
        "file": "robot/TC-Mod-17.mid",
        "duration": MODULE_DURATION,
        "character": "Q",
    },
    {
        "file": "robot/TC-Mod-18.mid",
        "duration": MODULE_DURATION,
        "character": "R",
    },
]
