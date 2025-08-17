import unittest
import sys
sys.path.append('../')
from Audio_To_Midi import audio_to_midi
from Audio_To_Midi import extract_notes_from_midi

class AudioToMidiTestCase(unittest.TestCase):
    def scale_compare(self, start_note: int, path_to_audio: str):
        test_path = audio_to_midi(path_to_audio)
        notes = extract_notes_from_midi(test_path)
        major_scale_pattern = [2, 2, 1, 2, 2, 2, 1]

        for i, j in zip(range(0,12), major_scale_pattern):
            self.assertEqual(notes[i][0], start_note)
            start_note += j
    
    def test_c_2_scale(self):
        self.scale_compare(48, 'inputs/c_scale.wav')
        # test_path = audio_to_midi('inputs/c_scale.wav')
        # notes = extract_notes_from_midi(test_path)
        # major_scale_pattern = [2, 2, 1, 2, 2, 2, 1]
        # start_note = 48

        # for i, j in zip(range(0,12), major_scale_pattern):
        #     self.assertEqual(notes[i][0], start_note)
        #     start_note += j


if __name__ == '__main__':
    unittest.main()
