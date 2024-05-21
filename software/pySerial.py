import serial

if __name__ == '__main__':
    ser = serial.Serial()
    ser.baudrate = 230400
    ser.port = '/dev/ttyACM0'
    print(ser.name)         # check which port was really used
    