from Dependencies.R4UART import sendPWMValues, initiateUART # UART code 
from Dependencies.extraneous import millis

import time
import matplotlib.pyplot as plt

import pandas as pd

def isValidString(s: str) -> bool:
    return "." in s and not s.startswith(".")

def run_sim(file_name, runTime_In, runSpeed_In, startPos_In):
    print("Started.\n")
    print("Run Time (s): ", runTime_In/1000)
    print("Run Speed (ms/): ", runSpeed_In)
    print("Start Position: ", startPos_In)
    #dataFrame = pd.read_csv("runPySolReal.csv") # magnetic fields dataframe
    dataFrame = pd.read_csv(file_name) # magnetic fields dataframe

    ################################################################################ Run parameters

    loop = False # if true, simulation will loop 1 value

    timeLimit = True
    totalrunTime = runTime_In # Time for total sim if timeLimit is true

    startPosition = startPos_In # index of the dataframe to start in
    runSpeed = runSpeed_In # time in miliseconds between each change in field, so 1000 is real time

    ################################################################################

    #                x  y  z
    currentFields = [0, 0, 0]

    #                +x -x +y -y +z -z
    currentPWMVals = [0, 0, 0, 0, 0, 0]

    realTimeVector = []
    timeVar = 0

    terminals = initiateUART(True, True)
    time.sleep(1)
    #nanoSer = terminals[0]
    R4Ser = terminals[1]

    sendPWMValues(0, 0, 0, 0, 0, 0, R4Ser)
    time.sleep(2)

#     trueMagOutputX = []
#     trueMagOutputY = []
#     trueMagOutputZ = []
#     totalMagOutput = []

    simulationX = []
    simulationY = []
    simulationZ = []
    simulationTotal = []
    simulationPosition = 0 
    
    if simulationPosition >= len(dataFrame):
        print(f"Error: Start position {simulationPosition} is larger DF length {len(dataFrame)}")
        return
    
    currentPWMVals[0] = dataFrame.loc[simulationPosition, 'PWM_X+']
    currentPWMVals[1] = dataFrame.loc[simulationPosition, 'PWM_X-']
    currentPWMVals[2] = dataFrame.loc[simulationPosition, 'PWM_Y+']
    currentPWMVals[3] = dataFrame.loc[simulationPosition, 'PWM_Y-']
    currentPWMVals[4] = dataFrame.loc[simulationPosition, 'PWM_Z+']
    currentPWMVals[5] = dataFrame.loc[simulationPosition, 'PWM_Z-']

    sendPWMValues(currentPWMVals[2], currentPWMVals[3], currentPWMVals[1], currentPWMVals[0], currentPWMVals[4], currentPWMVals[5], R4Ser)
    time.sleep(1)

    realTimeVector = []
    realTime = 0

    t0 = millis()
    pwmTime = t0

    while(True):
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
            
#         simTotal = pow(((currentFields[0] * currentFields[0]) + (currentFields[1] * currentFields[1]) + (currentFields[2] * currentFields[2])), 0.5)
#         simulationX.append(currentFields[0])
#         simulationY.append(currentFields[1])
#         simulationZ.append(currentFields[2])
#         simulationTotal.append(simTotal)
        
        realTime += 1
        realTimeVector.append(realTime)
        
        if((millis() - t0) > totalrunTime):
            print("RUN SIM EXIT")
            sendPWMValues(0,0,0,0,0,0,R4Ser)
            break   
