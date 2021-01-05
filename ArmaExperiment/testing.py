from Wav2Float import wav2float
from PCMProcessing import *
import matplotlib.pyplot as plt

audio = wav2float(r"D:\Dropbox\수업자료\개별연구\NoiseAudio\8.wav")
plt.subplot(121)
plt.plot(audio)
#plt.show()
plt.subplot(122)
plt.plot(DecreaseFrequency(list(audio),44100,800,False))
plt.show()