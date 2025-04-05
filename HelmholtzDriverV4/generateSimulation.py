# this code generates a simulation from PySol, iterates through it and sends the magnetic field values through PID to be emulated in the cage
# the resulting PWM values are associated with each magnetic field vector
# this creates a CSV file that can be read by the runSimulation program without a magnetometer 

import time
import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np

from PySol.sol_sim import generate_orbit_data
from Dependencies.R4UART import sendPWMValues, readPWMValues, initiateUART, readMagnetometerValues # UART code 
from Dependencies.PID import xPID, yPID, zPID # PID code
from Dependencies.calibrateValues import calibrate # magnetometer calibration code 
from Dependencies.extraneous import processStrings, calculateOffsets, millis # import extraneous functions

########################################################################################## Settings

pidTries = 20 # number of tries the pid can take to get the desired value before it moves on to next value
pidDelay = 100 # number of miliseconds between each pid iteration

startPos = 0 # starting position in simulation
runValues = 5900 # number of values to run through for PYSOL

usingPYSOL = False

inputFileName = "zeroed.csv"
outputFileName = "runPysol.csv"
fftOutput = "magFieldsOut.csv"

########################################################################################## pysol initialization

oe = [121, 6_800, 0.0000922, 51, -10, 80]
total_time = 3 # in hours
timestep = 1.0 # time step in seconds
file_name = "magneticFields.csv"
store_data = True
generate_GPS = False
generate_RAM = False

#generate_orbit_data(oe, total_time, timestep, file_name, store_data, generate_GPS, generate_RAM)

script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, "PySol")
os.makedirs(output_dir, exist_ok=True)
        
# Full path to output file
output_path = os.path.join(output_dir, "outputs")
output_path = os.path.join(output_path, file_name)

dataFrame = 0

if(usingPYSOL):
    dataFrame = pd.read_csv(output_path) # magnetic fields dataframe
else:
    dataFrame = pd.read_csv(inputFileName)

currentFields = [0, 0, 0]

currentFields[0] = dataFrame.loc[startPos, 'Bx']
currentFields[1] = dataFrame.loc[startPos, 'By']
currentFields[2] = dataFrame.loc[startPos, 'Bz']

df = pd.DataFrame(columns=["SIMX", "SIMY", "SIMZ", "PWM_X+", "PWM_X-", "PWM_Y+", "PWM_Y-", "PWM_Z+", "PWM_Z-"])
#fftFrame = pd.DataFrame(columns=["X", "Y", "Z"])


##########################################################################################

terminals = initiateUART(True, True)
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
    

maxVal = 100 # max value of pwm signal (control output)

# turn off cage at start
sendPWMValues(0, 0, 0, 0, 0, 0, R4Ser)
time.sleep(2)

def isValidString(s: str) -> bool:
    return "." in s and not s.startswith(".")

trueMagOutputX = [0]
trueMagOutputY = [0]
trueMagOutputZ = [0]
totalMagOutput = [0]

simulationOutputX = [0]
simulationOutputY = [0]
simulationOutputZ = [0]
simulationPos = startPos

pidMagOutputX = [0]
pidMagOutputY = [0]
pidMagOutputZ = [0]

pwmPosOutputX = [0]
pwmNegOutputX = [0]
pwmPosOutputY = [0]
pwmNegOutputY = [0]
pwmPosOutputZ = [0]
pwmNegOutputZ = [0]

realTimeVector = [0]
realTime = 0 # increments with each loop, used for graphing

t0 = millis() # start time of the program

pidTime = t0
pidTriesCount = 0
pidPosition = 0
pidTimeVector = [0]

err_current = 0
err_best = 10000
bestIndex = 0

runValuesCount = 0

magX = 0
magY = 0
magZ = 0

