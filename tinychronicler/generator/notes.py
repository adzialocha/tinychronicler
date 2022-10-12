import contextlib
import json
import random
import subprocess
import wave
from typing import List

import numpy as np
from loguru import logger
from vosk import KaldiRecognizer, Model, SetLogLevel

from tinychronicler.constants import (
    GRID_SIZE,
    MIDI_MODULES_1,
    MIDI_MODULES_2,
    MODEL_PATHS,
)

from .midi import load_midi_modules

SetLogLevel(-1)  # Disable vosk logging

# Look only for onsets which are close (+/- seconds)
SIMILARITY_THRESHOLD = 0.2

# Load files with this sample rate
SAMPLE_RATE = 16000

# Buffer size to load audio file in batches
BUFFER_SIZE = 4000

# Allow silence of this length (in seconds)
SILENCE_DURATION = 0.250  # 8th note


def times_from_range(times, start, end):
    return [t for t in times if t >= start and t <= end]


def calculate_similarity(source, target, t=SIMILARITY_THRESHOLD):
    if len(target) == 0 and len(source) == 0:
        return 1
    deltas = np.array([])
    for src_event in source:
        values = [abs(src_event - trg_event) for trg_event in target]
        deltas = np.append(deltas,
                           [(t - v) / t for v in values if v < t])
    result = np.median(deltas) if len(deltas) > 0 else 0.0
    return result


def audio_file_duration(audio_file: str):
    with contextlib.closing(wave.open(audio_file, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        return duration  # seconds


def detect_word_times(audio_file: str, language_code: str = "en"):
    if language_code not in MODEL_PATHS:
        raise Exception(
            "No model for language code {} given".format(language_code))

    # Load ML model for speech recognition
    model = Model(MODEL_PATHS[language_code])
    logger.info("Loaded speech recognition model for language '{}'"
                .format(language_code))

    # Prepare speech recognition
    rec = KaldiRecognizer(model, SAMPLE_RATE)
    rec.SetWords(True)
    results = []

    # Helper method to handle vosk responses
    def append_results(vosk_str):
        # The response comes as a JSON string, we have to decode it
        response_dict = json.loads(vosk_str)
        # Ignore empty responses (aka failed recognitions)
        if 'result' not in response_dict:
            return
        for item in response_dict['result']:
            logger.debug("{0:5.2f}s - {1:5.2f}s: {2:14} ({3:.2%})"
                         .format(item['start'],
                                 item['end'],
                                 item['word'][:14],
                                 item['conf']))
            results.append(item["start"])

    # Convert audio (16khz, mono, 16bit PCM) and feed it in batches into speech
    # recognition model
    with subprocess.Popen(["ffmpeg",
                           "-loglevel", "quiet",
                           "-i", audio_file,
                           "-ar", str(SAMPLE_RATE),
                           "-ac", "1",
                           "-f", "s16le",
                           "-"],
                          stdout=subprocess.PIPE) as process:
        while True:
            data = process.stdout.read(BUFFER_SIZE)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                append_results(rec.Result())
            else:
                append_results(rec.PartialResult())
        append_results(rec.FinalResult())

    return results


def quantize_word_times(word_times: List[int]):
    results = []
    for word in word_times:
        correlation = word % GRID_SIZE
        if correlation < GRID_SIZE:
            value = word - correlation
            # Check for duplicates
            if value not in results:
                results.append(word - correlation)
    return results


def map_modules_to_word_times(total_duration: int,
                              modules,
                              word_times: List[int]):
    offset = 0
    result_notes = np.empty((0, 3))
    result_modules = []

    while offset < total_duration:
        start_time = offset
        results = []

        # Analyze silence and add as one golden option
        end_time = start_time + SILENCE_DURATION
        times_range = times_from_range(word_times, start_time, end_time)
        similarity = calculate_similarity(times_range, [])
        results.append({
            'similarity': similarity,
            'is_silence': True,
            'index': 0,
            'start_time': start_time,
            'end_time': end_time,
            'notes_with_offset': [],
        })

        for index, module in enumerate(modules):
            # Get notes of MIDI module file and apply offset
            file = module["file"]
            notes = module["notes"]
            duration = module["duration"]

            # Take only the starting time of each note (pitch, start, end)
            notes_with_offset = np.array([t + start_time for t in notes])[:, 1]

            # Get all offset events between this slice (start - end time)
            end_time = start_time + duration
            times_range = times_from_range(word_times, start_time, end_time)

            # Analyze similarity of original slice with module notes
            similarity = calculate_similarity(times_range, notes_with_offset)

            final_notes = []
            for note in notes:
                final_notes.append(
                    (int(note[0]), note[1] + start_time, note[2] + start_time))

            # Store results
            results.append({
                'similarity': similarity,
                'is_silence': False,
                'file': file,
                'index': index + 1,
                'start_time': start_time,
                'end_time': end_time,
                'notes_with_offset': final_notes,
            })

        # @TODO: What is this doing here?
        # if len(results) == 0:
        #     break

        # Shuffle it before to allow different results when similarity score is
        # the same
        shuffled = results[:]
        random.shuffle(shuffled)

        # Find most similar module for this section
        results_winner = max(shuffled, key=lambda x: x['similarity'])

        # Add winner module to final results
        if len(results_winner['notes_with_offset']) > 0:
            result_notes = np.append(
                result_notes, results_winner['notes_with_offset'], axis=0)
        result_modules.append((
            results_winner['index'],
            results_winner['start_time'],
            results_winner['end_time']))

        # Prepare offset for next iteration
        offset = results_winner['end_time']

        # Debug logging
        logger.debug('-----------------')
        logger.debug("{}s - {}s".format(results_winner['start_time'],
                                        results_winner['end_time']))
        logger.debug('-----------------')
        for r in results:
            win = "✔" if results_winner['index'] == r['index'] else ""
            score = r['similarity'] if r['similarity'] != 0.0 else 0
            logger.debug("{0:>2}: {1:10.2%} {2}"
                         .format(r['index'], score, win))

    return result_notes, result_modules


def generate_notes(audio_file: str, language: str):
    # Determine total duration of file
    duration = audio_file_duration(audio_file)
    logger.info("Read audio file: {}, {}hz, {:0.2f}s"
                .format(audio_file, SAMPLE_RATE, duration))

    # Detect all spoken words inside the audio and return times
    word_times = detect_word_times(audio_file, language)
    logger.info("Detected {} words".format(len(word_times)))

    # Quantize all times so they fit a grid
    quantized_word_times = quantize_word_times(word_times)

    # Generate two separate voices
    result_notes = []
    result_module_indices = []
    for midi_modules in [MIDI_MODULES_1, MIDI_MODULES_2]:
        # Load MIDI files for this voice
        modules = load_midi_modules(midi_modules)

        # Try to map modules as close as possible to word times
        notes, module_indices = map_modules_to_word_times(
            duration, modules, quantized_word_times)

        result_notes.append(notes.tolist())
        result_module_indices.append(module_indices)

    logger.info("Finished generating notes")
    return (result_notes, result_module_indices)
