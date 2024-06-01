import amfm_decompy.pYAAPT as pYAAPT
import amfm_decompy.basic_tools as basic
from scipy.io import wavfile
import scipy.fft 
import numpy as np
import matplotlib.pyplot as plt

sample_rate, data = wavfile.read('./examples/twinkle/twinkle.wav')
data = data[:, 0]  # Use only one channel
time = np.arange(0, float(data.shape[0]), 1) / sample_rate
fig, ax = plt.subplots(2, 1, figsize=(10, 10))
ax[0].plot(time, data)
ax[0].set_xlabel('Time [s]')
ax[0].set_ylabel('Amplitude')
ax[0].set_title('Audio in time domain')
spectrum = np.abs(scipy.fft.fft(data))
freqs = np.fft.fftfreq(len(spectrum), 1/sample_rate)
spectrum = spectrum[:len(spectrum)//2]
freqs = freqs[:len(freqs)//2]

signal = basic.SignalObj('./examples/twinkle/twinkle.wav')
pitch = pYAAPT.yaapt(signal, f0_min=40, f0_max=2000)
x = np.linspace(0, len(data), len(pitch.values))/sample_rate
ax[1].plot(x, pitch.values, label='values')
# x = np.linspace(0, len(data), len(pitch.samp_values))/sample_rate
# ax[1].plot(x, pitch.samp_values, label='samp_values')
# ax[1].legend()
ax[1].set_xlabel('Time [s]')
ax[1].set_ylabel('Frequency [Hz]')
ax[1].set_title('Pitch tracking')
# print("values length: ", len(pitch.values))
print("samp_values length: ", len(pitch.samp_values))
plt.show()
