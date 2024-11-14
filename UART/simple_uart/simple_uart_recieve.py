import serial
import time

# Replace '/dev/ttyUSB0' with the actual port for your Arduino on the Raspberry Pi
arduino_port = '/dev/cu.usbmodem101'
baud_rate = 9600

# Initialize the serial connection
ser = serial.Serial(arduino_port, baud_rate)
time.sleep(2)  # Wait for the connection to initialize

try:
    while True:
        if ser.in_waiting > 0:
            # Read and print the data from Arduino
            data = ser.readline().decode('utf-8').strip()
            print("Received:", data)

except KeyboardInterrupt:
    print("Program stopped by user")

finally:
    ser.close()
