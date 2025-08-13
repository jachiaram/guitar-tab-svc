
import numpy as np
if not hasattr(np, 'int'):
    np.int = int
import os
import pretty_midi
import networkx as nx
import warnings
import matplotlib.pyplot as plt
from basic_pitch.inference import predict
from basic_pitch.note_creation import note_events_to_midi
from Audio_To_Midi import audio_to_midi


warnings.filterwarnings("ignore", message=".*tf.lite.Interpreter is deprecated.*")

class Guitar:
    def __init__(self, tuning=["E2", "A2", "D3", "G3", "B3", "E4"], frets=20):
        self.frets = frets
        self.tuning = [self.note_to_midi(note) for note in tuning]
        self.string_map = self.build_string_map()

    def note_to_midi(self, note):
        note_map = {'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5,
                    'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11}
        name = note[:-1]
        octave = int(note[-1])
        return 12 * (octave + 1) + note_map[name]

    def build_string_map(self):
        note_to_pos = {}
        for string_idx, open_note in enumerate(self.tuning):
            for fret in range(self.frets + 1):
                midi_note = open_note + fret
                if midi_note not in note_to_pos:
                    note_to_pos[midi_note] = []
                note_to_pos[midi_note].append((string_idx, fret))
        return note_to_pos

    def get_positions(self, midi_note):
        return self.string_map.get(midi_note, [])

def cost(from_pos, to_pos):
    string_diff = abs(from_pos[0] - to_pos[0])
    fret_diff = abs(from_pos[1] - to_pos[1])
    return string_diff + fret_diff

def build_fretboard_graph(guitar, midi_sequence):
    G = nx.DiGraph()
    layers = []

    for note_idx, (note, _) in enumerate(midi_sequence):
        positions = guitar.get_positions(note)
        layer_nodes = []
        for pos in positions:
            node = (note_idx, pos)
            G.add_node(node)
            layer_nodes.append(node)
        layers.append(layer_nodes)

    for i in range(len(layers) - 1):
        for src in layers[i]:
            for dst in layers[i + 1]:
                c = cost(src[1], dst[1])
                G.add_edge(src, dst, weight=c)

    return G, layers

def find_optimal_fingering(graph, layers):
    min_cost = float("inf")
    best_path = None

    for start in layers[0]:
        for end in layers[-1]:
            try:
                path = nx.dijkstra_path(graph, start, end)
                total_cost = sum(graph[u][v]['weight'] for u, v in zip(path, path[1:]))
                if total_cost < min_cost:
                    min_cost = total_cost
                    best_path = path
            except nx.NetworkXNoPath:
                continue

    return best_path

def print_tab_path(path, midi_sequence):
    print("Generated Guitar Tab:")
    for (note_idx, (string, fret)) in path:
        midi = midi_sequence[note_idx][0]
        print(f"Note {midi} -> String {6 - string}, Fret {fret}")

def draw_graph(G):
    pos = {node: (node[0], node[1][1]) for node in G.nodes}  # X: time, Y: fret
    labels = {node: f"S{node[1][0]+1}-F{node[1][1]}" for node in G.nodes}

    plt.figure(figsize=(12, 6))
    nx.draw(G, pos, with_labels=True, labels=labels, node_size=600, font_size=8)
    plt.title("Guitar Fretboard Graph")
    plt.xlabel("Note Index")
    plt.ylabel("Fret Number")
    plt.grid(True)
    plt.show()

def extract_notes_from_midi(midi_path):
    midi_data = pretty_midi.PrettyMIDI(midi_path)
    notes = []
    for instrument in midi_data.instruments:
        if instrument.is_drum:
            continue
        for note in instrument.notes:
            notes.append((note.pitch, note.start))
    notes.sort(key=lambda x: x[1])  # Sort by start time
    return notes

def generate_tab_from_midi(midi_path):
    guitar = Guitar()
    midi_sequence = extract_notes_from_midi(midi_path)
    graph, layers = build_fretboard_graph(guitar, midi_sequence)
    draw_graph(graph)
    best_path = find_optimal_fingering(graph, layers)
    if best_path:
        print_tab_path(best_path, midi_sequence)
    else:
        print("No valid fingering found.")


if __name__ == "__main__":
    audio_file = "test3.m4a"
    generate_tab_from_midi(audio_to_midi(audio_file))



# def midi_to_tabs(midi_data: pretty_midi.PrettyMIDI, tuning_name='standard'):
#     guitar_program = pretty_midi.instrument_name_to_program('electricguitarclean')
#     tuning = TUNINGS[tuning_name]
#     num_strings = len(tuning)
#     tab_lines = {s: [] for s in range(1, num_strings + 1)}
#
#     # Collect and sort notes
#     notes = []
#     # for instrument in midi_data.instruments:
#     for note in guitar_program.notes:
#         mapping = pitch_to_string_and_fret(note.pitch, tuning)
#         if mapping:
#             string, fret = mapping
#             notes.append((note.start, string, fret, note.pitch))
#     notes.sort(key=lambda x: x[0])
#
#     # Write tab
#     for note in notes:
#         _, string, fret, _ = note
#         for s in tab_lines:
#             if s == string:
#                 tab_lines[s].append(str(fret).rjust(2))
#             else:
#                 tab_lines[s].append('--')
#
#     for s in sorted(tab_lines.keys(), reverse=False):
#         print(f"String {s} | " + ' '.join(tab_lines[s]))


# # ---- Guitar Tablature Configuration ----
# MAX_FRET = 20
#
# # Example tunings (MIDI pitches, string 6 → 1)
# TUNINGS = {
#     "standard": [40, 45, 50, 55, 59, 64], # E A D G B E
#     "open_f":   [41, 45, 48, 55, 59, 64], # F A C G B E
#     "drop_d":   [38, 45, 50, 55, 59, 64], # D A D G B E
#     "open_g":   [38, 43, 50, 55, 59, 62], # D G D G B D
# }
#
# def pitch_to_string_and_fret(pitch, tuning):
#     """Map MIDI pitch to best string/fret based on tuning"""
#     candidates = []
#     for i, open_pitch in enumerate(tuning):  # i = 0 (string 6)
#         string = 6 - i
#         fret = pitch - open_pitch
#         if 0 <= fret <= MAX_FRET:
#             candidates.append((string, fret))
#             return min(candidates, key=lambda x: x[1]) if candidates else None
