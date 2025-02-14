
import time
import matplotlib.pyplot as plt
import pandas as pd
import os

from Dependencies.R4UART import sendPWMValues, readPWMValues, initiateUART, readMagnetometerValues # UART code 
from Dependencies.calibrateValues import calibrate # magnetometer calibration code 
from Dependencies.extraneous import processStrings, calculateOffsets, millis # import extraneous functions

timeVector = [0]
timeVar = 0

terminals = initiateUART(True, True)
time.sleep(1)
nanoSer = terminals[0]
R4Ser = terminals[1]

magOutputX = [0]
magOutputY = [0]
magOutputZ = [0]

startTime = millis()

def isValidString(s: str) -> bool:
    return "." in s and not s.startswith(".")

freqX = 200
freqY = 200
freqZ = 200
sendPWMValues(0, 0, 0, 0, 0, 0, freqX, freqY, freqZ, R4Ser)
time.sleep(2)

sendPWMValues(0, 10, 0, 0, 0, 0, freqX, freqY, freqZ, R4Ser)
print("running")
while(True):

    
    ################################################################################################################## magnetometer reading
    nanoSer.reset_input_buffer()
    nanoSer.reset_output_buffer()

    magnetometerOutput = nanoSer.readline().decode('utf-8').strip().split()
    if magnetometerOutput:
        if ((len(magnetometerOutput) == 3) and isValidString(magnetometerOutput[0])):
           magX = round(float(magnetometerOutput[0]), 2)
           magY = round(float(magnetometerOutput[1]), 2)
           magZ = round(float(magnetometerOutput[2]), 2)
           
           magOutputX.append(magX)
           magOutputY.append(magY)
           magOutputZ.append(magZ)
        else:
           magOutputX.append(magOutputX[len(magOutputX) - 1])
           magOutputY.append(magOutputY[len(magOutputY) - 1])
           magOutputZ.append(magOutputZ[len(magOutputZ) - 1])
        
    R4Ser.reset_input_buffer()
    R4Ser.reset_output_buffer()
    
    timeVector.append(timeVar)
    timeVar += 1
    
    if(millis() - startTime > 10000):
        break
    
   

fig, ax = plt.subplots(3)

ax[0].plot(timeVector,magOutputX, color = "red", label = "Real")

ax[1].plot(timeVector,magOutputY, color = "red")

ax[2].plot(timeVector,magOutputZ, color = "red")
plt.show()


