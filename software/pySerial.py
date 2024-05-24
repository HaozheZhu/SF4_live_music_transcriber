import serial
import time

def serial_setup(): 
    ser = serial.Serial()
    ser.baudrate = 230400
    ser.port = '/dev/ttyACM0'
    print(ser)         # check which port was really used
    
    ser.open()
    print(ser.is_open) # True for opened port
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
    time.sleep(0.1)
    print("Starting")
    data = read_data(ser)
    while data != 0xFFF2:
        print_data(data)
        data = read_data(ser)
    print('Started') # Start confirmation received from Arduino

if __name__ == '__main__':
    ser = serial_setup()
    print("Please reset the Arduino")
    while ser.read(1) != b'R':
        pass
    print("Arduino ready")
    starting_routine(ser)

    while True:
        data = read_data(ser)
        print_data(data)
    