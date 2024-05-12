from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt

sample_rate, data = wavfile.read('test.wav')

print('Sample rate:', sample_rate)
print('Total samples:', len(data))
print('Duration:', len(data) / sample_rate, 'seconds')

time = np.arange(0, float(data.shape[0]), 1) / sample_rate
plt.plot(time, data, linewidth=0.01, alpha=0.7, color='black')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.show()