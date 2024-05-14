from scipy.io import wavfile
import scipy.fft as fft
import scipy.signal as signal
import numpy as np
import matplotlib.pyplot as plt

# TODO: need to find start of a new note by finding sharp increases in amplitude

if __name__ == '__main__':
    sample_rate, data = wavfile.read('./software/test.wav') # data has two channels, left and right
    data = data[:, 0]  # Use only one channel
    start_sec = 0.0
    end_sec = 1
    time = np.arange(0, float(data.shape[0]), 1) / sample_rate
    # Use only the first few seconds for testing purposes
    time = time[(int(start_sec*sample_rate)):(int(end_sec*sample_rate))] 
    data = data[(int(start_sec*sample_rate)):(int(end_sec*sample_rate))] 

    print('Sample rate:', sample_rate)
    print('Total samples:', len(data))
    print('Duration:', len(data) / sample_rate, 'seconds')

    # Plot the audio signal
    fig, ax = plt.subplots(2, 1)
    ax[0].plot(time, data, linewidth=0.6, alpha = 0.9, color='black')
    ax[0].set_xlabel('Time (s)')
    ax[0].set_ylabel('Amplitude')
    ax[0].set_title('Audio Signal (time domain)')

    # Compute the Fourier Transform
    n = len(data)
    fourier = fft.fft(data) / n
    freq = fft.fftfreq(n, 1/sample_rate)
    spectrum_freq = freq[:n//2]
    spectrum_mag = np.abs(fourier)[:n//2]
    ax[1].plot(spectrum_freq, spectrum_mag, linewidth=0.6, alpha = 0.9, color='black')
    ax[1].set_xlabel('Frequency (Hz)')
    ax[1].set_ylabel('Amplitude')
    ax[1].set_title('Audio Signal (frequency domain)')

    # TODO: Find the fundamental frequency of the note
    peaks, _ = signal.find_peaks(spectrum_mag, height=max(spectrum_mag)*0.5, distance=50)
    ax[1].plot(spectrum_freq[peaks], spectrum_mag[peaks], 'x', color='red')
    plt.show()