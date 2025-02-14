
import time
import matplotlib.pyplot as plt
import pandas as pd
import os

from Dependencies.R4UART import sendPWMValues, readPWMValues, initiateUART, readMagnetometerValues # UART code 
from Dependencies.calibrateValues import calibrate # magnetometer calibration code 
from Dependencies.extraneous import processStrings, calculateOffsets, millis # import extraneous functions

timeVector = []
timeVar = 0

terminals = initiateUART(True, False)
time.sleep(1)
nanoSer = terminals[0]

magOutputX = []
magOutputY = []
magOutputZ = []

startTime = millis()

lock = False
while(True):

    
    ################################################################################################################## magnetometer reading
    nanoSer.reset_input_buffer()
    nanoSer.reset_output_buffer()

    magnetometerOutput = nanoSer.readline().decode('utf-8').strip().split()
    try: 
        
        magX = round(float(magnetometerOutput[0]), 2)
        magY = round(float(magnetometerOutput[1]), 2)
        magZ = round(float(magnetometerOutput[2]), 2)
        # print(str(magX) + " " + str(magY) + " " + str(magZ))
    
        magOutputX.append(magX)
        magOutputY.append(magY)
        magOutputZ.append(magZ)
    except:
        magOutputX.append(magOutputX[len(magOutputX) - 1])
        magOutputY.append(magOutputY[len(magOutputY) - 1])
        magOutputZ.append(magOutputZ[len(magOutputZ) - 1])
    
    nanoSer.reset_input_buffer()
    nanoSer.reset_output_buffer()
    
    # R4Ser.reset_input_buffer()
    # R4Ser.reset_output_buffer()
    
    timeVector.append(timeVar)
    timeVar += 1
    
    if(millis() - startTime > 10000):
        break
    

fig, ax = plt.subplots(3)

ax[0].plot(timeVector,magOutputX, color = "red", label = "Real")

ax[1].plot(timeVector,magOutputY, color = "red")

ax[2].plot(timeVector,magOutputZ, color = "red")
plt.show()
