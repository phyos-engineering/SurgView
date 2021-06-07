import serial

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ser.flush

string = "{} {} {} {}\n".format("mouse",1,1,0)
ser.write(bytes(string, 'utf-8'))

line = ser.readline().decode('utf-8').rstrip()
print(line)
