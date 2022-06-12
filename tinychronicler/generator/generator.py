import os
from typing import List

from tinychronicler.constants import (
    ALLOWED_MIME_TYPES_AUDIO,
    ALLOWED_MIME_TYPES_IMAGE,
    ALLOWED_MIME_TYPES_VIDEO,
    MIDI_MODULES_DIR,
)
from tinychronicler.database import schemas

from .midi import get_midi_files
from .movements import MOVEMENTS
from .notes import generate_notes
from .parameters import generate_parameters


def generate_composition(files: List[schemas.File]):
    # Separate media files by type
    audio_files = [f.path for f in files if f.mime in ALLOWED_MIME_TYPES_AUDIO]
    video_files = [f.path for f in files if f.mime in ALLOWED_MIME_TYPES_VIDEO]
    image_files = [f.path for f in files if f.mime in ALLOWED_MIME_TYPES_IMAGE]
    midi_files = get_midi_files(MIDI_MODULES_DIR)

    # Load audio file which serves as the base for this composition. Every
    # chronicle holds one only audio file
    assert len(audio_files) == 1
    audio_file = audio_files[0]
    assert os.path.exists(audio_file)

    # Generate a MIDI score and list of modules from audio file. A module is a
    # predetermined short sequence of notes
    (notes, modules) = generate_notes(audio_file, midi_files)

    # Generate parameters which determine the used sounds and media of the
    # composition
    parameters = generate_parameters(modules, MOVEMENTS)

    return {
        "notes": notes,
        "parameters": parameters,
    }
