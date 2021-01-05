# With help from 
# https://stackoverflow.com/questions/7769981/how-to-convert-wav-file-to-float-amplitude/29989593#29989593
import wave
import struct
import sys


def wav2float(wave_file):
    w = wave.open(wave_file)
    byte_audio = w.readframes(w.getnframes())
    # convert binary chunks to short 
    audio = struct.unpack("%ih" % (w.getnframes()* w.getnchannels()), byte_audio)
    audio_float = [float(val) / pow(2, 15) for val in audio]
    return audio_float