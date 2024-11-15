# Adafruit Mag code

import bleak
import asyncio
import struct
import time
import numpy
import serial

from R4UART import sendPWMValues, readPWMValues, initiateUART, readMagnetometerValues # UART code 
from PID import PIDsetpoints, computePID # PID code
from calibrateValues import calibrate # magnetometer calibration code 
from extraneous import processStrings # import extraneous functions

debug = False # enables extra print statements (slow)
manual = False # when false, PID is enabled

# initial setpoints, for manual mode set desired ones here

terminals = initiateUART()
nanoSer = terminals[0]
R4Ser = terminals[1]

while True:
    
    # initial duty cycles, for manual mode set desired ones here
    Xp = 0.0
    Xn = 0.0

    Yp = 0.0
    Yn = 0.0

    Zp = 0.0
    Zn = 0.0
    
    setX = 0
    setY = 0
    setZ = 0
                    
    #print("X: " + "{:.2f}".format(magX) + " Y: " + "{:.2f}".format(magY) + " Z: " + "{:.2f}".format(magZ))

    magnetometerOutput = readMagnetometerValues(nanoSer)

    magnetometerOutput = magnetometerOutput.split(" ")

    magX = float(magnetometerOutput[0])
    magY = float(magnetometerOutput[1])
    magZ = float(magnetometerOutput[2])

    calibratedValues = calibrate(magX, magY, magZ) # apply calibration

    print("X: " + "{:.2f}".format(magX) + " Y: " + "{:.2f}".format(magY) + " Z: " + "{:.2f}".format(magZ))

    magX = round(calibratedValues[0], 2)
    magY = round(calibratedValues[1], 2)
    magZ = round(calibratedValues[2], 2)
    
    # purely for readable format, adds necessary zeros to preserve 2 decimal format
    magStrings = processStrings(magX, magY, magZ)
    
    #print("X: " + str(magStrings[0]) + " Y: " + str(magStrings[1]) + " Z: " + str(magStrings[2]))

    
    if not(manual):
        PIDsetpoints(setX, setY, setZ)
        results = computePID(magX, magY, magZ)
        
        xTemp = results[0]
        yTemp = results[1]
        zTemp = results[2]
        
        if(xTemp < 0):
            Xn = xTemp * -1
            Xp = 0
        else:
            Xp = xTemp
            Xn = 0
        
        if(yTemp < 0):
            Yn = yTemp * -1
            Yp = 0
        else:
            Yp = yTemp
            Yn = 0
            
        if(zTemp < 0):
            Zn = zTemp * -1
            Zp = 0
        else:
            Zp = zTemp
            Zn = 0
    time.sleep(0.1)
    sendPWMValues(Yp, Yn, Xn, Xp, Zp, Zn, R4Ser) # sends PWM to R4 (currently trying with 1 direction)

    if(debug):
        readPWMValues(R4Ser)
    


