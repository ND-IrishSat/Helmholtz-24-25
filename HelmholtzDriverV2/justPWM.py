
import time
import matplotlib.pyplot as plt
import pandas as pd
import os

from Dependencies.R4UART import sendPWMValues, readPWMValues, initiateUART, readMagnetometerValues # UART code 
from Dependencies.calibrateValues import calibrate # magnetometer calibration code 
from Dependencies.extraneous import processStrings, calculateOffsets, millis # import extraneous functions

terminals = initiateUART(False, True)
time.sleep(1)
nanoSer = terminals[0]
R4Ser = terminals[1]

sendPWMValues(0, 0, 0, 0, 0, 0, R4Ser)
time.sleep(2)



Xp = 0
Xn = 0

Yp = 0
Yn = 0

Zp = 100
Zn = 0


while(True):
    
    R4Ser.reset_input_buffer()
    R4Ser.reset_output_buffer()
    print("Running")
    sendPWMValues(Yp, Yn, Xn, Xp, Zp, Zn, R4Ser)
    time.sleep(1)
    
    