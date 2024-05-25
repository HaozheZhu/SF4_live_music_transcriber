import serial
import time

def serial_setup(): 
    ser = serial.Serial()
    ser.baudrate = 230400
    ser.port = '/dev/ttyACM0'
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
    print(time.time(), end=" ")
    print(data)

def starting_routine(ser): 
    while input("Input 's' to start: ") not in ['S', 's']:
        pass
    ser.write('S'.encode())
    time.sleep(0.01)
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

if __name__ == '__main__':
    ser = serial_setup()
    Arduino_reset(ser)
    starting_routine(ser)
    print("Recording data, press Ctrl+C to stop")

    try: 
        data_list = []
        start_time = time.time()
        while True:
            data = read_data(ser)
            data_list.append((time.time()-start_time, data))
    except KeyboardInterrupt:
        print("Exiting...")
        ser.close()
        print("=====================================")
        print("Number of data points: ", len(data_list))
        print("Time elapsed: ", time.time()-start_time)
        print("First 10 data points: ")
        for i in range(10): 
            print(data_list[i])
        print("Last 10 data points: ")
        for i in range(-10, 0): 
            print(data_list[i])
    