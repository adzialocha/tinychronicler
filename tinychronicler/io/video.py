from loguru import logger

from tinychronicler.io.osc import send_message


def play_video(video_file_path: str, seek: float = 0.0):
    logger.debug("Play video file @ {}".format(video_file_path))
    send_message("/video", video_file_path, seek)


def show_image(image_file_path: str):
    logger.debug("Show image file @ {}".format(image_file_path))
    send_message("/image", image_file_path)


def stop_video_or_image():
    send_message("/video/reset")
