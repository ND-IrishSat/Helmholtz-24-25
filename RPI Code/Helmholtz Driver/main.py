# Adafruit Mag code

import bleak
import asyncio
import struct
import time
import numpy
import serial

import matplotlib.pyplot as plt

from R4UART import sendPWMValues, readPWMValues, initiateUART, readMagnetometerValues # UART code 
#from PID import PIDsetpoints, computePID # PID code
from PID_new import PID_fun
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
xSet = 0
ySet = 0
zSet = 0

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
i = 1;

startTime = time.time(); # get start time
timeVec = [0]

# while (time.time()-startTime < 10):
#     timeVec.append(time.time()-startTime)               
#     ################################################################################################################## magnetometer reading
#     #print("X: " + "{:.2f}".format(magX) + " Y: " + "{:.2f}".format(magY) + " Z: " + "{:.2f}".format(magZ))
# 
#     magnetometerOutput = readMagnetometerValues(nanoSer)
# 
#     magnetometerOutput = magnetometerOutput.split(" ")
# 
#     magX = float(magnetometerOutput[0])
#     magY = float(magnetometerOutput[1])
#     magZ = float(magnetometerOutput[2])
# 
#     calibratedValues = calibrate(magX, magY, magZ) # apply calibration
# 
#     #print("X: " + "{:.2f}".format(magX) + " Y: " + "{:.2f}".format(magY) + " Z: " + "{:.2f}".format(magZ))
# 
#     magX = round(calibratedValues[0], 2)
#     magY = round(calibratedValues[1], 2)
#     magZ = round(calibratedValues[2], 2)
#     
#     # purely for readable format, adds necessary zeros to preserve 2 decimal format
#     magStrings = processStrings(magX, magY, magZ)
#     
#     print("X: " + str(magStrings[0]) + " Y: " + str(magStrings[1]) + " Z: " + str(magStrings[2]))
#     ##################################################################################################################
# 
#     if(initializing):
#         xAvg.append(magX)
#         yAvg.append(magY)
#         zAvg.append(magZ)
#         if(len(xAvg) >= numOfOffsetVals):
#             xOffset, yOffset, zOffset = calculateOffsets(xAvg, yAvg, zAvg)
#             initializing = False
#             #print(str(xOffset) + " " + str(yOffset) + " " + str(zOffset))
# 
#     
#     if (not(manual) and not(initializing)):
#         PIDsetpoints(xSet, ySet, zSet)
#         magOutput.append(magX)
#         
#         
#         results = computePID(magX, magY, magZ)
#         
#         xTemp = results[0]
#         yTemp = results[1]
#         zTemp = results[2]
#         
#         dutyCycleOutput.append(xTemp)
#         
#         if(xTemp < 0):
#             Xn = xTemp
#             Xp = 0
#         else:
#             Xp = xTemp
#             Xn = 0
#         
#         if(yTemp < 0):
#             Yn = yTemp * -1
#             Yp = 0
#         else:
#             Yp = yTemp
#             Yn = 0
#             
#         if(zTemp < 0):
#             Zn = zTemp * -1
#             Zp = 0
#         else:
#             Zp = zTemp
#             Zn = 0
#         
#         #print(str(xTemp) + " " + str(yTemp) + " " + str(zTemp))
# 
#     time.sleep(0.1)
#     sendPWMValues(0, 0, Xn, Xp, 0, 0, R4Ser)
#     #sendPWMValues(Yp, Yn, Xn, Xp, Zp, Zn, R4Ser) # sends PWM to R4 (currently trying with 1 direction)
# 
#     if(debug):
#         readPWMValues(R4Ser)
#     i+=1


while (time.time()-startTime < 10):
    timeVec.append(time.time()-startTime)               
    ################################################################################################################## magnetometer reading
    #print("X: " + "{:.2f}".format(magX) + " Y: " + "{:.2f}".format(magY) + " Z: " + "{:.2f}".format(magZ))
    nanoSer.reset_input_buffer()
    nanoSer.reset_output_buffer()
    
    R4Ser.reset_input_buffer()
    R4Ser.reset_output_buffer()
    magnetometerOutput = readMagnetometerValues(nanoSer)

    magnetometerOutput = magnetometerOutput.split(" ")

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

    [Xp, Xn] = PID_fun(xSet, calMagX, magOutputX[i-1], pwmPosOutputX[i-1], pwmNegOutputX[i-1], maxVal, timeVec[i]-timeVec[i-1])
    [Yp, Yn] = PID_fun(ySet, calMagY, magOutputY[i-1], pwmPosOutputY[i-1], pwmNegOutputY[i-1], maxVal, timeVec[i]-timeVec[i-1])
    [Zp, Zn] = PID_fun(zSet, calMagZ, magOutputZ[i-1], pwmPosOutputZ[i-1], pwmNegOutputZ[i-1], maxVal, timeVec[i]-timeVec[i-1]) 
    
#     Xp += 5
#     
#     if (Xp >=100):
#         Xp = 100

    pwmPosOutputX.append(Xp)
    pwmNegOutputX.append(Xn)
    
    pwmPosOutputY.append(Yp)
    pwmNegOutputY.append(Yn)
    
    pwmPosOutputZ.append(Zp)
    pwmNegOutputZ.append(Zn)

        
        #print(str(xTemp) + " " + str(yTemp) + " " + str(zTemp))

    time.sleep(0.1)
    sendPWMValues(Yp, Yn, Xn, Xp, Zp, Zn, R4Ser)
    readPWMValues(R4Ser)
    #sendPWMValues(Yp, Yn, Xn, Xp, Zp, Zn, R4Ser) # sends PWM to R4 (currently trying with 1 direction)

    i+=1
    
    
fig, ax = plt.subplots(3)
ax[0].plot(timeVec, magOutputX)
ax[1].plot(timeVec, magOutputY)
ax[2].plot(timeVec, magOutputZ)
plt.show()


