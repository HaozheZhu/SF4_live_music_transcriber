import numpy as np
import scipy.io.wavfile as wavfile
import analysis as analysis
import comms
import draw
import matplotlib.pyplot as plt
import subprocess

if __name__ == '__main__':
    comms.receive('/dev/ttyACM0')

    # time, data, sample_rate = analysis.load_test_data_wav('./software/_lib/test.wav')
    # time, data, sample_rate = analysis.load_test_data_csv('./software/_lib/test_recording_data.csv')
    time, data, sample_rate = analysis.load_test_data_csv('./software/tmp/data.csv')

    intervals = analysis.extract_intervals(data, sample_rate, debug=True)
    notes = []
    durations = []
    for interval, number in zip(intervals, range(len(intervals))):
        note, duration = analysis.extract_note_and_duration(interval, sample_rate, number, debug=False)
        print('Note:', note, 'Duration:', duration)
        notes.append(note)
        durations.append(duration)
    durations = np.apply_along_axis(lambda x: np.round(x*8)/8, 0, durations) # round to the nearest 0.125
    
    draw.draw_music(notes, durations)

    subprocess.call('./software/bash_command.sh')