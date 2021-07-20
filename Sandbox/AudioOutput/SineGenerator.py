import numpy as np
import matplotlib.pyplot as plt

def generate_sine(frequency):
	intervals = int(25000/frequency)
	sinetable = np.sin(np.arange(intervals)/intervals*2*np.pi)*128+128
	sinetable_zn = sinetable-128
	clipping = sinetable>255
	sinetable[clipping] = 255
	clipping = sinetable_zn>127
	sinetable_zn[clipping] = 127
	sinetable = [int(i) for i in sinetable]
	sinetable_zn = [int(i) for i in sinetable_zn]
	return (intervals-1,sinetable,sinetable_zn)
