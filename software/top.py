import numpy as np
import scipy.io.wavfile as wavfile

if __name__ == '__main__':
    sample_rate, data = wavfile.read('./software/test.wav') # data has two channels, left and right
    data = data[:, 0]  # Use only one channel
    start_sec = 0.0
    end_sec = 5
    time = np.arange(0, float(data.shape[0]), 1) / sample_rate
    # Use only the first few seconds for testing purposes
    time = time[(int(start_sec*sample_rate)):(int(end_sec*sample_rate))] 
    data = data[(int(start_sec*sample_rate)):(int(end_sec*sample_rate))] 

    print('Sample rate:', sample_rate)
    print('Total samples:', len(data))
    print('Duration:', len(data) / sample_rate, 'seconds')

    
