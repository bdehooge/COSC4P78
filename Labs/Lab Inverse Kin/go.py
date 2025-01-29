from serial import Serial
import math
import queue

innerArmLength = 5
outerArmLength = 5


def main():

    penState = 1 #1 for up, 2 for down?

    ser = Serial('COM1', 115200, timeout=1) #Remember to change COM number
    print( ser.readline().decode('utf-8').strip() ) #Should say 'hi.'

    q = queue.Queue()
    print("Please enter coordinates in the form x,y ie: 100,100 . To change pen state type 'pen'. Enter 'quit' to exit: ")
    
    #Input Loop
    while True:
        inpString = input("Enter Coordinates: ")
        if inpString == "quit":
            break
        inpList = inpString.split(",")
        if inpList[0] == "pen":
            q.put("pen")
        else:
            x, y = inpList[0], inpList[1]
            q.put((int(x), int(y)))
    
    print("Coordinates entered. Press Enter to begin.")
    input()
    
    #Running Loop
    while q.qsize() > 0:
        if q.get() == "pen":
            penState = 2 if penState == 1 else 1
            print("Pen state changed to: ", penState)
            continue
        else:
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