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
manual = False # when false, PID is enabled

# initial setpoints, for manual mode set desired ones here

ser = initiateUART()

async def main():
    
    # initial duty cycles, for manual mode set desired ones here
    Xp = 0.0
    Xn = 0.0

    Yp = 0.0
    Yn = 0.0

    Zp = 0.0
    Zn = 0.0
    
    setX = 40
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
                
                xTemp = results[0]
                yTemp = results[1]
                zTemp = results[2]
                
                if(xTemp < 0):
                    Xn = xTemp * -1
                    Xp = 0
                else:
                    Xp = xTemp
                    Xn = 0
                
                if(yTemp < 0):
                    Yn = yTemp * -1
                    Yp = 0
                else:
                    Yp = yTemp
                    Yn = 0
                    
                if(zTemp < 0):
                    Zn = zTemp * -1
                    Zp = 0
                else:
                    Zp = zTemp
                    Zn = 0
                    
                time.sleep(1)


            sendPWMValues(Yp, Yn, Xn, Xp, Zp, Zn, ser) # sends PWM to R4 (currently trying with 1 direction)

            if(debug):
                readPWMValues(ser)
            
        
asyncio.run(main())

