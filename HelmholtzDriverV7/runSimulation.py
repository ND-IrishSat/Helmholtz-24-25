from Dependencies.extraneous import millis

import time
import threading
import matplotlib.pyplot as plt

import pandas as pd

from math import sqrt
from cage_hardware import CageHardware

def run_sim(
        cage: CageHardware,
        stop_event: threading.Event,
        input_file: str, 
        runTime_In: int = 10000, 
        runSpeed_In: int = 1000, 
        startPos_In: int = 0
) -> None:
    # magnetic fields dataframe
    dataFrame = pd.read_csv(input_file)             

    ############################################################################ 
    # Run parameters
    ############################################################################
    loop = False        # if true, simulation will loop 1 value
    totalrunTime        = runTime_In # Time for total sim if timeLimit is true
    runSpeed            = runSpeed_In # time in miliseconds between each change in field, so 1000 is real time
    simulationPosition  = startPos_In

    ############################################################################

    if simulationPosition >= len(dataFrame):
        print(f"Error: Start position {simulationPosition} is larger DF length {len(dataFrame)}")
        return

    # turn off the cage at start
    cage.set_pwm(0,0,0,0,0,0)
    time.sleep(1)
    
    # Send initial step before loop begins
    currentPWMVals = [
        dataFrame.loc[simulationPosition, 'PWM_X+'],  
        dataFrame.loc[simulationPosition, 'PWM_X-'],  
        dataFrame.loc[simulationPosition, 'PWM_Y+'],  
        dataFrame.loc[simulationPosition, 'PWM_Y-'],  
        dataFrame.loc[simulationPosition, 'PWM_Z+'],  
        dataFrame.loc[simulationPosition, 'PWM_Z-'],  
    ]
    #  xp, xn, yp, yn, zp, zn
    cage.set_pwm(
        currentPWMVals[0], currentPWMVals[1], # xp, xn
        currentPWMVals[2], currentPWMVals[3], # xp, yn
        currentPWMVals[4], currentPWMVals[5]  # zp, zn
    )

    simulated_X = float(dataFrame.loc[simulationPosition, 'SIMX'])
    simulated_Y = float(dataFrame.loc[simulationPosition, 'SIMY'])
    simulated_Z = float(dataFrame.loc[simulationPosition, 'SIMZ'])
    simulated_tot = sqrt((simulated_X*simulated_X) + (simulated_Y*simulated_Y) + (simulated_Z*simulated_Z))
    cage.send_sim_value(simulated_tot)
    time.sleep(1)

    t0 = millis()
    pwmTime = t0

    try:
        while not stop_event.is_set():
            if (millis() - pwmTime) >= runSpeed:
                pwmTime = millis()
                simulationPosition += 1

                if simulationPosition >= len(dataFrame):
                    break

                currentPWMVals = [
                    dataFrame.loc[simulationPosition, 'PWM_X+'],  
                    dataFrame.loc[simulationPosition, 'PWM_X-'],  
                    dataFrame.loc[simulationPosition, 'PWM_Y+'],  
                    dataFrame.loc[simulationPosition, 'PWM_Y-'],  
                    dataFrame.loc[simulationPosition, 'PWM_Z+'],  
                    dataFrame.loc[simulationPosition, 'PWM_Z-'],  
                ]
                cage.set_pwm(
                    currentPWMVals[0], currentPWMVals[1], # xp, xn
                    currentPWMVals[2], currentPWMVals[3], # xp, yn
                    currentPWMVals[4], currentPWMVals[5]  # zp, zn
                )

                simulated_X = float(dataFrame.loc[simulationPosition, 'SIMX'])
                simulated_Y = float(dataFrame.loc[simulationPosition, 'SIMY'])
                simulated_Z = float(dataFrame.loc[simulationPosition, 'SIMZ'])
                simulated_tot = sqrt((simulated_X*simulated_X) + (simulated_Y*simulated_Y) + (simulated_Z*simulated_Z))
                cage.send_sim_value(simulated_tot)

            if (millis() - t0) > totalrunTime:
                break

            time.sleep(0.001)

    finally:
        print("RUN SIM EXIT") 
        cage.set_pwm(0, 0, 0, 0, 0, 0)
        cage.send_sim_value(0.0)
        