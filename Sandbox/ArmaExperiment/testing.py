from Wav2Float import wav2float
from PCMProcessing import *
import matplotlib.pyplot as plt
import statsmodels.tsa.arima.model
import numpy as np

audio = (wav2float(r"D:\Dropbox\수업자료\개별연구\repo\Sandbox\ArmaExperiment\8.wav"))[82000:int(2.5*30875+82000)]
audio_800 = DecreaseFrequency(list(audio),44100,800)
audio_5000 = DecreaseFrequency(list(audio),44100,5000)
audio_10k = DecreaseFrequency(list(audio),44100,10000)
audio_25k = DecreaseFrequency(list(audio)[:30875],44100,25000)
audio_31k = DecreaseFrequency(list(audio),44100,31250)
# plt.subplot(131)
# plt.plot(audio)
# plt.subplot(132)
# plt.plot(audio_800)
# plt.subplot(133)
# plt.plot(audio_5000)
# plt.show()

#mod = statsmodels.tsa.arima.model.ARIMA(audio,order=(10,0,7))
#res = mod.fit()
#res.summary()

### 25k
# audio_25k_1byte = np.array(audio_25k)
# audio_25k_1byte = audio_25k_1byte - min(audio_25k_1byte)
# audio_25k_1byte = audio_25k_1byte / max(audio_25k_1byte)
# audio_25k_1byte *= 256
# clip = audio_25k_1byte > 255
# audio_25k_1byte[clip_25k] = 255
# copy_this = [int(i) for i in audio_25k_1byte]
# print(copy_this)
# print(len(copy_this))
# plt.plot(copy_this)
# plt.show()

### 5k
# audio_5k_1byte = np.array(audio_5000)
# audio_5k_1byte = audio_5k_1byte - min(audio_5k_1byte)
# audio_5k_1byte = audio_5k_1byte / max(audio_5k_1byte)
# audio_5k_1byte *= 256
# clip_5k = audio_5k_1byte > 255
# audio_5k_1byte[clip_5k] = 255
# copy_this_5k = [int(i) for i in audio_5k_1byte]
# print(copy_this_5k)
# print(len(copy_this_5k))
# plt.plot(copy_this_5k)
# plt.show()

audio_10k_1byte = np.array(audio_10k)
audio_10k_1byte = audio_10k_1byte - min(audio_10k_1byte)
audio_10k_1byte = audio_10k_1byte / max(audio_10k_1byte)
audio_10k_1byte *= 256
clip_10k = audio_10k_1byte > 255
audio_10k_1byte[clip_10k] = 255
copy_this_10k = [int(i) for i in audio_10k_1byte]
print(copy_this_10k)
print(len(copy_this_10k))
plt.plot(copy_this_10k)
plt.show()