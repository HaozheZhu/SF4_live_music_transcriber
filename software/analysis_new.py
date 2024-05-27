from pydub import AudioSegment
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal

if __name__ == '__main__':
    song = AudioSegment.from_file("./software/_lib/test_recording.wav", format="wav")
    song = song[200:] # Remove the first 200ms of the song to remove the big noise in ACD on startup
    SEGMENT_MS = 20 # Size of segments to break song into for volume calculations
    volume = [segment.dBFS for segment in song[::SEGMENT_MS]] # dBFS is decibels relative to the maximum possible loudness
    x_axis = np.arange(len(volume)) * (SEGMENT_MS / 1000)
    song_high_passed = song.high_pass_filter(80)
    volume = [segment.dBFS for segment in song_high_passed[::SEGMENT_MS]]
    song_low_passed = song_high_passed.low_pass_filter(2500)
    volume = [segment.dBFS for segment in song_low_passed[::SEGMENT_MS]]
    plt.plot(x_axis, volume, '-')
    plt.xlabel("Time (s)")
    plt.ylabel("Volume (dBFS)")
    plt.title("Volume of song over time")

    volume = np.array(volume)
    PEAK_THRESHOLD_DB = 8
    TROUGH_PEAK_THRESHOLD_DB = 5
    PEAK_DISTANCE_MS = 80
    TROUGH_DISTANCE_MS = 20
    peaks, _ = signal.find_peaks(volume, height=min(volume)+PEAK_THRESHOLD_DB, distance=PEAK_DISTANCE_MS//SEGMENT_MS) 
    troughs, _= signal.find_peaks(-volume)
    filter_troughs = []
    for peak in peaks:
        left_troughs = troughs[troughs < peak]
        left_trough = left_troughs.max() 
        while volume[peak] - volume[left_trough] < TROUGH_PEAK_THRESHOLD_DB:    
            left_troughs = left_troughs[left_troughs != left_trough]
            left_trough = left_troughs.max() 
        right_troughs = troughs[troughs > peak]
        right_trough = right_troughs.min()
        while volume[peak] - volume[right_trough] < TROUGH_PEAK_THRESHOLD_DB:
            right_troughs = right_troughs[right_troughs != right_trough]
            right_trough = right_troughs.min()
        print(left_trough, peak, right_trough)
        plt.plot(x_axis[left_trough], volume[left_trough], 'v', color='blue')
        plt.plot(x_axis[right_trough], volume[right_trough], 'v', color='blue')

    plt.plot(x_axis[peaks], volume[peaks], '^', color='red')
    # plt.plot(x_axis[troughs], volume[troughs], 'v', color='blue')
    plt.show()