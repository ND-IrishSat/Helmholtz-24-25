
import time
import matplotlib.pyplot as plt
import pandas as pd
import os

from Dependencies.R4UART import sendPWMValues, readPWMValues, initiateUART, readMagnetometerValues # UART code 
from Dependencies.calibrateValues import calibrate # magnetometer calibration code 
from Dependencies.extraneous import processStrings, calculateOffsets, millis # import extraneous functions


dataFrame = pd.read_csv("runZeroed.csv") # magnetic fields dataframe

################################################################################ Run parameters

loop = True # if true, simulation will loop 1 value
runTime = 10000 # # if loop is true, the simulation will only loop for this number of miliseconds

startPosition = 0 # index of the dataframe to start in
runSpeed = 100 # time in miliseconds between each change in field, so 1000 is real time

################################################################################

#                x  y  z
currentFields = [0, 0, 0]

#                +x -x +y -y +z -z
currentPWMVals = [0, 0, 0, 0, 0, 0]

realTimeVector = []
timeVar = 0

terminals = initiateUART(True, True)
time.sleep(1)
nanoSer = terminals[0]
R4Ser = terminals[1]

sendPWMValues(0, 0, 0, 0, 0, 0, R4Ser)
time.sleep(2)



trueMagOutputX = []
trueMagOutputY = []
trueMagOutputZ = []
totalMagOutput = []

simulationX = []
simulationY = []
simulationZ = []
simulationTotal = []
simulationPosition = 0

currentPWMVals[0] = dataFrame.loc[simulationPosition, 'PWM_X+']
currentPWMVals[1] = dataFrame.loc[simulationPosition, 'PWM_X-']
currentPWMVals[2] = dataFrame.loc[simulationPosition, 'PWM_Y+']
currentPWMVals[3] = dataFrame.loc[simulationPosition, 'PWM_Y-']
currentPWMVals[4] = dataFrame.loc[simulationPosition, 'PWM_Z+']
currentPWMVals[5] = dataFrame.loc[simulationPosition, 'PWM_Z-']

def isValidString(s: str) -> bool:
    return "." in s and not s.startswith(".")

sendPWMValues(currentPWMVals[2], currentPWMVals[3], currentPWMVals[1], currentPWMVals[0], currentPWMVals[4], currentPWMVals[5], R4Ser)
time.sleep(1)

realTimeVector = []
realTime = 0

t0 = millis()
pwmTime = t0

while(True):

    ##################################################################################################### magnetometer reading 
    nanoSer.reset_input_buffer()
    nanoSer.reset_output_buffer()
    
    R4Ser.reset_input_buffer()
    R4Ser.reset_output_buffer()
    magnetometerOutput = nanoSer.readline().decode('utf-8').strip().split()
    if magnetometerOutput:
        if ((len(magnetometerOutput) == 3) and isValidString(magnetometerOutput[0])):
           magX = round(float(magnetometerOutput[0]), 2)
           magY = round(float(magnetometerOutput[1]), 2)
           magZ = round(float(magnetometerOutput[2]), 2)
           
           trueMagOutputX.append(magX)
           trueMagOutputY.append(magY)
           trueMagOutputZ.append(magZ)
        else:
           trueMagOutputX.append(trueMagOutputX[len(trueMagOutputX) - 1])
           trueMagOutputY.append(trueMagOutputY[len(trueMagOutputY) - 1])
           trueMagOutputZ.append(trueMagOutputZ[len(trueMagOutputZ) - 1])
           
           magX = trueMagOutputX[len(trueMagOutputX) - 1]
           magY = trueMagOutputY[len(trueMagOutputY) - 1]
           magZ = trueMagOutputZ[len(trueMagOutputZ) - 1]

           
    #####################################################################################################
    totalMag = pow(((magX * magX) + (magY * magY) + (magZ * magZ)), 0.5)
    totalMagOutput.append(totalMag)

    if(millis() - pwmTime >= runSpeed):
        pwmTime = millis()

        simulationPosition += 1

        if(loop):
            simulationPosition = 0
        
        currentPWMVals[0] = dataFrame.loc[simulationPosition, 'PWM_X+']
        currentPWMVals[1] = dataFrame.loc[simulationPosition, 'PWM_X-']
        currentPWMVals[2] = dataFrame.loc[simulationPosition, 'PWM_Y+']
        currentPWMVals[3] = dataFrame.loc[simulationPosition, 'PWM_Y-']
        currentPWMVals[4] = dataFrame.loc[simulationPosition, 'PWM_Z+']
        currentPWMVals[5] = dataFrame.loc[simulationPosition, 'PWM_Z-']

        sendPWMValues(currentPWMVals[2], currentPWMVals[3], currentPWMVals[1], currentPWMVals[0], currentPWMVals[4], currentPWMVals[5], R4Ser)

        currentFields[0] = dataFrame.loc[simulationPosition, 'SIMX']
        currentFields[1] = dataFrame.loc[simulationPosition, 'SIMY']
        currentFields[2] = dataFrame.loc[simulationPosition, 'SIMZ']
        
    simTotal = pow(((currentFields[0] * currentFields[0]) + (currentFields[1] * currentFields[1]) + (currentFields[2] * currentFields[2])), 0.5)

    simulationX.append(currentFields[0])
    simulationY.append(currentFields[1])
    simulationZ.append(currentFields[2])
    simulationTotal.append(simTotal)
    
    realTime += 1
    realTimeVector.append(realTime)
    
    if(loop and (millis() - t0 > runTime)):
        break
    elif(not loop and simulationPosition >= len(dataFrame) - 1):
        break


sendPWMValues(0, 0, 0, 0, 0, 0, R4Ser)

fig, ax = plt.subplots(4)

ax[0].plot(realTimeVector,trueMagOutputX, color = "red", label = "Real")
ax[0].plot(realTimeVector, simulationX, color = "blue", label = "PySOL")

ax[1].plot(realTimeVector,trueMagOutputY, color = "red")
ax[1].plot(realTimeVector, simulationY,  color = "blue")

ax[2].plot(realTimeVector,trueMagOutputZ, color = "red")
ax[2].plot(realTimeVector, simulationZ, color = "blue")

ax[3].plot(realTimeVector, totalMagOutput, color = "red")
ax[3].plot(realTimeVector, simulationTotal, color = "blue")

plt.show()


