import serial

ser = serial.Serial('COM9', 115200, timeout=1) #Remember to change COM number
print( ser.readline().decode('utf-8').strip() ) #Should say 'hi.'

penX = 380
penY = 370
penPosition = 1

origin = "{" + str(penX) + "," + str(penY) + "," + str(penPosition) + "}\n"
ser.write(origin.encode())

radius = 50
startAngle = 75

penX -= 2
pos = "{" + str(penX) + "," + str(penY) + "," + str(penPosition) + "}\n"
ser.write(pos.encode())



