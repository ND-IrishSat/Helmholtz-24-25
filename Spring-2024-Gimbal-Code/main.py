# Gimbal Encoder BLE Receiver
# Authored by Will Stotz for IrishSat, 2024

# TODO - work out direction of rotation and negative angle change

import bleak
import asyncio
import numpy as np
from os import system

async def main():
    async with bleak.BleakClient("B5FB88F9-4C72-19A4-D74A-48ADDDEFE512") as client1:    #must be changed to MAC address to run on Windows
        async with bleak.BleakClient("F54BF5C0-472E-4C4D-1B73-9B9E0B4DB925") as client2:
            encoder1 = await client1.read_gatt_char("fd0f3499-4289-46b1-8ee5-c7781cb46b77")
            encoder2 = await client1.read_gatt_char("11a6ddf2-12e4-4804-a75e-6f0185a59326")
            encoder3 = await client2.read_gatt_char("fd0f3499-4289-46b1-8ee5-c7781cb46b77")
            encoder4 = await client2.read_gatt_char("11a6ddf2-12e4-4804-a75e-6f0185a59326")

            encoder1pings = encoder2pings = encoder3pings = encoder4pings = 0

            cooldown = False

            xDirection = yDirection = 0

            while True:
                if not cooldown:
                    newEncoder1 = await client1.read_gatt_char("fd0f3499-4289-46b1-8ee5-c7781cb46b77")
                    newEncoder2 = await client1.read_gatt_char("11a6ddf2-12e4-4804-a75e-6f0185a59326")
                    newEncoder3 = await client2.read_gatt_char("fd0f3499-4289-46b1-8ee5-c7781cb46b77")
                    newEncoder4 = await client2.read_gatt_char("11a6ddf2-12e4-4804-a75e-6f0185a59326")

                    if not np.array_equal(encoder1, newEncoder1):
                        encoder1pings += 1
                        xDirection = -1
                        cooldown = True
                    if not np.array_equal(encoder2, newEncoder2):
                        encoder2pings += 1
                        xDirection = 1
                        cooldown = True
                    if not np.array_equal(encoder3, newEncoder3):
                        encoder3pings += 1
                        yDirection = -1
                        cooldown = True
                    if not np.array_equal(encoder4, newEncoder4):
                        encoder4pings += 1
                        yDirection = 1
                        cooldown = True

                    encoder1 = newEncoder1
                    encoder2 = newEncoder2
                    encoder3 = newEncoder3
                    encoder4 = newEncoder4

                    system("clear")
                    print("Encoder 1 Pings: "+str(encoder1pings)+
                        "\nEncoder 1 Degrees: "+str(encoder1pings/2*13.0)+
                        "\nEncoder 2 Pings: "+str(encoder2pings)+
                        "\nEncoder 2 Degrees: "+str(encoder2pings/2*13.0)+
                        "\nEncoder 3 Pings: "+str(encoder3pings)+
                        "\nEncoder 3 Degrees: "+str(encoder3pings/2*13.0)+
                        "\nEncoder 4 Pings: "+str(encoder4pings)+
                        "\nEncoder 4 Degrees: "+str(encoder4pings/2*13.0)+
                        "\nX Direction: "+str(xDirection)+
                        "\nY Direction: "+str(yDirection)+"\n")
                else:
                    cooldown = False

asyncio.run(main())
