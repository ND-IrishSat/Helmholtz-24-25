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

debug = True # enables extra print statements (slow)
manual = True # when false, PID is enabled

# initial setpoints, for manual mode set desired ones here
setX = 0
setY = 0
setZ = 0

ser = initiateUART()

async def main():
    
    # initial duty cycles, for manual mode set desired ones here
    x1 = 0.0
    x2 = 0.0
    y1 = 0.0
    y2 = 0.0
    z1 = 0.0
    z2 = 0.0

    async with bleak.BleakClient("30:C6:F7:01:53:AA") as magnetometer:

        while True:
            # Gets magnetic fields
            magX = await magnetometer.read_gatt_char("fd0f3499-4289-46b1-8ee5-c7781cb46b77")
            magY = await magnetometer.read_gatt_char("0bea22dc-8371-4193-8e1a-1c8e46550f3f")
            magZ = await magnetometer.read_gatt_char("ab134932-3915-45bd-8366-8ee0ce7535f8")
            
            magX = struct.unpack('f', magX)[0]
            magY = struct.unpack('f', magY)[0]
            magZ = struct.unpack('f', magZ)[0]

            calibratedValues = calibrate(magX, magY, magZ) # apply calibration

            magX = calibratedValues[0]
            magY = calibratedValues[1]
            magZ = calibratedValues[2]
            
            print("X: " + "{:.2f}".format(magX) + " Y: " + "{:.2f}".format(magY) + " Z: " + "{:.2f}".format(magZ))
        
            if not(manual):
                PIDsetpoints(setX, setY, setZ)
                results = computePID(magX, magY, magZ)

                # implement negative calculations here later

                x1 = results[0]
                y1 = results[1]
                z1 = results[2]

            sendPWMValues(x1, x2, y1, y2, z1, z2, ser) # sends PWM to R4 (currently trying with 1 direction)

            if(debug):
                readPWMValues(ser)
            
        
asyncio.run(main())

