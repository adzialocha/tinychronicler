import os
from typing import List

import librosa
import numpy as np
from loguru import logger

from tinychronicler.constants import (
    ALLOWED_MIME_TYPES_AUDIO,
    ALLOWED_MIME_TYPES_IMAGE,
    ALLOWED_MIME_TYPES_VIDEO,
    MIDI_MODULES_DIR,
)
from tinychronicler.database import schemas

from .audio import detect_onsets, remove_close_onsets
from .midi import analyze_midi, get_midi_files

# Look only for onsets which are close (+/- seconds)
SIMILARITY_THRESHOLD = 0.4


def times_from_range(times, start, end):
    return [t for t in times if t >= start and t <= end]


def calculate_similarity(source, target):
    deltas = np.array([])
    for src_event in source:
        values = [abs(src_event - trg_event) for trg_event in target]
        deltas = np.append(
            deltas,
            [
                (SIMILARITY_THRESHOLD - v) / SIMILARITY_THRESHOLD
                for v in values
                if v < SIMILARITY_THRESHOLD
            ],
        )
    result = np.median(deltas) if len(deltas) > 0 else 0.0
    return result


async def generate_composition(files: List[schemas.File]):
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
    y, sr = librosa.load(audio_file)
    logger.debug("Read audio file: {} @ {}hz".format(audio_file, sr))

    # Detect onsets
    onset_frames, onset_env, onset_times = detect_onsets(y, sr)
    onset_frames = remove_close_onsets(onset_frames, onset_times)
    onset_frames_times = onset_times[onset_frames]

    # Find fitting module MIDI events to offset events of original sound
    offset = 0
    audio_duration = len(y) / sr
    result_notes = np.empty((0, 2))
    result_modules = []
    result_statistics = []
    while offset < audio_duration:
        # Analyze similarity of all modules to offsets
        start_time = offset
        results = []

        for index, file in enumerate(midi_files):
            # Get notes of MIDI module file and apply offset
            notes, duration = analyze_midi(file)
            notes_with_offset = np.array([t + start_time for t in notes])[:, 0]

            # Get all offset events between this slice (start - end time)
            end_time = start_time + duration
            times_range = times_from_range(
                onset_frames_times, start_time, end_time
            )
            if len(times_range) == 0:
                continue

            # Analyze similarity of original slice with module notes
            similarity = calculate_similarity(times_range, notes_with_offset)

            # Store results
            results.append(
                {
                    "similarity": similarity,
                    "file": file,
                    "index": index,
                    "start_time": start_time,
                    "end_time": end_time,
                    "notes_with_offset": np.array(
                        [t + start_time for t in notes]
                    ),
                }
            )

        if len(results) == 0:
            break

        # Find most similar module for this section
        results_winner = max(results, key=lambda x: x["similarity"])

        # Add winner module to final results
        result_notes = np.append(
            result_notes, results_winner["notes_with_offset"], axis=0
        )
        result_modules.append(results_winner["index"])

        # Prepare offset for next iteration
        offset = results_winner["end_time"]

        # Gather some statistics
        result_statistics.append(results_winner)

        logger.info("-----------------")
        logger.info(
            "{}s - {}s".format(
                results_winner["start_time"], results_winner["end_time"]
            )
        )
        logger.info("-----------------")
        for r in results:
            win = "🗸" if results_winner["index"] == r["index"] else ""
            score = r["similarity"] if r["similarity"] != 0.0 else "%"
            logger.info(
                "{0:>2}: {1:.2%} {2}".format(r["index"] + 1, score, win)
            )

    return {
        "notes": result_notes.tolist(),
        "modules": result_modules,
    }
