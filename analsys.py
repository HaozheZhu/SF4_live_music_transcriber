from scipy.io import wavfile
import scipy.fft as fft
import numpy as np
import matplotlib.pyplot as plt

def clean_audio(audio, threshold):
    # Remove all samples below the threshold
    return np.array([0 if abs(sample) < threshold else sample for sample in audio])

if __name__ == '__main__':
    sample_rate, data = wavfile.read('test.wav') # data has two channels, left and right
    data = data[:, 0]  # Use only one channel
    data = data[:(int(1*sample_rate))] # Use only the first few seconds for testing purposes
    data = clean_audio(data, 2000) # Remove all samples below 500

    print('Sample rate:', sample_rate)
    print('Total samples:', len(data))
    print('Duration:', len(data) / sample_rate, 'seconds')

    # Plot the audio signal
    fig, ax = plt.subplots(1, 2)
    time = np.arange(0, float(data.shape[0]), 1) / sample_rate
    ax[0].plot(time, data, linewidth=0.6, alpha = 0.9, color='black')
    ax[0].set_xlabel('Time (s)')
    ax[0].set_ylabel('Amplitude')
    ax[0].set_title('Audio Signal (time domain)')

    # Compute the Fourier Transform
    fourier = fft.fft(data)
    n = len(data)
    freq = fft.fftfreq(n, 1/sample_rate)
    ax[1].plot(freq[:n//2], np.abs(fourier)[:n//2], linewidth=0.6, alpha = 0.9, color='black')
    ax[1].set_xlabel('Frequency (Hz)')
    ax[1].set_ylabel('Amplitude')
    ax[1].set_title('Audio Signal (frequency domain)')

    plt.show()