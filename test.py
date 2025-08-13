import tensorflow as tf
from basic_pitch.inference import predict, Model
from basic_pitch import ICASSP_2022_MODEL_PATH

model_output, midi_data, note_events = predict('inputs/c_scale.wav')
print(note_events)
