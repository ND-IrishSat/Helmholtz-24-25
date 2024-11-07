# Adafruit Mag code

import bleak
import asyncio
import struct

async def main():
    async with bleak.BleakClient("30:C6:F7:01:53:AA") as magnetometer:
        with open("arduino_output.txt", "w") as file:
            while True:
                x = await magnetometer.read_gatt_char("fd0f3499-4289-46b1-8ee5-c7781cb46b77")
                y = await magnetometer.read_gatt_char("0bea22dc-8371-4193-8e1a-1c8e46550f3f")
                z = await magnetometer.read_gatt_char("ab134932-3915-45bd-8366-8ee0ce7535f8")
                
                x = struct.unpack('f', x)[0]
                y = struct.unpack('f', y)[0]
                z = struct.unpack('f', z)[0]
                
                print("X: " + "{:.2f}".format(x) + " Y: " + "{:.2f}".format(y) + " Z: " + "{:.2f}".format(z) )
                arduino_output = "{:.2f}".format(x) + " " + "{:.2f}".format(y) + " " + "{:.2f}".format(z)
                # print(arduino_output)  # Testing print statement to display the output
                file.write(arduino_output + "\n")  # Save the output to the text file
                file.flush()  # Ensure data is written to the file
        
asyncio.run(main())
