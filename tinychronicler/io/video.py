from loguru import logger

from tinychronicler.io.osc import send_message


def play_video(
    video_file_path: str,
    seek: int = 0,
    duration: int = 10,
    muted: bool = False
):
    logger.debug("Play video file @ {}".format(video_file_path))
    send_message("/video", video_file_path, seek, duration)


def show_image(
    image_file_path: str,
    duration: int = 10,
):
    logger.debug("Show image file @ {}".format(image_file_path))
    send_message("/image", image_file_path, duration)


def stop_video_or_image():
    send_message("/video/reset")
