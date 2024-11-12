# Adafruit Mag code

import bleak
import asyncio
import struct
import time
import numpy
import serial

from R4UART import sendPWMValues, readPWMValues, initiateUART # UART code 
from PID import PIDsetpoints, computePID # PID code
from calibrateValues import calibrate # magnetometer calibration code 

debug = False # enables extra print statements (slow)
manual = True # when false, PID is enabled

# initial setpoints, for manual mode set desired ones here

ser = initiateUART()

async def main():
    
    # initial duty cycles, for manual mode set desired ones here
    Xp = 0.0 
    Xn = 0.0

    Yp = 0.0
    Yn = 0.0

    Zp = 0.0
    Zn = 5
    
    setX = 0
    setY = 0
    setZ = 0

    async with bleak.BleakClient("30:C6:F7:01:53:AA") as magnetometer:

        while True:
            # Gets magnetic fields
            magX = await magnetometer.read_gatt_char("fd0f3499-4289-46b1-8ee5-c7781cb46b77")
            magY = await magnetometer.read_gatt_char("0bea22dc-8371-4193-8e1a-1c8e46550f3f")
            magZ = await magnetometer.read_gatt_char("ab134932-3915-45bd-8366-8ee0ce7535f8")
            
            magX = struct.unpack('f', magX)[0]
            magY = struct.unpack('f', magY)[0]
            magZ = struct.unpack('f', magZ)[0]
            
            #print("X: " + "{:.2f}".format(magX) + " Y: " + "{:.2f}".format(magY) + " Z: " + "{:.2f}".format(magZ))

            calibratedValues = calibrate(magX, magY, magZ) # apply calibration

            magX = calibratedValues[0]
            magY = calibratedValues[1]
            magZ = calibratedValues[2]
            
            print("X: " + "{:.2f}".format(magX) + " Y: " + "{:.2f}".format(magY) + " Z: " + "{:.2f}".format(magZ))
            print()
            
            if not(manual):
                PIDsetpoints(setX, setY, setZ)
                results = computePID(magX, magY, magZ)

                Xp = results[0]
                Xn = results[1] * -1

                Yp = results[2]
                Yn = results[3] * -1

                Zp = results[4]
                Zn = results[5] * -1

            sendPWMValues(Xp, Xn, Yp, Yn, Zp, Zn, ser) # sends PWM to R4 (currently trying with 1 direction)

            if(debug):
                readPWMValues(ser)
            
        
asyncio.run(main())

