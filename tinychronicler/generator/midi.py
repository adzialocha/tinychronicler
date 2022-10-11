import os

import numpy as np
import pretty_midi

from tinychronicler.constants import MIDI_MODULES_DIR


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

    # Get MIDI events in seconds and remove duplicates (eg. chords)
    return get_all_notes(score)


def load_midi_modules(midi_files):
    """
    Load all MIDI files from a list
    """
    modules = []
    for file in midi_files:
        notes = analyze_midi("{}/{}".format(MIDI_MODULES_DIR, file["file"]))
        modules.append({
            "notes": notes,
            "file": file["file"],
            "duration": file["duration"],
        })
    return modules
