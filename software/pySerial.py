import serial
import time

if __name__ == '__main__':
    ser = serial.Serial()
    ser.baudrate = 230400
    ser.port = '/dev/ttyACM2'
    print(ser)         # check which port was really used
    
    ser.open()
    print(ser.is_open) # True for opened port

    time.sleep(5)
    ser.write('S'.encode())
    print('Start') # Start confirmation received from Arduino

    while True:
        data = ser.read(2)
        datalist = list(data)
        data = (datalist[0] << 8) + datalist[1]
        print(time.time(), end=" ")
        print(data)
    