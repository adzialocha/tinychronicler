import asyncio

from loguru import logger

from tinychronicler.constants import MODULE_DURATION
from tinychronicler.database import schemas
from tinychronicler.io import (
    play_video, show_image, play_audio, stop_video_or_image,
    mute_audio, unmute_audio, play_note)

tasks = set()


def trigger_audio(media: str):
    logger.debug("Trigger audio: {} {}", media)
    play_audio(media)


def trigger_video(media: str, media_from: float):
    logger.debug("Trigger video: {} {}", media, media_from)
    play_video(media, media_from)


def trigger_photo(media: str):
    logger.debug("Trigger photo: {}", media)
    show_image(media)


def trigger_photo_and_video_stop():
    logger.debug("Stop video / photo")
    stop_video_or_image()


def mute_narrator():
    logger.debug("Mute narrator")
    mute_audio()


def unmute_narrator():
    logger.debug("Unmute narrator")
    unmute_audio()


def trigger_note(voice: str, note: int):
    logger.debug("Trigger note {} {}", voice, note)
    play_note(voice, note)


async def perform_voice(voice: str, notes):
    last_start = 0
    try:
        for note in notes:
            delay = note[1] - last_start
            if delay > 0:
                await asyncio.sleep(delay)
            trigger_note(voice, note[0])
            last_start = note[1]
    except asyncio.CancelledError:
        pass


def prepare_voice_performance(voice: str, notes, start_time, end_time):
    to_be_performed = []
    for note in notes:
        if note[1] >= start_time and note[2] <= end_time:
            to_be_performed.append(
                (note[0], note[1] - start_time, note[2] - start_time))
    if len(to_be_performed) > 0:
        # Play notes in separate task
        task = asyncio.create_task(perform_voice(voice, to_be_performed))
        tasks.add(task)
        task.add_done_callback(tasks.discard)


async def perform(audio_file_path: str,
                  composition_data: schemas.CompositionData,
                  is_demo=False):
    # Composition data
    current_module_index = 0
    modules = composition_data["parameters"]
    notes = composition_data["notes"]
    notes_human = notes[0]
    notes_robot = notes[1]
    total_modules = len(modules)

    # Performance state
    video = None
    photo = None
    audio_enabled = True
    human_voice_enabled = True
    robot_voice_enabled = True

    # Prepare stage
    trigger_photo_and_video_stop()
    unmute_narrator()
    play_audio(audio_file_path)

    # Play score!
    try:
        while current_module_index < total_modules:
            # Get composition data for next module
            module = modules[current_module_index]
            parameters = module["parameters"]
            (id, start_time, end_time) = module["module"]
            media = module["media"] if "media" in module else None
            media_from = (
                module["media_from"] if "media_from" in module else None)

            # Print some debugging info
            logger.debug("=============")
            logger.debug("Module #{} ({})", current_module_index, id)
            logger.debug("Parameters: {} {}s-{}s, Media: {}".format(
                         ", ".join(parameters), start_time, end_time, media))

            # Performance state machine
            if "VIDEO" in parameters and video is None:
                video = media
                trigger_video(media, media_from)
            elif "PHOTO" in parameters and photo is None:
                photo = media
                trigger_photo(media)

            if ("VIDEO" not in parameters
                    and "PHOTO" not in parameters
                    and (video is not None or photo is not None)):
                video = None
                photo = None
                trigger_photo_and_video_stop()

            if ("NARRATOR" in parameters and not audio_enabled):
                unmute_narrator()
            elif ("NARRATOR" not in parameters and audio_enabled):
                mute_narrator()

            # Performance state machine for demo mode
            if ("VOICE_1" in parameters and not human_voice_enabled):
                human_voice_enabled = True
            elif ("VOICE_1" not in parameters and human_voice_enabled):
                human_voice_enabled = False

            if ("VOICE_2" in parameters and not robot_voice_enabled):
                robot_voice_enabled = True
            elif ("VOICE_2" not in parameters and robot_voice_enabled):
                robot_voice_enabled = False

            # Trigger notes as well in demo mode
            if is_demo:
                if human_voice_enabled:
                    prepare_voice_performance("human", notes_human,
                                              start_time, end_time)
                if robot_voice_enabled:
                    prepare_voice_performance("robot", notes_robot,
                                              start_time, end_time)

            # Wait for next module
            await asyncio.sleep(MODULE_DURATION)
            current_module_index += 1
    except asyncio.CancelledError:
        logger.debug("Performance got cancelled")
    finally:
        logger.debug("Finish performance")
        trigger_photo_and_video_stop()


def perform_composition(title: str,
                        audio_file_path: str,
                        composition_data: schemas.CompositionData,
                        is_demo: bool):
    for task in tasks:
        if not task.done():
            raise Exception("Another composition is currently being performed")

    logger.debug(
        "Perform composition '{}' (is_demo={}, audio_file={})"
        .format(title, is_demo, audio_file_path))
    task = asyncio.create_task(
        perform(audio_file_path, composition_data, is_demo))

    # Add task to the set. This creates a strong reference.
    tasks.add(task)

    # To prevent keeping references to finished tasks forever, make each task
    # remove its own reference from the set after completion:
    task.add_done_callback(tasks.discard)


def stop_composition():
    for task in tasks:
        task.cancel()
