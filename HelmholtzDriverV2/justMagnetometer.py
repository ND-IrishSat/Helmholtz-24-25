
import time
import matplotlib.pyplot as plt
import pandas as pd
import os

from Dependencies.R4UART import sendPWMValues, readPWMValues, initiateUART, readMagnetometerValues # UART code 
from Dependencies.calibrateValues import calibrate # magnetometer calibration code 
from Dependencies.extraneous import processStrings, calculateOffsets, millis # import extraneous functions


#                x  y  z

timeVector = []
timeVar = 0

terminals = initiateUART(True, True)
time.sleep(1)
nanoSer = terminals[0]
R4Ser = terminals[1]

pwmFrequencyX = 250 # pwm frequency in Hz
pwmFrequencyY = 250 # pwm frequency in Hz
pwmFrequencyZ = 250 # pwm frequency in Hz

pwmUSecX = (1/pwmFrequencyX) * 1000000
pwmUSecY = (1/pwmFrequencyY) * 1000000
pwmUSecZ = (1/pwmFrequencyZ) * 1000000

sendPWMValues(0, 0, 0, 0, 0, 0, pwmUSecX, pwmUSecY, pwmUSecZ, R4Ser)
time.sleep(2)
Xp = 0
Xn = 0

Yp = 0
Yn = 0

Zp = 20
Zn = 0


magOutputX = []
magOutputY = []
magOutputZ = []

startTime = millis()

sendPWMValues(Yp, Yn, Xn, Xp, Zp, Zn, pwmUSecX, pwmUSecY, pwmUSecZ, R4Ser)
lock = False
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
    #print("X: " + str(magStrings[0]) + " Y: " + str(magStrings[1]) + " Z: " + str(magStrings[2]))
    
    timeVector.append(timeVar)
    timeVar += 1
    
    if(millis() - startTime > 1000 and not lock):
        sendPWMValues(0, 0, 0, 0, 0, 20, pwmUSecX, pwmUSecY, pwmUSecZ, R4Ser)
        lock = True
    if(millis() - startTime > 1500):
        break
    

fig, ax = plt.subplots(3)

ax[0].plot(timeVector,magOutputX, color = "red", label = "Real")

ax[1].plot(timeVector,magOutputY, color = "red")

ax[2].plot(timeVector,magOutputZ, color = "red")
plt.show()
