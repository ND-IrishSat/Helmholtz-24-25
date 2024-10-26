# Adafruit Mag code

import bleak
import asyncio
import struct

async def main():
    async with bleak.BleakClient("30:C6:F7:01:53:AA") as magnetometer:
        while True:
            x = await magnetometer.read_gatt_char("fd0f3499-4289-46b1-8ee5-c7781cb46b77")
            y = await magnetometer.read_gatt_char("0bea22dc-8371-4193-8e1a-1c8e46550f3f")
            z = await magnetometer.read_gatt_char("ab134932-3915-45bd-8366-8ee0ce7535f8")
            print("X: " + "{:.2f}".format(struct.unpack('f', x)[0]) + " Y: " + "{:.2f}".format(struct.unpack('f', y)[0]) + " Z: " + "{:.2f}".format(struct.unpack('f', z)[0]) )
        
asyncio.run(main())