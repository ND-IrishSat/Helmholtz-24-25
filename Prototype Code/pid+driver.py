import serial
import time
from simple_pid import PID

# PID Gibberish
pid= PID(5, 2, 2, setpoint=1)

pid.output_limits(0.00, 100.00)

pid.setpoint = 75

mag_field = 0

while True:
    duty = pid(mag_field)
    
    mag_field = 


if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM1',9600,timeout=1)
    ser.reset_input_buffer()
    
    while True:
        # x1 x2 y1 y2 z1 z2
        ser.write(b"50.00 0.00 50.00 0.00 50.00 0.00")
        print(ser.readline().decode('utf-8').rstrip())
        time.sleep(10)
        ser.write(b"100.00 0.00 100.00 0.00 100.00 0.00")
        print(ser.readline().decode('utf-8').rstrip())
        time.sleep(10)
 
