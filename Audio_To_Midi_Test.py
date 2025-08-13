import unittest
from Audio_To_Midi import audio_to_midi
from Audio_To_Midi import extract_notes_from_midi


class AudioToMidiTestCase(unittest.TestCase):
    def test_c_scale(self):
        test_path = audio_to_midi('inputs/c_scale.wav')
        notes = extract_notes_from_midi(test_path)
        major_scale_pattern = [2, 2, 1, 2, 2, 2, 1]
        start_note = 48

        for i, j in zip(range(0,12), major_scale_pattern):
            self.assertEqual(notes[i][0], start_note)
            start_note += j

    def test_covet_riff(self):
        test_path = audio_to_midi('inputs/covet_riff.mp3')
        notes = extract_notes_from_midi(test_path)
        # major_scale_pattern = [2, 2, 1, 2, 2, 2, 1]
        # start_note = 48
        #
        # for i, j in zip(range(0,12), major_scale_pattern):
        #     self.assertEqual(notes[i][0], start_note)
        #     start_note += j

if __name__ == '__main__':
    unittest.main()
