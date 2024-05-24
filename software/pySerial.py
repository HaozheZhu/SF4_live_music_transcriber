import serial
import time

def read_data(ser):
    data = ser.read(2)
    datalist = list(data)
    data = (datalist[0] << 8) + datalist[1]
    return data

def print_data(data):
    print(time.time(), end=" ")
    print(data)

if __name__ == '__main__':
    ser = serial.Serial()
    ser.baudrate = 230400
    ser.port = '/dev/ttyACM4'
    print(ser)         # check which port was really used
    
    ser.open()
    print(ser.is_open) # True for opened port

    time.sleep(5)
    ser.write('S'.encode())
    time.sleep(0.1)
    print("Starting")
    data = read_data(ser)
    while data != 0xFFF2:
        print_data(data)
        data = read_data(ser)
    print('Started') # Start confirmation received from Arduino

    while True:
        data = read_data(ser)
        print_data(data)
    