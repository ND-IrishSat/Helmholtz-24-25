# communication from RPi -> Arduino R4 for PWM

import serial
import time

def initiateUART():
                
        nanoSer = serial.Serial('/dev/ttyACM0',9600)
        R4Ser = serial.Serial('/dev/ttyACM2',115200)

        nanoSer.reset_input_buffer()
        nanoSer.reset_output_buffer()
        
        R4Ser.reset_input_buffer()
        R4Ser.reset_output_buffer()
        
        return [nanoSer, R4Ser]


def sendPWMValues(x1, x2, y1, y2, z1, z2, R4Ser):
    data = f"{x1} {x2} {y1} {y2} {z1} {z2}\n"
    #data = str(x1) + " " + str(x2) + " " + str(y1) + " " + str(y2) + " " + str(z1) + " " + str(z2)
    R4Ser.write(data.encode('utf-8'))
    

def readPWMValues(R4Ser):
    print(R4Ser.readline().decode('utf-8').rstrip())


def readMagnetometerValues(nanoSer):
    #print(nanoSer.readline().decode('utf-8').rstrip())
    return nanoSer.readline().decode('utf-8').rstrip()


            