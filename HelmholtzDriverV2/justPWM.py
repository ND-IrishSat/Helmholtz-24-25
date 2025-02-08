
import time
import matplotlib.pyplot as plt
import pandas as pd
import os

from Dependencies.R4UART import sendPWMValues, readPWMValues, initiateUART, readMagnetometerValues # UART code 
from Dependencies.calibrateValues import calibrate # magnetometer calibration code 
from Dependencies.extraneous import processStrings, calculateOffsets, millis # import extraneous functions

terminals = initiateUART()
time.sleep(1)
nanoSer = terminals[0]
R4Ser = terminals[1]

sendPWMValues(0, 0, 0, 0, 0, 0, R4Ser)
time.sleep(2)



Xp = 100
Xn = 0

Yp = 0
Yn = 0

Zp = 0
Zn = 0


while(True):

    print("Running")
    sendPWMValues(Yp, Yn, Xn, Xp, Zp, Zn, R4Ser)
    time.sleep(100)