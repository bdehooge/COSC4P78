import serial

ser = serial.Serial('COM9', 115200, timeout=1) #Remember to change COM number
print( ser.readline().decode('utf-8').strip() ) #Should say 'hi.'
while True: #Might time out as blank lines if you don't move the knobs
    print( ser.readline().decode('utf-8').strip() )
    