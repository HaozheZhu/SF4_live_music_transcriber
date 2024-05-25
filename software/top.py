import numpy as np
import scipy.io.wavfile as wavfile
import analysis
import comms

if __name__ == '__main__':
    time, data, sample_rate = analysis.load_test_data('./software/_lib/test.wav', 0, 5)
    intervals = analysis.extract_intervals(data, sample_rate)
    notes = []
    durations = []
    for interval in intervals:
        note, duration = analysis.extract_note_and_duration(interval, sample_rate)
        print('Note:', note, 'Duration:', duration)
        notes.append(note)
        durations.append(duration)
    durations = np.apply_along_axis(lambda x: np.round(x*8)/8, 0, durations) # round to the nearest 0.125
    print('-----------------------------------')
    print('Notes:', notes)
    print('Durations:', durations)

    
