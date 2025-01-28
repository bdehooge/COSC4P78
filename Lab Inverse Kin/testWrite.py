import serial

ser = serial.Serial('COM9', 115200, timeout=1) #Remember to change COM number
print( ser.readline().decode('utf-8').strip() ) #Should say 'hi.'


ser.read(1)
pos = "{200,200,2}\n"
pos = pos.encode()
ser.write(pos)
print( ser.readline().decode('utf-8').strip() ) #Should say 'hi.'

