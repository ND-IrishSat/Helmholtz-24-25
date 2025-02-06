
import time
import matplotlib.pyplot as plt
import pandas as pd
import os

from Dependencies.R4UART import sendPWMValues, readPWMValues, initiateUART, readMagnetometerValues # UART code 
from Dependencies.calibrateValues import calibrate # magnetometer calibration code 
from Dependencies.extraneous import processStrings, calculateOffsets, millis # import extraneous functions


dataFrame = pd.read_csv("filename") # magnetic fields dataframe

################################################################################ Run parameters

loop = False # if true, simulation will start from the beginning upon reaching the end
runSpeed = 1 # delay time in seconds between each simulation value, so 1 is real time
startPosition = 0 # index of the dataframe to start in

################################################################################

#                x  y  z
currentFields = [0, 0, 0]

#                +x -x +y -y +z -z
currentPWMVals = [0, 0, 0, 0, 0, 0]

timeVector = []
timeVar = 0

i = startPosition

terminals = initiateUART()
time.sleep(1)
nanoSer = terminals[0]
R4Ser = terminals[1]

sendPWMValues(0, 0, 0, 0, 0, 0, R4Ser)
time.sleep(2)


magOutputX = []
magOutputY = []
magOutputZ = []

simulationX = []
simulationY = []
simulationZ = []

while(True):

    ################################################################################################################## magnetometer reading
    nanoSer.reset_input_buffer()
    nanoSer.reset_output_buffer()
    
    R4Ser.reset_input_buffer()
    R4Ser.reset_output_buffer()
    magnetometerOutput = readMagnetometerValues(nanoSer)

    magnetometerOutput = magnetometerOutput.split(" ")
    #print(magnetometerOutput)

    try:
        magX = float(magnetometerOutput[0])
        magY = float(magnetometerOutput[1])
        magZ = float(magnetometerOutput[2])    
        
        calibratedValues = calibrate(magX, magY, magZ) # apply calibration

# #     print("X: " + "{:.2f}".format(magX) + " Y: " + "{:.2f}".format(magY) + " Z: " + "{:.2f}".format(magZ))

        calMagX = round(calibratedValues[0], 2)
        calMagY = round(calibratedValues[1], 2)
        calMagZ = round(calibratedValues[2], 2)
    
    except:
        
        calMagX = magOutputX[len(magOutputX) - 1]
        calMagY = magOutputY[len(magOutputY) - 1]
        calMagZ = magOutputZ[len(magOutputZ) - 1]
    
# #     # purely for readable format, adds necessary zeros to preserve 2 decimal format
    magStrings = processStrings(calMagX, calMagY, calMagZ)

    magOutputX.append(calMagX)
    magOutputY.append(calMagY)
    magOutputZ.append(calMagZ)
    print("X: " + str(magStrings[0]) + " Y: " + str(magStrings[1]) + " Z: " + str(magStrings[2]))


    currentFields[0] = dataFrame.loc[i, 'SIMX']
    currentFields[1] = dataFrame.loc[i, 'SIMY']
    currentFields[2] = dataFrame.loc[i, 'SIMZ']

    simulationX.append(currentFields[0])
    simulationY.append(currentFields[1])
    simulationZ.append(currentFields[2])

    currentPWMVals[0] = dataFrame.loc[i, 'PWM_X+']
    currentPWMVals[1] = dataFrame.loc[i, 'PWM_X-']
    currentPWMVals[2] = dataFrame.loc[i, 'PWM_Y+']
    currentPWMVals[3] = dataFrame.loc[i, 'PWM_Y-']
    currentPWMVals[4] = dataFrame.loc[i, 'PWM_Z+']
    currentPWMVals[5] = dataFrame.loc[i, 'PWM_Z-']

    sendPWMValues(currentPWMVals[2], currentPWMVals[3], currentPWMVals[1], currentPWMVals[0], currentPWMVals[4], currentPWMVals[5])

    i += 1

    if(i == len(dataFrame) - 1):
        if(loop):
            i = startPosition
        else:
            break

    timeVector.append(timeVar)
    timeVar += 1

    time.sleep(runSpeed)


fig, ax = plt.subplots(3)

ax[0].plot(timeVector,magOutputX, color = "red", label = "Real")
ax[0].plot(timeVector, simulationX, color = "blue", label = "PySOL")

ax[1].plot(timeVector,magOutputY, color = "red")
ax[1].plot(timeVector, simulationY,  color = "blue")

ax[2].plot(timeVector,magOutputZ, color = "red")
ax[2].plot(timeVector, simulationZ, color = "blue")
