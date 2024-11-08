# communication from RPi -> Arduino R4 for PWM

import serial
import time

ser = 0
def initiateUART():
    if __name__ == '__main__':
                
        try: 
            ser = serial.Serial('/dev/ttyACM0',9600,timeout=1)
        except:
            print('USB port ACM1')
            ser = serial.Serial('/dev/ttyACM1',9600,timeout=1)
        else:
            print('USB port ACM0')

        ser = serial.Serial('/dev/ttyACM0',9600,timeout=1)
        ser.reset_input_buffer()


def sendPWMValues(x1, x2, y1, y2, z1, z2):
    data = str(x1) + " " + str(x2) + " " + str(y1) + " " + str(y2) + " " + str(z1) + " " + str(z2)
    ser.write(data.encode('utf-8'))

def readPWMValues():
    print(ser.readline().decode('utf-8').rstrip())
    time.sleep(0.8)

            