from Wav2Float import wav2float
from PCMProcessing import *
import matplotlib.pyplot as plt
import statsmodels.tsa.arima.model

audio = [0]+wav2float(r"D:\Dropbox\수업자료\개별연구\NoiseAudio\8.wav")[110000:150000]
audio_800 = DecreaseFrequency(list(audio),44100,800)
audio_5000 = DecreaseFrequency(list(audio),44100,5000)
# plt.subplot(131)
# plt.plot(audio)
# plt.subplot(132)
# plt.plot(audio_800)
# plt.subplot(133)
# plt.plot(audio_5000)
# plt.show()

mod = statsmodels.tsa.arima.model.ARIMA(audio_5000,order=(10,0,7))
res = mod.fit()
res.summary()


