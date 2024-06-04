import serial
from time import perf_counter, sleep
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.io.wavfile as wavfile

def serial_setup(port_name_string): 
    ser = serial.Serial()
    ser.baudrate = 230400
    ser.port = port_name_string
    ser.open()
    if ser.is_open:
        print("Serial setup complete")
    else:
        print("Serial setup failed, exiting")
        raise SystemExit
    return ser

def read_data(ser):
    data = ser.read(2)
    datalist = list(data)
    data = (datalist[0] << 8) + datalist[1]
    return data

def print_data(data):
    print(perf_counter(), end=" ")
    print(data)

def starting_routine(ser): 
    while input("Input 's' to start: ") not in ['S', 's']:
        pass
    ser.write('S'.encode())
    sleep(0.01)
    print("Starting to record")
    data = read_data(ser)
    while data != 0xFFF2:
        print_data(data)
        data = read_data(ser)
    print('Started') # Start confirmation received from Arduino

def Arduino_reset(ser):
    print("Please reset the Arduino (usually automatic)")
    while ser.read(1) != b'R':
        pass
    print("Arduino reset and ready")    

def receive(port_name_string, debug=False): 
    ser = serial_setup(port_name_string)
    Arduino_reset(ser)
    starting_routine(ser)
    print("Recording data, press Ctrl+C to stop")

    try: 
        data_list = []
        start_time = perf_counter()
        while True:
            data = read_data(ser)
            data_list.append((perf_counter()-start_time, data))
    except KeyboardInterrupt:
        print("Exiting...")
        ser.close()
        print("=====================================")
        print("Number of data points: ", len(data_list))
        print("Time elapsed: ", perf_counter()-start_time)
        print("Sample rate: ", len(data_list)/data_list[-1][0])

        # Remove DC offset
        data_list = np.array(data_list)
        print(f'MEAN: {int(np.mean(data_list[:, 1]))}')
        data_list[:, 1] = (data_list[:, 1] - int(np.mean(data_list[:, 1]))).astype(int)

        df = pd.DataFrame(data_list, columns=['Time', 'Data'])
        df.to_csv('./software/tmp/data.csv', index=False)

        wavfile.write('./software/tmp/data.wav', 4000, data_list[:, 1])


if __name__ == '__main__':
    receive('/dev/ttyACM0', debug=True)

    