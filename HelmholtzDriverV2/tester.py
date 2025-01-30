# this code generates a simulation from PySol, iterates through it and sends the magnetic field values through PID to be emulated in the cage
# the resulting PWM values are associated with each magnetic field vector
# this creates a CSV file that can be read by the runSimulation program without a magnetometer 

import time
import matplotlib.pyplot as plt
import pandas as pd
import os

from PySol.sol_sim import generate_orbit_data
from Dependencies.R4UART import sendPWMValues, readPWMValues, initiateUART, readMagnetometerValues # UART code 
from Dependencies.PID import xPID, yPID, zPID # PID code
from Dependencies.calibrateValues import calibrate # magnetometer calibration code 
from Dependencies.extraneous import processStrings, calculateOffsets # import extraneous functions


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

