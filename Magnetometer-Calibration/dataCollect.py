# reads magnetometer through USB connection
# data sent from the arduino nano is already processed correctly
# data is read into arduino_output.txt

# get serial port name from arduino IDE

import serial
import time

# Replace with your own USB port
serialPort = '/dev/cu.usbmodem101'  

ser = serial.Serial(serialPort, 9600, timeout=1)

start_time = time.time()  # Record the start time

with open("arduino_output6.txt", "w") as file:
    while time.time() - start_time < 60:  # Run for 10 seconds
        line = ser.readline().decode('utf-8').strip()
        if line:
            #print(line)
            file.write(line + "\n")  # Save the output to the text file
            file.flush()  # Ensure data is written to the file

print("Data collection complete. Exiting...")
ser.close()  # Close the serial connection
 