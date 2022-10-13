from loguru import logger

from tinychronicler.io.osc import send_message


def play_audio(audio_file_path: str):
    logger.debug("Play audio file @ {}".format(audio_file_path))
    send_message("/audio", audio_file_path)


def stop_audio():
    send_message("/audio/reset")


def mute_audio():
    send_message("/audio/mute")


def unmute_audio():
    send_message("/audio/mute")


def play_note(instrument: str, note: int):
    send_message("/note/{}".format(str), note)
