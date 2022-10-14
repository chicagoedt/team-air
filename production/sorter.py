import numpy as np
from control import *
from colors import *

# determine if ball is in the chamber
def ballInChamber(sensorRGB):
    if (sensorRGB == (45, 0, 0) or sensorRGB == (255, 0, 0)):
        print('no ball')
        return False
    print('ball')
    return True

# read color 10 times, get the average, then return a string color closest to that average
def getBallColor(control):
    rgbReadings = []
    numReadings = 10

    print("getting average...")

    for i in range(numReadings):
        rgbReadings.append(control.readColor())
        sleep(0.1)

    rgbAverage = np.mean(rgbReadings, 0)

    print("std:", np.std(rgbReadings, 0))
    print("avg:", rgbAverage)

    return getClosestColor(rgbAverage)

# change global variable when button is pressed
def buttonPressed():
    global buttonHasBeenPressed
    buttonHasBeenPressed = True

def runSorter(control):
    # initialize the sequences
    lightColors = {
        "red":(255, 0, 0),
        "orange":(255, 40, 0),
        "yellow":(255, 150, 0),
        "green":(0, 255, 0),
        "blue":(0, 0, 255),
        "purple":(80, 0, 255),
        "pink":(255, 50, 50)
    }

    # set servos to min and turn on vacuum motor
    control.resetServos()
    control.setVacuumMotor(True)

    # when the button is pressed, call the buttonPressed method
    control.button.when_pressed = buttonPressed

    # execution loop
    while (True):
        global buttonHasBeenPressed
        buttonHasBeenPressed = False

        sensorRGB = control.readColor()  # get colorSensor reading

        # ball in the chamber
        if ballInChamber(sensorRGB):
            # get color of ball as a string
            ballColor = getBallColor(control)
            print(ballColor)

            control.setRGB(lightColors[ballColor])  # turn on LED with ballColor

            # if it matches the next color we need, keep it
            if ballColor not in ('orange', 'pink'):
                print("keeping ball")
                control.keepBall()
            else:  # otherwise drop it
                print("dropping ball")
                control.dropBall()

            control.setRGB((0,0,0))  # turn off LED

        if buttonHasBeenPressed:
            break

