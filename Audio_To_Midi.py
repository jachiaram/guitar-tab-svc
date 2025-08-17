import os
import numpy as np
import pretty_midi
import logging
import warnings
import sys
from contextlib import redirect_stdout, redirect_stderr
from io import StringIO

logging.getLogger().setLevel(logging.ERROR)
warnings.filterwarnings('ignore')

from basic_pitch.inference import predict
from basic_pitch.note_creation import note_events_to_midi

warnings.filterwarnings("ignore")
if not hasattr(np, 'int'):
    np.int = int

def audio_to_midi(audio_path: str):
    with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
        _, midi_data, note_events = predict(audio_path, onset_threshold=0.45, frame_threshold=0.40, minimum_note_length=110)

        filtered_notes = [note for note in note_events if note[3] >= 0.45]

        midi_obj = note_events_to_midi(filtered_notes)
        midi_path = "outputs/" + os.path.basename(audio_path) + "_transcribed.mid"
        midi_obj.write(midi_path)
        return midi_path

def extract_notes_from_midi(midi_path):
    midi_data = pretty_midi.PrettyMIDI(midi_path)
    notes = []
    for instrument in midi_data.instruments:
        if instrument.is_drum:
            continue
        for note in instrument.notes:
            notes.append((note.pitch, note.start))
    notes.sort(key=lambda x: x[1])
    return notes