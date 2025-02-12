# reads magnetometer through USB connection
# data sent from the arduino nano is already processed correctly
# data is read into arduino_output.txt

# get serial port name from arduino IDE

import serial
import time

# tylers mac '/dev/cu.usbmodem2101'

serialPort = '/dev/cu.usbmodem101' # replace with your own usb port 

ser = serial.Serial(serialPort, 9600, timeout=1)

with open("arduino_output.txt", "w") as file:
    while True:
        line = ser.readline().decode('utf-8').strip()
        if line:
            print(line)

            file.write(line + "\n")  # Save the output to the text file
            file.flush()  # Ensure data is written to the file


 