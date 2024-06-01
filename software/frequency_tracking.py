import amfm_decompy.pYAAPT as pYAAPT
import amfm_decompy.basic_tools as basic
from scipy.io import wavfile
import scipy.fft 
import numpy as np
import matplotlib.pyplot as plt

sample_rate, data = wavfile.read('./examples/twinkle/twinkle.wav')
data = data[:, 0]  # Use only one channel
time = np.arange(0, float(data.shape[0]), 1) / sample_rate
fig, ax = plt.subplots(3, 1)
ax[0].plot(time, data)
spectrum = np.abs(scipy.fft.fft(data))
freqs = np.fft.fftfreq(len(spectrum), 1/sample_rate)
spectrum = spectrum[:len(spectrum)//2]
freqs = freqs[:len(freqs)//2]
ax[1].plot(freqs, spectrum)
ax[1].axvline(x=261.63, color='r')

signal = basic.SignalObj('./examples/twinkle/twinkle.wav')
pitch = pYAAPT.yaapt(signal, f0_min=40, f0_max=2000)
x = np.arange(0, len(pitch.values), 1)
ax[2].plot(x, pitch.values)
plt.show()
