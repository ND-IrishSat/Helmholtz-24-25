# this code generates a simulation from PySol, iterates through it and sends the magnetic field values through PID to be emulated in the cage
# the resulting PWM values are associated with each magnetic field vector
# this creates a CSV file that can be read by the runSimulation program without a magnetometer 

import time
import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np
import serial

from queue import Empty

from PySol.sol_sim import generate_orbit_data
from Dependencies.R4UART import sendPWMValues, readPWMValues, initiateUART, refresh_buffers, readMagnetometerValues # UART code 
from Dependencies.PID import xPID, yPID, zPID # PID code
from Dependencies.calibrateValues import calibrate # magnetometer calibration code 
from Dependencies.extraneous import processStrings, calculateOffsets, millis # import extraneous functions

def isValidString(s: str) -> bool:
    return "." in s and not s.startswith(".")

########################################################################################## Settings

def gen_sim(file_name , nanoSer=None, msg_q=None):
    if msg_q is None:
        raise RuntimeError("msg_q required for magnetometer data")
    if nanoSer is None or not hasattr(nanoSer, "read_value"):
        raise RuntimeError("No magnetometer serial provided")
    
    R4Ser = serial.Serial('/dev/serial/by-id/usb-Arduino_UNO_WiFi_R4_CMSIS-DAP_F412FA74EB4C-if01', 9600)

    
    pidTries = 30 # number of tries the pid can take to get the desired value before it moves on to next value
    pidDelay = 100 # number of miliseconds between each pid iteration

    startPos = 0 # starting position in simulation
    runValues = 2950 # number of values to run through for PYSOL

    inputFileName = file_name
    outputFileName = "runZeroed.csv"
    file_name = "magneticFields.csv"

    # Creates path for output directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "PySol")
    os.makedirs(output_dir, exist_ok=True)
            
    # Full path to output file
    output_path = os.path.join(output_dir, "outputs")
    output_path = os.path.join(output_path, file_name)

    dataFrame = pd.read_csv(inputFileName)
    currentFields = [0, 0, 0]

    # .loc[row_label, column_label]
    # initialized currentFields with the first target values in dataFrame.loc[startPos, 'Bx']
    currentFields[0] = dataFrame.loc[startPos, 'Bx'] # Index: 0 Column Label : 'Bx'
    currentFields[1] = dataFrame.loc[startPos, 'By']
    currentFields[2] = dataFrame.loc[startPos, 'Bz']

    # Dataframe created to store the final outputs data: target fields
    df = pd.DataFrame(columns=["SIMX", "SIMY", "SIMZ", "PWM_X+", "PWM_X-", "PWM_Y+", "PWM_Y-", "PWM_Z+", "PWM_Z-"])

    ##########################################################################################
    
    # initial duty cycles, for manual mode set desired ones here
    Xp, Xn = 0.0, 0.0
    Yp, Yn = 0.0, 0.0
    Zp, Zn = 0.0, 0.0
    
    maxVal = 100 # max value of pwm signal (control output)

    # turn off cage at start
    sendPWMValues(0, 0, 0, 0, 0, 0, R4Ser)
    time.sleep(2)

    # real-time magnetometer readings
    trueMagOutputX = [0]
    trueMagOutputY = [0]
    trueMagOutputZ = [0]
    totalMagOutput = [0]
    # target magnetometer values from simulation
    simulationOutputX = [0]
    simulationOutputY = [0]
    simulationOutputZ = [0]
    simulationPos = startPos
    # magnetometer values from the moment PID calculations run
    pidMagOutputX = [0]
    pidMagOutputY = [0]
    pidMagOutputZ = [0]
    # history of calculate pid values
    pwmPosOutputX = [0]
    pwmNegOutputX = [0]
    pwmPosOutputY = [0]
    pwmNegOutputY = [0]
    pwmPosOutputZ = [0]
    pwmNegOutputZ = [0]
    # time counter for plotting (each loop iteration)
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
        ################################################################################################################## 
        # magnetometer reading                                                                                           #
        ################################################################################################################## 
        # refresh_buffers(nanoSer, R4Ser)

        # Drain all available magnetometer readings from queue
        got_new_reading = False
        while True:
            try:
                msg_type, payload = msg_q.get_nowait()
                if msg_type == "serial":
                    try:
                        magX = round(float(payload[0]), 2)
                        magY = round(float(payload[1]), 2)
                        magZ = round(float(payload[2]), 2)
                        got_new_reading = True
                    except (ValueError, IndexError, TypeError):
                        pass
            except Empty:
                break

        # Appends to history if we got a new reading
        if got_new_reading:
            trueMagOutputX.append(magX)
            trueMagOutputY.append(magY)
            trueMagOutputZ.append(magZ)
        else:
            # No new data, repeat last value
            trueMagOutputX.append(trueMagOutputX[len(trueMagOutputX) - 1])
            trueMagOutputY.append(trueMagOutputY[len(trueMagOutputY) - 1])
            trueMagOutputZ.append(trueMagOutputZ[len(trueMagOutputZ) - 1])

        ##################################################################################################################
        magRow = pd.DataFrame([{"X": magX, "Y": magY, "Z": magZ,}])
        totalMag = pow(((magX * magX) + (magY * magY) + (magZ * magZ)), 0.5)
        totalMagOutput.append(totalMag)
        
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

    # Creates output CSV file
    df.to_csv(outputFileName, index=True)
    sendPWMValues(0, 0, 0, 0, 0, 0, R4Ser)
    R4Ser.close()
