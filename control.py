# Adafruit Mag code

import bleak
import asyncio
import struct
import serial
import time
from simple_pid import PID

async def main():
    # Init
    # PID Init
    pid = PID(5, 2, 2, setpoint=1)
    pid.output_limits = (0.00, 100.00)
    pid.setpoint = 75
    
    # Duty Cycles Init
    dutyX1 = 0.0
    dutyX2 = 0.0
    dutyY1 = 0.0
    dutyY2 = 0.0
    dutyZ1 = 0.0
    dutyZ2 = 0.0
    
    # Mag Field Setpoints Init
    setX = 70.0
    setY = 80.0
    setZ = 60.0

    # Body
    async with bleak.BleakClient("30:C6:F7:01:53:AA") as magnetometer:
        while True:
            # Gets magnetic fields
            magX = await magnetometer.read_gatt_char("fd0f3499-4289-46b1-8ee5-c7781cb46b77")
            magY = await magnetometer.read_gatt_char("0bea22dc-8371-4193-8e1a-1c8e46550f3f")
            magZ = await magnetometer.read_gatt_char("ab134932-3915-45bd-8366-8ee0ce7535f8")
            
            magX = struct.unpack('f', magX)[0]
            magY = struct.unpack('f', magY)[0]
            magZ = struct.unpack('f', magZ)[0]
            
            print("X: " + "{:.2f}".format(magX) + " Y: " + "{:.2f}".format(magY) + " Z: " + "{:.2f}".format(magZ) )
            
            # Run PID
            pid.setpoint = setX
            dutyX = pid(magX)
            pid.setpoint = setY
            dutyY = pid(magY)
            pid.setpoint = setZ
            dutyZ = pid(magZ)
            
            # Send new duty cycles
            if __name__ == '__main__':
                ser = serial.Serial('/dev/ttyACM0',9600,timeout=1)
                ser.reset_input_buffer()
            
            # x1 x2 y1 y2 z1 z2
            data = "0.00 " + str(dutyX) + " " + str(dutyY) + " 0.00 " + "0.00 " + str(dutyZ)
            ser.write(data.encode('utf-8'))
            print(ser.readline().decode('utf-8').rstrip())
            
            
        
asyncio.run(main())

