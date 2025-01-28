# this code generates a simulation from PySol, iterates through it and sends the magnetic field values through PID to be emulated in the cage
# the resulting PWM values are associated with each magnetic field vector
# this creates a CSV file that can be read by the runSimulation program without a magnetometer 

import time
import math
import matplotlib.pyplot as plt
import pandas as pd
import os

from PySol.sol_sim import generate_orbit_data
from HelmholtzDriverV2.Dependencies.R4UART import sendPWMValues, readPWMValues, initiateUART, readMagnetometerValues # UART code 
from HelmholtzDriverV2.Dependencies.PID import xPID, yPID, zPID # PID code
from HelmholtzDriverV2.Dependencies.calibrateValues import calibrate # magnetometer calibration code 
from HelmholtzDriverV2.Dependencies.extraneous import processStrings, calculateOffsets # import extraneous functions

########################################################################################## Settings

runTime = 10 # in seconds
runSpeed = 1 # percentage of how fast simulation should be processed, 1 is 100% real time, 0.1 is 10x faster

########################################################################################## pysol initialization

oe = [121, 6_800, 0.0000922, 51, -10, 80]
total_time = 3 # in hours
timestep = 1.0 # time step in seconds
file_name = "magneticFields.csv"
store_data = True
generate_GPS = False
generate_RAM = False

generate_orbit_data(oe, total_time, timestep, file_name, store_data, generate_GPS, generate_RAM)

script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, "PySol")
os.makedirs(output_dir, exist_ok=True)
        
# Full path to output file
output_path = os.path.join(output_dir, "outputs")
output_path = os.path.join(output_path, file_name)

dataFrame = pd.read_csv(output_path) # magnetic fields dataframe

currentFields = []

currentFields[0] = dataFrame.loc[0, 'Bx']
currentFields[1] = dataFrame.loc[0, 'By']
currentFields[2] = dataFrame.loc[0, 'Bz']

##########################################################################################

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

startTime = time.time(); # get start time
timeVec = [0]
i = 0
while (time.time()-startTime <= runTime):
    timeVec.append(time.time() - startTime)               

    ################################################################################################################## magnetometer reading
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


    [Xp, Xn] = xPID(xRamp, calMagX, magOutputX[i-1], pwmPosOutputX[i-1], pwmNegOutputX[i-1], maxVal, timeVec[i]-timeVec[i-1])
    [Yp, Yn] = yPID(yRamp, calMagY, magOutputY[i-1], pwmPosOutputY[i-1], pwmNegOutputY[i-1], maxVal, timeVec[i]-timeVec[i-1])
    [Zp, Zn] = zPID(zRamp, calMagZ, magOutputZ[i-1], pwmPosOutputZ[i-1], pwmNegOutputZ[i-1], maxVal, timeVec[i]-timeVec[i-1]) 
    

    pwmPosOutputX.append(Xp)
    pwmNegOutputX.append(Xn)
    
    pwmPosOutputY.append(Yp)
    pwmNegOutputY.append(Yn)
    
    pwmPosOutputZ.append(Zp)
    pwmNegOutputZ.append(Zn)


    time.sleep(1 * runSpeed)

    sendPWMValues(Yp, Yn, Xn, Xp, Zp, Zn, R4Ser)

    i += 1
        
fig, ax = plt.subplots(3)
ax[0].plot(timeVec, magOutputX)
ax[0].set_ylim(-75, 75)
ax[1].plot(timeVec, magOutputY)
ax[1].set_ylim(-75, 75)
ax[2].plot(timeVec, magOutputZ)
ax[2].set_ylim(-50, 50)
plt.show()


