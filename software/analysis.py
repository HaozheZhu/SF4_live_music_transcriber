from scipy.io import wavfile
import scipy.fft as fft
import scipy.signal as signal
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def load_test_data_wav(path, start_sec, end_sec):
    sample_rate, data = wavfile.read(path) # data has two channels, left and right
    data = data[:, 0]  # Use only one channel
    time = np.arange(0, float(data.shape[0]), 1) / sample_rate
    # Use only the first few seconds for testing purposes
    time = time[(int(start_sec*sample_rate)):(int(end_sec*sample_rate))] 
    data = data[(int(start_sec*sample_rate)):(int(end_sec*sample_rate))] 

    print('Load test data successful! ')
    print('Sample rate:', sample_rate)
    print('Total samples:', len(data))
    print('Duration:', len(data) / sample_rate, 'seconds')
    print('-----------------------------------')
    return time, data, sample_rate

def load_test_data_csv(path, start_sec, end_sec):
    df = pd.read_csv(path)
    sample_rate = int(len(df) / df.iloc[-1]['Time'])

    # Use only the first few seconds for testing purposes
    time = df['Time'][int(start_sec*sample_rate):int(end_sec*sample_rate)]
    data = df['Data'][int(start_sec*sample_rate):int(end_sec*sample_rate)]

    print('Load test data successful! ')
    print('Average sample rate:', sample_rate)
    print('Total samples:', len(data))
    print('Duration:', len(data) / sample_rate, 'seconds')
    print('-----------------------------------')
    return time, data, sample_rate

def freq_to_note(freq):
    note_freq_table = pd.read_csv('./software/_lib/note_frequency_conversion.csv')
    note_freq_table = note_freq_table.astype({'Frequency': float, 'Note': str})
    note_freq_table['offset'] = note_freq_table['Frequency'] - freq
    note_freq_table['offset'] = abs(note_freq_table['offset'])
    note_freq_table = note_freq_table.sort_values(by='offset')
    return note_freq_table.iloc[0]['Note']

def freq_analysis(data, sample_rate): 
    n = len(data)
    fourier = fft.fft(data) / n
    freq = fft.fftfreq(n, 1/sample_rate)
    spectrum_freq = freq[:n//2]
    spectrum_mag = np.abs(fourier)[:n//2]
    return spectrum_freq, spectrum_mag

def extract_intervals(data, sample_rate): 
    # output: list of intervals, each interval is a list of two elements: the data and the duration in seconds
    # interval edegs are detected by large positive gradient of the smoothed envelope
    envelope = abs(signal.hilbert(data))
    smoothed_envelope = signal.savgol_filter(envelope, 800, 3)
    gradient = np.gradient(smoothed_envelope)
    gradient_peak, _ = signal.find_peaks(gradient, height=max(gradient)*0.3, distance=int(sample_rate*0.05))
    intervals = []
    for i in range(len(gradient_peak)-1):
        start = gradient_peak[i]
        end = gradient_peak[i+1]
        intervals.append(data[start:end])
    return intervals

def extract_note_and_duration(interval, sample_rate):
    spectrum_freq, spectrum_mag = freq_analysis(interval, sample_rate)
    peaks, _ = signal.find_peaks(spectrum_mag, height=max(spectrum_mag)*0.3, distance=50)
    notes = []
    for peak in peaks:
        freq = spectrum_freq[peak]
        note = freq_to_note(freq)
        notes.append(note)
    # print(f'peaks: {spectrum_freq[peaks]}')
    # note = freq_to_note(spectrum_freq[peaks])
    duration = len(interval) / sample_rate
    if notes:
        most_frequent_note = max(set(notes), key=notes.count)
        return most_frequent_note, duration
    return None, duration

def butter_lowpass_filter(data, cutoff, fs, order):
    normal_cutoff = cutoff / (0.5 * fs)
    # Get the filter coefficients 
    b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)
    y = signal.filtfilt(b, a, data)
    return y

if __name__ == '__main__':
    # time, data, sample_rate = load_test_data_wav('./software/_lib/test.wav', 0, 5)
    time, data, sample_rate = load_test_data_csv('./software/_lib/test_recording_data.csv', 0, 6)
    # time, data, sample_rate = load_test_data_csv('./software/_lib/data.csv', 0, 5)
    # time, data, sample_rate = load_test_data_csv('./software/tmp/data.csv', 0, 5)
    time = np.linspace(0, len(data)/sample_rate, len(data))
    data = np.array(data)
    data = data - np.mean(data)
    # data = butter_lowpass_filter(data, 500, sample_rate, 3)
    # data = signal.savgol_filter(data, 5, 3)
    
    if True:
        # Plot the time domain
        fig, ax = plt.subplots(3, 1)
        ax[0].plot(time, data, '-', linewidth=0.6, alpha = 0.9, color='black')
        ax[0].plot(time, data, 'x', linewidth=0.6, alpha = 0.9, color='black')
        ax[0].set_xlabel('Time (s)')
        ax[0].set_ylabel('Amplitude')
        ax[0].set_title('Audio Signal (time domain)')
        envelope = abs(signal.hilbert(data))
        ax[0].plot(time, envelope, linewidth=0.6, alpha = 0.9, color='blue')
        ax[0].plot(time, envelope, linewidth=0.6, alpha = 0.9, color='red')
        gradient = np.gradient(envelope)
        gradient_peak, _ = signal.find_peaks(gradient, height=max(gradient)*0.3, distance=int(sample_rate*0.05))
        ax[2].plot(time, gradient, linewidth=0.6, alpha = 0.9, color='green')
        ax[2].plot(time[gradient_peak], gradient[gradient_peak], 'x', color='blue')
        ax[0].plot(time[gradient_peak], envelope[gradient_peak], 'x', color='blue')

        spectrum_freq, spectrum_mag = freq_analysis(data, sample_rate)
        ax[1].plot(spectrum_freq, spectrum_mag, linewidth=0.6, alpha = 0.9, color='black')
        ax[1].set_xlabel('Frequency (Hz)')
        ax[1].set_ylabel('Amplitude')
        ax[1].set_title('Audio Signal (frequency domain)')

        # TODO: Find the fundamental frequency of the note
        peaks, _ = signal.find_peaks(spectrum_mag, height=max(spectrum_mag)*0.3, distance=50)
        ax[1].plot(spectrum_freq[peaks], spectrum_mag[peaks], 'x', color='red')
        print('Peaks:', peaks)

        for peak in peaks:
            print('Peak frequency:', spectrum_freq[peak])
            print('Peak note:', freq_to_note(spectrum_freq[peak]))
            ax[1].text(spectrum_freq[peak], spectrum_mag[peak], freq_to_note(spectrum_freq[peak]), fontsize=8, color='blue')
        plt.savefig('./software/tmp/analysis.png')
        plt.show()

    intervals = extract_intervals(data, sample_rate)
    for interval in intervals:
        note, duration = extract_note_and_duration(interval, sample_rate)
        print('Note:', note, 'Duration:', duration)
    
    wavfile.write('./software/tmp/filtered.wav', sample_rate, data.astype(np.int16)*50)