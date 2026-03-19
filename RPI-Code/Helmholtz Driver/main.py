# Adafruit Mag code

import bleak
import asyncio
import struct
import time
import numpy
import serial
import math

import matplotlib.pyplot as plt

from R4UART import sendPWMValues, readPWMValues, initiateUART, readMagnetometerValues # UART code 
#from PID import PIDsetpoints, computePID # PID code
from PID_new import xPID, yPID, zPID
from calibrateValues import calibrate # magnetometer calibration code 
from extraneous import processStrings, calculateOffsets # import extraneous functions

debug = False # enables extra print statements (slow)
manual = False # when false, PID is enabled
initializing = False # leave true to find earth magnetic field offsets for PID
numOfOffsetVals = 50 # number of measurements script will take before calculating earth offset 
xOffset = 0
yOffset = 0
zOffset = 0

# initial setpoints, for manual mode set desired ones here

terminals = initiateUART()
time.sleep(1)
nanoSer = terminals[0]
R4Ser = terminals[1]


# initial duty cycles, for manual mode set desired ones here
Xp = 0.0
Xn = 0.0

Yp = 0.0
Yn = 0.0

Zp = 0.0
Zn = 0.0
    
    # initial set positions, implement pysol reading here
    # Array for changing set values
# xSet = [0, 0, 0, 0]
# ySet = [0, 10, 30, -10]
# zSet = [0, 0, 0, 0]

xRamp = 0
yRamp = 0
zRamp = 0

    # arrays to hold initial offset values
xAvg = []
yAvg = []
zAvg = []

maxVal = 100 # max value of pwm signal (control output)

    # turn off cage at start
sendPWMValues(0, 0, 0, 0, 0, 0, R4Ser)
time.sleep(2)

magOutputX = [0]
magOutputY = [0]
magOutputZ = [0]

pwmPosOutputX = [0]
pwmNegOutputX = [0]
pwmPosOutputY = [0]
pwmNegOutputY = [0]
pwmPosOutputZ = [0]
pwmNegOutputZ = [0]
i = 1

startTime = time.time(); # get start time
timeVec = [0]

while (time.time()-startTime < 15):
    timeVec.append(time.time()-startTime)               
    ################################################################################################################## magnetometer reading
    #Change set values
#     if (time.time()-startTime < 4):
#         set_index = 0
#     elif (time.time()-startTime < 10):
#         set_index = 1
#     elif (time.time()-startTime < 15):
#         set_index = 2
#     elif (time.time()-startTime < 16):
#         set_index = 3

    xRamp = 70 * math.sin(2 * math.pi * (time.time()-startTime) / 15)

    # Ramp Y values
    # yRamp = (13/12) * (-1 * (time.time()-startTime)) * ((time.time()-startTime) - 15)
    yRamp = -70 * math.sin(2 * math.pi * (time.time()-startTime) / 15)
    
    zRamp = 60 * math.cos(6 * math.pi * (time.time()-startTime) / 15)
    
    #print("X: " + "{:.2f}".format(magX) + " Y: " + "{:.2f}".format(magY) + " Z: " + "{:.2f}".format(magZ))
    nanoSer.reset_input_buffer()
    nanoSer.reset_output_buffer()
    
    R4Ser.reset_input_buffer()
    R4Ser.reset_output_buffer()
    magnetometerOutput = readMagnetometerValues(nanoSer)

    magnetometerOutput = magnetometerOutput.split(" ")
    # print(magnetometerOutput)

    magX = float(magnetometerOutput[0])
    magY = float(magnetometerOutput[1])
    magZ = float(magnetometerOutput[2])

    calibratedValues = calibrate(magX, magY, magZ) # apply calibration

#     print("X: " + "{:.2f}".format(magX) + " Y: " + "{:.2f}".format(magY) + " Z: " + "{:.2f}".format(magZ))

    calMagX = round(calibratedValues[0], 2)
    calMagY = round(calibratedValues[1], 2)
    calMagZ = round(calibratedValues[2], 2)
    
#     # purely for readable format, adds necessary zeros to preserve 2 decimal format
    magStrings = processStrings(calMagX, calMagY, calMagZ)
    magOutputX.append(calMagX)
    magOutputY.append(calMagY)
    magOutputZ.append(calMagZ)
    print("X: " + str(magStrings[0]) + " Y: " + str(magStrings[1]) + " Z: " + str(magStrings[2]))
    ##################################################################################################################

    if(initializing):
        xAvg.append(calMagX)
        yAvg.append(magY)
        zAvg.append(magZ)
        if(len(xAvg) >= numOfOffsetVals):
            xOffset, yOffset, zOffset = calculateOffsets(xAvg, yAvg, zAvg)
            initializing = False
            #print(str(xOffset) + " " + str(yOffset) + " " + str(zOffset))

    [Xp, Xn] = xPID(xRamp, calMagX, magOutputX[i-1], pwmPosOutputX[i-1], pwmNegOutputX[i-1], maxVal, timeVec[i]-timeVec[i-1])
    [Yp, Yn] = yPID(yRamp, calMagY, magOutputY[i-1], pwmPosOutputY[i-1], pwmNegOutputY[i-1], maxVal, timeVec[i]-timeVec[i-1])
    [Zp, Zn] = zPID(zRamp, calMagZ, magOutputZ[i-1], pwmPosOutputZ[i-1], pwmNegOutputZ[i-1], maxVal, timeVec[i]-timeVec[i-1]) 
    

    pwmPosOutputX.append(Xp)
    pwmNegOutputX.append(Xn)
    
    pwmPosOutputY.append(Yp)
    pwmNegOutputY.append(Yn)
    
    pwmPosOutputZ.append(Zp)
    pwmNegOutputZ.append(Zn)

        
        #print(str(xTemp) + " " + str(yTemp) + " " + str(zTemp))

    time.sleep(0.1)
    #sendPWMValues(Yp, Yn, 0, 0, 0, 0, R4Ser)
    #sendPWMValues(0, 0, Xn, Xp, 0, 0, R4Ser)
    #sendPWMValues(0, 0, 0, 0, Zp, Zn, R4Ser)
    sendPWMValues(Yp, Yn, Xn, Xp, Zp, Zn, R4Ser)
    #readPWMValues(R4Ser)
    #sendPWMValues(Yp, Yn, Xn, Xp, Zp, Zn, R4Ser) # sends PWM to R4 (currently trying with 1 direction)

    i+=1
    
    
fig, ax = plt.subplots(3)
ax[0].plot(timeVec, magOutputX)
ax[0].set_ylim(-75, 75)
ax[1].plot(timeVec, magOutputY)
ax[1].set_ylim(-75, 75)
ax[2].plot(timeVec, magOutputZ)
ax[2].set_ylim(-50, 50)
plt.show()


