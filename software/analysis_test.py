from pydub import AudioSegment
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal
from scipy.io import wavfile
import analysis

if __name__ == '__main__':
    data = AudioSegment.from_file("./software/_lib/test_recording.wav", format="wav")
    data = data.high_pass_filter(80)
    data = data.low_pass_filter(2500)
    data = data[200:] # Remove the first 200ms of the data to remove the big noise in ACD on startup
    SEGMENT_MS = 1 # Size of segments to break data into for volume calculations
    volume = [segment.dBFS for segment in data[::SEGMENT_MS]] # dBFS is decibels relative to the maximum possible loudness
    x_axis = np.arange(len(volume)) * (SEGMENT_MS / 1000)
    
    fig, ax = plt.subplots(2, 1)
    ax[0].plot(x_axis, volume, '-')
    ax[0].set_xlabel("Time (s)")
    ax[0].set_ylabel("Volume (dBFS)")
    ax[0].set_title("Filtered audio volume in dB")

    volume = np.array(volume)
    PEAK_THRESHOLD_DB = 10
    TROUGH_PEAK_THRESHOLD_DB = 8
    PEAK_DISTANCE_MS = 80
    TROUGH_DISTANCE_MS = 20
    peaks, _ = signal.find_peaks(volume, height=min(volume)+PEAK_THRESHOLD_DB, distance=PEAK_DISTANCE_MS//SEGMENT_MS) 
    troughs, _= signal.find_peaks(-volume)
    left_peak_right = []
    for peak in peaks:
        left_troughs = troughs[troughs < peak]
        if left_troughs.size == 0:
            left_trough =  None
        else:
            left_trough = left_troughs.max()
            while volume[peak] - volume[left_trough] < TROUGH_PEAK_THRESHOLD_DB:    
                left_troughs = left_troughs[left_troughs != left_trough]
                if left_troughs.size == 0:
                    left_trough =  None
                    break
                left_trough = left_troughs.max() 
            right_troughs = troughs[troughs > peak]
        if right_troughs.size == 0:
            right_trough = None
        else:
            right_trough = right_troughs.min()
            while volume[peak] - volume[right_trough] < TROUGH_PEAK_THRESHOLD_DB:
                right_troughs = right_troughs[right_troughs != right_trough]
                if right_troughs.size == 0:
                    right_trough = None
                    break
                right_trough = right_troughs.min()
        left_peak_right.append((left_trough, peak, right_trough))
        if left_trough is not None:
            ax[0].plot(x_axis[left_trough], volume[left_trough], 'v', color='blue')
        if right_trough is not None:
            ax[0].plot(x_axis[right_trough], volume[right_trough], 'v', color='blue')

    ax[0].plot(x_axis[peaks], volume[peaks], '^', color='red')

    time, data, sample_rate = analysis.load_test_data_csv('./software/_lib/test_recording_data.csv', 0.2, 6)
    time = np.linspace(0, len(data)/sample_rate, len(data))
    ax[1].plot(time, data, '-', linewidth=0.6, alpha = 0.9, color='black')
    ax[1].set_xlabel('Time (s)')
    ax[1].set_ylabel('Amplitude')
    ax[1].set_title('Raw audio amplitude')

    # for left_trough, peak, right_trough in left_peak_right:
    #     if left_trough is not None:
    #         ax[0].axvline(x_axis[left_trough], color='blue')
    #         ax[1].axvline(x_axis[left_trough], color='blue')
    #         ax[0].plot(x_axis[left_trough], volume[left_trough], 'v', color='blue')
        
    #     if right_trough is not None:
    #         ax[0].axvline(x_axis[right_trough], color='blue')
    #         ax[1].axvline(x_axis[right_trough], color='blue')
    #         ax[0].plot(x_axis[right_trough], volume[right_trough], 'v', color='blue')
    
    plt.show()