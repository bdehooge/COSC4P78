from serial import Serial
import math
import queue

innerArmLength = 5
outerArmLength = 5
penState = 1 #1 for up, 2 for down?

def main():

    ser = Serial('COM1', 115200, timeout=1) #Remember to change COM number
    print( ser.readline().decode('utf-8').strip() ) #Should say 'hi.'

    q = queue.Queue()
    print("Please enter coordinates in the form x,y ie: 100,100 . To change pen state type 'penUp' or 'penDown'. Enter 'quit' to exit: ")
    
    while True:
        coordinates = input("Enter Coordinates: ")
        if coordinates == "quit":
            break
        coordinates = coordinates.split(",")
        x, y = coordinates[0], coordinates[1]
        q.put((int(x), int(y)))
    
    print("Coordinates entered. Press Enter to begin.")
    input()
    
    while q.qsize() > 0:
        x, y = q.get()
        shoulderMotorAngle, elbowMotorAngle = getAngles(x, y)
        writeAngles(ser, shoulderMotorAngle, elbowMotorAngle, penState)
        print("Job done!")

def getAngles(x, y):
    hypotenuse = math.sqrt(x**2 + y**2)
    hypotenuseAngle = math.asin(x/hypotenuse)
    innerAngle = math.acos((hypotenuse**2 + innerArmLength**2 - outerArmLength**2)/(2*hypotenuse*innerArmLength))
    shoulderMotorAngle = hypotenuseAngle - innerAngle
    outerAngle = math.acos((innerArmLength**2 + outerArmLength**2 - hypotenuse**2)/(2*innerArmLength*outerArmLength))
    elbowMotorAngle = math.pi - outerAngle
    print(math.degrees(shoulderMotorAngle), math.degrees(elbowMotorAngle))
    return (math.degrees(shoulderMotorAngle), math.degrees(elbowMotorAngle))    

def writeAngles(ser, shoulderMotorAngle, elbowMotorAngle, penState):
    angleString = "{%d,%d,%d}\n" % (shoulderMotorAngle, elbowMotorAngle, penState)
    print(angleString)
    angleString = angleString.encode()
    ser.write(angleString)

if __name__ == "__main__":
    main()