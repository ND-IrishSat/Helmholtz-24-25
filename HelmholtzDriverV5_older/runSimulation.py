from Dependencies.R4UART import sendPWMValues, initiateUART # UART code 
from Dependencies.extraneous import millis

import time
import matplotlib.pyplot as plt

import pandas as pd

def isValidString(s: str) -> bool:
    return "." in s and not s.startswith(".")

def run_sim(file_name, runTime_In, runSpeed_In, startPos_In):
    """
    Run the simulation with proper error handling.
    This function is called from a thread, so all exceptions must be caught.
    """
    R4Ser = None  # Initialize to None so exception handlers can check if it exists
    try:
        print("Started.\n")
        print("Run Time (s): ", runTime_In/1000)
        print("Run Speed (ms/): ", runSpeed_In)
        print("Start Position: ", startPos_In)
        #dataFrame = pd.read_csv("runPySolReal.csv") # magnetic fields dataframe
        dataFrame = pd.read_csv(file_name) # magnetic fields dataframe

        ################################################################################ Run parameters

        loop = False # if true, simulation will loop 1 value
        runTime = 5000 # # if loop is true, the simulation will only loop for this number of miliseconds

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

        simulationPosition = startPosition # 0 -> startPosition to use the starting position parameter
        
        # Validate start position is within DataFrame bounds
        if simulationPosition < 0:
            print(f"Error: Start position {simulationPosition} is negative")
            return
        if simulationPosition >= len(dataFrame):
            print(f"Error: Start position {simulationPosition} is beyond DataFrame length {len(dataFrame)} (valid range: 0-{len(dataFrame)-1})")
            return
        
        # Use iloc with proper syntax: iloc[row][column_name] or loc[row, column_name]
        # iloc only accepts integer positions, so we use loc which works with integer index and column names
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
            #print("Running...\n")

            ##################################################################################################### magnetometer reading 
    #         nanoSer.reset_input_buffer()
    #         nanoSer.reset_output_buffer()
    #         
    #         R4Ser.reset_input_buffer()
    #         R4Ser.reset_output_buffer()
    #         magnetometerOutput = nanoSer.readline().decode('utf-8').strip().split()
    #         if magnetometerOutput:
    #             if ((len(magnetometerOutput) == 3) and isValidString(magnetometerOutput[0])):
    #                 magX = round(float(magnetometerOutput[0]), 2)
    #                 magY = round(float(magnetometerOutput[1]), 2)
    #                 magZ = round(float(magnetometerOutput[2]), 2)
    #                 trueMagOutputX.append(magX)
    #                 trueMagOutputY.append(magY)
    #                 trueMagOutputZ.append(magZ)
    #             else:
    #                 trueMagOutputX.append(trueMagOutputX[len(trueMagOutputX) - 1])
    #                 trueMagOutputY.append(trueMagOutputY[len(trueMagOutputY) - 1])
    #                 trueMagOutputZ.append(trueMagOutputZ[len(trueMagOutputZ) - 1])
    # 
    #                 magX = trueMagOutputX[len(trueMagOutputX) - 1]
    #                 magY = trueMagOutputY[len(trueMagOutputY) - 1]
    #                 magZ = trueMagOutputZ[len(trueMagOutputZ) - 1]
    # 
    #                
            #####################################################################################################
    #         totalMag = pow(((magX * magX) + (magY * magY) + (magZ * magZ)), 0.5)
    #         totalMagOutput.append(totalMag)

            if(millis() - pwmTime >= runSpeed):
                pwmTime = millis()

                simulationPosition += 1

                if(loop):
                    simulationPosition = 0
                
                # Check bounds before accessing DataFrame to prevent IndexError
                if simulationPosition >= len(dataFrame):
                    print(f"Warning: Simulation position {simulationPosition} exceeds DataFrame length {len(dataFrame)}. Stopping.")
                    sendPWMValues(0,0,0,0,0,0,R4Ser)
                    break
                
                # Use loc for integer index with column names (works correctly)
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
    # 
    #         simulationX.append(currentFields[0])
    #         simulationY.append(currentFields[1])
    #         simulationZ.append(currentFields[2])
    #         simulationTotal.append(simTotal)
            
            realTime += 1
            realTimeVector.append(realTime)
            
            if(loop and (millis() - t0 > runTime)):
                print("Broke_1")
                sendPWMValues(0,0,0,0,0,0,R4Ser)
                break
            elif(timeLimit and (millis() - t0 > totalrunTime)):
                print("Broke_2")
                sendPWMValues(0,0,0,0,0,0,R4Ser)
                break   
    #         elif(not loop and simulationPosition >= len(dataFrame) - 1):
    #             print("Broke_3")
    #             sendPWMValues(0,0,0,0,0,0,R4Ser)
    #             break

    except KeyboardInterrupt:
        print("Simulation interrupted by user")
        if R4Ser is not None:
            try:
                sendPWMValues(0,0,0,0,0,0,R4Ser)
            except Exception as e:
                print(f"Warning: Could not zero PWM values on interrupt: {e}")
    except Exception as e:
        print(f"ERROR in run_sim: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        if R4Ser is not None:
            try:
                sendPWMValues(0,0,0,0,0,0,R4Ser)
            except Exception as cleanup_error:
                print(f"Warning: Could not zero PWM values on error: {cleanup_error}")
    finally:
        # Cleanup: ensure PWM values are zeroed if R4Ser was initialized
        if R4Ser is not None:
            try:
                sendPWMValues(0,0,0,0,0,0,R4Ser)
            except:
                pass  # Silently fail in finally block
        print("Simulation ended.")
    # sendPWMValues(0, 0, 0, 0, 0, 0, R4Ser)
    # 
    # fig, ax = plt.subplots(4)
    # 
    # ax[0].plot(realTimeVector,trueMagOutputX, color = "red", label = "Real")
    # ax[0].plot(realTimeVector, simulationX, color = "blue", label = "PySOL")
    # 
    # ax[1].plot(realTimeVector,trueMagOutputY, color = "red")
    # ax[1].plot(realTimeVector, simulationY,  color = "blue")
    # 
    # ax[2].plot(realTimeVector,trueMagOutputZ, color = "red")
    # ax[2].plot(realTimeVector, simulationZ, color = "blue")
    # 
    # ax[3].plot(realTimeVector, totalMagOutput, color = "red")
    # ax[3].plot(realTimeVector, simulationTotal, color = "blue")
    # 
    # plt.show()


