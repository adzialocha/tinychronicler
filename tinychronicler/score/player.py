import asyncio
import random

from loguru import logger

from tinychronicler.constants import MODULE_DURATION
from tinychronicler.database import schemas
from tinychronicler.io import (
    mute_audio,
    play_audio,
    play_beat,
    play_count_in,
    play_note,
    play_video,
    show_image,
    stop_audio,
    stop_video_or_image,
    unmute_audio,
)
from tinychronicler.io.led import (
    print_background,
    print_left_eye,
    print_mouth,
    print_right_eye,
    reset_all,
    reset_eyes,
    reset_mouth,
)

tasks = set()

SILENCE_MODULE = 0
HUMAN_PARAMETERS = ["HUMAN_1", "HUMAN_2", "HUMAN_3", "HUMAN_4"]
ROBOT_PARAMETERS = ["ROBOT_1", "ROBOT_2", "ROBOT_BASS"]


def contains(a, b):
    for item in a:
        if item in b:
            return True
    return False


def trigger_audio(media: str):
    logger.debug("Trigger audio: {} {}", media)
    play_audio(media)


def trigger_audio_stop():
    logger.debug("Trigger audio stop")
    stop_audio()


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
    reset_mouth()


def unmute_narrator():
    logger.debug("Unmute narrator")
    unmute_audio()
    print_mouth()


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


async def perform_metronome(metronome=False, count_in=False):
    # Audible metronome
    if count_in:
        play_count_in()
    elif metronome:
        play_beat()

    # Visual fun
    if random.random() > 0.8:
        reset_eyes()
    if random.random() > 0.8:
        print_right_eye()
        await asyncio.sleep(random.random())
    if random.random() > 0.8:
        print_left_eye()
        await asyncio.sleep(random.random())


def prepare_metronome(metronome: bool, count_in: bool):
    task = asyncio.create_task(perform_metronome(metronome,
                                                 count_in))
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
    count_in = True

    # Prepare stage
    trigger_photo_and_video_stop()
    unmute_narrator()
    print_background()

    # Count in!
    prepare_metronome(False, True)
    await asyncio.sleep(MODULE_DURATION)
    play_audio(audio_file_path)
    print_mouth()

    # Play score!
    try:
        while current_module_index < total_modules:
            # Get composition data for next module
            module = modules[current_module_index]
            parameters = module["parameters"]
            (id_1, id_2, start_time, end_time) = module["module"]
            media = module["media"] if "media" in module else None
            media_from = (
                module["media_from"] if "media_from" in module else None)

            # Print some debugging info
            logger.debug("=============")
            logger.debug("Module #{} ({}, {})",
                         current_module_index, id_1, id_2)
            logger.debug("Parameters: {} {}s-{}s, Media: {}".format(
                         ", ".join(parameters), start_time, end_time, media))

            # Performance state machine
            if "VIDEO" in parameters and video is None:
                video = media
                trigger_video(media, media_from)
            elif "PHOTO" in parameters and photo is None:
                photo = media
                trigger_photo(media)
            elif ("VIDEO" not in parameters
                    and "PHOTO" not in parameters
                    and (video is not None or photo is not None)):
                video = None
                photo = None
                trigger_photo_and_video_stop()

            if ("NARRATOR" in parameters and not audio_enabled):
                audio_enabled = True
                unmute_narrator()
            elif ("NARRATOR" not in parameters and audio_enabled):
                audio_enabled = False
                mute_narrator()

            # Performance state machine for voices (and demo mode)
            if (contains(HUMAN_PARAMETERS, parameters)
                    and not human_voice_enabled):
                human_voice_enabled = True
            elif (not contains(HUMAN_PARAMETERS, parameters)
                    and human_voice_enabled):
                human_voice_enabled = False

            if (contains(ROBOT_PARAMETERS, parameters)
                    and not robot_voice_enabled):
                robot_voice_enabled = True
            elif (not contains(ROBOT_PARAMETERS, parameters)
                    and robot_voice_enabled):
                robot_voice_enabled = False

            # Trigger notes as well in demo mode
            if is_demo:
                if human_voice_enabled and id_1 != SILENCE_MODULE:
                    prepare_voice_performance("human", notes_human,
                                              start_time, end_time)
                if robot_voice_enabled and id_2 != SILENCE_MODULE:
                    prepare_voice_performance("robot", notes_robot,
                                              start_time, end_time)

            # Metronome
            count_in = False
            if current_module_index + 1 < total_modules:
                next_module = modules[current_module_index + 1]
                next_parameters = next_module["parameters"]
                if ((contains(HUMAN_PARAMETERS, next_parameters)
                        and not human_voice_enabled) or
                        (contains(ROBOT_PARAMETERS, next_parameters)
                            and not robot_voice_enabled)):
                    count_in = True
            prepare_metronome(
                human_voice_enabled or robot_voice_enabled, count_in)

            # Wait for next module
            await asyncio.sleep(MODULE_DURATION)
            current_module_index += 1
    except asyncio.CancelledError:
        logger.debug("Performance got cancelled")
    finally:
        logger.debug("Finish performance")
        trigger_photo_and_video_stop()
        reset_all()


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
    reset_all()
    trigger_audio_stop()

    for task in tasks:
        task.cancel()
