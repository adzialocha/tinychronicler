from tinychronicler.constants import (
    ALLOWED_MIME_TYPES_AUDIO,
    ALLOWED_MIME_TYPES_IMAGE,
    ALLOWED_MIME_TYPES_VIDEO,
)
from tinychronicler.server.files import random_file

from .audio import play_audio, stop_audio
from .led import run_test_sequence
from .printer import print_test_page
from .video import play_video, show_image, stop_video_or_image


async def run_test(test_id: str):
    if test_id == "print-test-page":
        print_test_page()
    elif test_id == "play-random-video":
        file = random_file(ALLOWED_MIME_TYPES_VIDEO)
        if file is None:
            raise Exception("Could not find any video file")
        play_video(file)
    elif test_id == "play-random-audio":
        file = random_file(ALLOWED_MIME_TYPES_AUDIO)
        if file is None:
            raise Exception("Could not find any audio file")
        play_audio(file)
    elif test_id == "stop-audio":
        stop_audio()
    elif test_id == "show-random-image":
        file = random_file(ALLOWED_MIME_TYPES_IMAGE)
        if file is None:
            raise Exception("Could not find any image file")
        show_image(file)
    elif test_id == "stop-video":
        stop_video_or_image()
    elif test_id == "run-led-test":
        await run_test_sequence()
    else:
        raise Exception("Unknown test id")
