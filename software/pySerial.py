import serial

if __name__ == '__main__':
    ser = serial.Serial()
    ser.baudrate = 230400
    ser.port = '/dev/ttyACM0'
    print(ser)         # check which port was really used
    
    ser.open()
    print(ser.is_open) # True for opened port

    data = 0 
    while True:
        data = ser.read(2)
        datalist = list(data)
        data = (datalist[0] << 8) + datalist[1]
        print(data)
    