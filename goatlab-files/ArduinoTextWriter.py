import serial
import time

# # serial.Serial('COMXX',baud rate)
ser = serial.Serial(port='COM10',baudrate=115200)
# Clears data that has already been received and waiting in the input buffer of a communication channel
ser.reset_input_buffer()

# Creates and writes on ardunio_output.txt file
with open("arduino_output.txt", "w") as file:
    while True:
        try:
            # Read the data from Arduino
            if ser.in_waiting > 0:
                arduino_output = ser.readline().decode('utf-8').strip()
                # print(arduino_output)  # Testing print statement to display the output
                file.write(arduino_output + "\n")  # Save the output to the text file
                file.flush()  # Ensure data is written to the file
        # Hold ctrl + C to end the program
        except KeyboardInterrupt:
            print("Stopped by user")
            break
