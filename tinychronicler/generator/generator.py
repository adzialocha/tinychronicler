import os
import random
from typing import List

from tinychronicler.constants import (
    ALLOWED_MIME_TYPES_AUDIO,
    ALLOWED_MIME_TYPES_IMAGE,
    ALLOWED_MIME_TYPES_VIDEO,
)
from tinychronicler.database import schemas

from .movements import (
    MOVEMENTS,
    MOVEMENTS_WITHOUT_PHOTO,
    MOVEMENTS_WITHOUT_VIDEO,
    MOVEMENTS_WITHOUT_VIDEO_AND_PHOTO,
)
from .notes import generate_notes
from .parameters import generate_parameters


def generate_composition(files: List[schemas.File]):
    # Separate media files by type
    audio_files = [f.path for f in files if f.mime in ALLOWED_MIME_TYPES_AUDIO]
    video_files = [f.path for f in files if f.mime in ALLOWED_MIME_TYPES_VIDEO]
    image_files = [f.path for f in files if f.mime in ALLOWED_MIME_TYPES_IMAGE]

    # Load audio file which serves as the base for this composition. Every
    # chronicle holds one only audio file
    assert len(audio_files) == 1
    audio_file = audio_files[0]
    assert os.path.exists(audio_file)

    # Generate a MIDI score and list of modules from audio file. A module is a
    # predetermined short sequence of notes
    (notes, module_indices) = generate_notes(audio_file)

    # Shuffle the files before, so the outcome is always a little different
    random.shuffle(video_files)
    random.shuffle(image_files)

    # Generate parameters which determine the used sounds and media of the
    # composition
    has_images = len(image_files) > 0
    has_videos = len(video_files) > 0
    movements = MOVEMENTS
    if not has_images and has_videos:
        movements = MOVEMENTS_WITHOUT_PHOTO
    elif has_images and not has_videos:
        movements = MOVEMENTS_WITHOUT_VIDEO
    elif not has_images and not has_videos:
        movements = MOVEMENTS_WITHOUT_VIDEO_AND_PHOTO
    parameters = generate_parameters(
        module_indices[0], movements, video_files, image_files)

    return {
        "notes": notes,
        "parameters": parameters,
    }
