import math
import os

import numpy as np
import pretty_midi

SECONDS_PER_MINUTE = 60
MS_PER_120_QUARTER = 500


def get_midi_files(base_dir):
    """
    Returns a list of all MIDI files in a given folder
    """
    midi_files = []
    for root, directories, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".mid"):
                midi_files.append(os.path.join(base_dir, file))
    midi_files.sort()
    return midi_files


def get_end_time(score, time_signature, bpm=120):
    # Get the score end time in seconds
    end_time = math.ceil(score.get_end_time() * 10) / 10

    # Calculate how long a measure is in seconds
    beat_time = (
        SECONDS_PER_MINUTE
        / bpm
        / (time_signature.denominator / time_signature.numerator)
    )
    measure_time = beat_time * time_signature.numerator

    # Normalize the end time to a well formed measure
    end_time = end_time + (end_time % measure_time)
    return end_time


def get_all_notes(score):
    """
    Returns a sorted and deduplicated list of all note start
    and end times over all instruments
    """
    notes = []
    for instrument in score.instruments:
        for note in instrument.notes:
            notes.append([note.start, note.end])
    return np.sort(np.unique(notes, axis=0), axis=0)


def analyze_midi(file, bpm=120):
    """
    Analyze a MIDI file, return all notes and duration
    """
    # Load MIDI file and clean up
    score = pretty_midi.PrettyMIDI(file, initial_tempo=bpm)
    score.remove_invalid_notes()

    # Get time signature
    if len(score.time_signature_changes) == 0:
        raise Exception("No time signature given for {}".format(file))
    time_signature = score.time_signature_changes[0]

    # Get last event in MIDI file
    last_event_time = score.get_end_time() * 1000

    # Get duration of one bar
    fraction = MS_PER_120_QUARTER / time_signature.denominator
    bar_duration = (fraction * time_signature.numerator) * 4

    # Get duration of whole midi file
    duration = math.ceil(last_event_time / bar_duration) * bar_duration

    # Get MIDI events in seconds and remove duplicates (eg. chords)
    notes = get_all_notes(score)
    return notes, duration / 1000
