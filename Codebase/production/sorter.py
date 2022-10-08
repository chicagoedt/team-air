from gpiozero import Servo
import board
import adafruit_tcs34725
import numpy as np

from colors import *
from servoControl import *

# initialize sensor and servos
i2c = board.I2C()
colorSensor = adafruit_tcs34725.TCS34725(i2c)
doorServo = Servo(14)
pushServo = Servo(15)
vacuumMotor = Servo(18)
chamberServo = Servo(23)

# initialize the sequences
s1 = ("blue", "purple", "red", "blue")
s2 = ("green", "yellow", "red", "green")
s3  = ("blue", "purple", "red", "green")
sequence = (s1, s2, s3)
seqIndex = 0


# set this to the "ambient" chamber rgb reading of the color sensor
ambientColor = (67, 10, 3)
# (255, 0, 0)
# (45, 0, 0)

#caleb's attempt to boost the color
def colorBooster(rgbValues):
    r = rgbValues[0] * 1.4
    g = rgbValues[1] * 1.4
    b = rgbValues[2] * 1.4
    return [r,g,b]

# determine if ball is in the chamber (sensor color a certain distance from ambient color)
def ballInChamber(sensorRGB):
    if (sensorRGB == (45, 0 , 0) or sensorRGB == (255, 0, 0)):
        print('no ball')
        return False
    print('ball')
    return True

    # distance = np.linalg.norm(np.array(sensorRGB) - ambientColor)
    # print(distance)
    # return distance > 20 # return true if color is within some distance
    # return True


# prompt to look for color
# user_input = input("Press enter to start")
runSorter = True
doorServo.min()
setVacuumMotor(vacuumMotor, True)  # turn vacuum on
while(runSorter):
    sensorRGB = colorSensor.color_rgb_bytes

    # ball in the chamber
    if ballInChamber(sensorRGB):
        # get color of ball as a string
        ballColor = getBallColor(colorSensor)
        print(ballColor)

        # if it matches the next color we need, keep it
        if ballColor == s1[seqIndex]:
            print("keeping ball")
            keepBall(doorServo, pushServo, vacuumMotor)
            seqIndex += 1
        else:  # otherwise drop it
            print("dropping ball")
            dropBall(vacuumMotor)

    # reached end of specified sequence
    if seqIndex == len(s1):
        dropSequence(chamberServo);

    # user_input = input("Press enter to read color or # to stop: ")
    # if (user_input == "#"):
    #     runSorter = False



# wtf is servo jitter?!?!?! look into it
# -chris