while (True):

    ################################################################################################################## magnetometer reading
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
    ##################################################################################################################
    magRow = pd.DataFrame([{"X": magX, "Y": magY, "Z": magZ,}])
    totalMag = pow(((magX * magX) + (magY * magY) + (magZ * magZ)), 0.5)
    totalMagOutput.append(totalMag)
    #fftFrame = pd.concat([fftFrame, magRow], ignore_index=True)
    
    
    simulationOutputX.append(currentFields[0])
    simulationOutputY.append(currentFields[1])
    simulationOutputZ.append(currentFields[2])
    
    if(millis() - pidTime > pidDelay):

        pidMagOutputX.append(magX)
        pidMagOutputY.append(magY)
        pidMagOutputZ.append(magZ)

        pidPosition += 1
        pidTimeVector.append(millis())

        pidTime = millis()
        
        [Xp, Xn] = xPID(currentFields[0], magX, pidMagOutputX[pidPosition-1], pwmPosOutputX[pidPosition-1], pwmNegOutputX[pidPosition-1], maxVal, pidTimeVector[pidPosition]-pidTimeVector[pidPosition-1])
        [Yp, Yn] = yPID(currentFields[1], magY, pidMagOutputY[pidPosition-1], pwmPosOutputY[pidPosition-1], pwmNegOutputY[pidPosition-1], maxVal, pidTimeVector[pidPosition]-pidTimeVector[pidPosition-1])
        [Zp, Zn] = zPID(currentFields[2], magZ, pidMagOutputZ[pidPosition-1], pwmPosOutputZ[pidPosition-1], pwmNegOutputZ[pidPosition-1], maxVal, pidTimeVector[pidPosition]-pidTimeVector[pidPosition-1])
     
        sendPWMValues(Yp, Yn, Xn, Xp, Zp, Zn, R4Ser)

        pwmPosOutputX.append(Xp)
        pwmNegOutputX.append(Xn)
        
        pwmPosOutputY.append(Yp)
        pwmNegOutputY.append(Yn)
        
        pwmPosOutputZ.append(Zp)
        pwmNegOutputZ.append(Zn)

        pidTriesCount += 1

        err_current = (abs(currentFields[0] - magX)) + (abs(currentFields[1] - magY)) + (abs(currentFields[2] - magZ))
        if (err_current < err_best):
            err_best = err_current
            bestIndex = pidPosition

# 
    realTime += 1
    realTimeVector.append(realTime)
    
    if(len(realTimeVector) != len(trueMagOutputX) or len(realTimeVector) != len(trueMagOutputY) or len(realTimeVector) != len(trueMagOutputZ)):
        trueMagOutputX.append(trueMagOutputX[len(trueMagOutputX) - 1])
        trueMagOutputY.append(trueMagOutputY[len(trueMagOutputY) - 1])
        trueMagOutputZ.append(trueMagOutputZ[len(trueMagOutputZ) - 1])

    if(pidTriesCount == pidTries):
        pidTriesCount = 0
        simulationPos += 1
        runValuesCount += 1
        err_best = 10000

        row = pd.DataFrame([{"SIMX": currentFields[0], "SIMY": currentFields[1], "SIMZ": currentFields[2], 
                             "PWM_X+": pwmPosOutputX[bestIndex], "PWM_X-": pwmNegOutputX[bestIndex],
                             "PWM_Y+": pwmPosOutputY[bestIndex], "PWM_Y-": pwmNegOutputY[bestIndex],
                             "PWM_Z+": pwmPosOutputZ[bestIndex], "PWM_Z-": pwmNegOutputZ[bestIndex],}])
        
        
        df = pd.concat([df, row], ignore_index=True)        
    
        if(simulationPos >= len(dataFrame) or runValuesCount >= runValues):
            break
        else:
            currentFields[0] = dataFrame.loc[simulationPos, 'Bx']
            currentFields[1] = dataFrame.loc[simulationPos, 'By']
            currentFields[2] = dataFrame.loc[simulationPos, 'Bz']


    

array = np.array(realTimeVector)
result = array / 310

print(realTimeVector[(len(realTimeVector) - 1)])
# Creates output CSV file
df.to_csv(outputFileName, index=True)
#fftFrame.to_csv(fftOutput, index=True)
sendPWMValues(0, 0, 0, 0, 0, 0, R4Ser)
# Plots data

plt.ylim(0,55)
plt.plot(result,totalMagOutput, color = "red")
# fig, ax = plt.subplots(4)

# ax[0].plot(result,trueMagOutputX, color = "blue", label = "Real")
# #ax[0].plot(realTimeVector, simulationOutputX, color = "black", label = "PySOL")
# 
# ax[1].plot(result,trueMagOutputY, color = "blue")
# #ax[1].plot(realTimeVector, simulationOutputY,  color = "black")
# 
# ax[2].plot(result,trueMagOutputZ, color = "blue")
# ax[1].set_ylim(0, 35)
# ax[1].plot(result,totalMagOutput, color = "red")

#ax[2].plot(realTimeVector, simulationOutputZ, color = "black")

plt.show()