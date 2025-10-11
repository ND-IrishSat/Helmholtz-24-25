# communication from RPi -> Arduino R4 for PWM

import serial
import serial.tools.list_ports
import time

def initiateUART(magnetometer, PWM):
    if(magnetometer):
        nanoSer = serial.Serial('/dev/serial/by-id/usb-Arduino_LLC_Arduino_NANO_33_IoT_8845351E50304D48502E3120FF0E180B-if00',115200)
    else:
        nanoSer = ""
        
    if(PWM):
        R4Ser = serial.Serial('/dev/serial/by-id/usb-Arduino_UNO_WiFi_R4_CMSIS-DAP_F412FA74EB4C-if01', 9600)
    else:
        R4Ser = ""
    
    return [nanoSer, R4Ser]

def sendPWMValues(x1, x2, y1, y2, z1, z2, R4Ser):
    ''' Writes literal values for x, y, and z pwm values to the Arduino R4 '''
    data = f"{x1} {x2} {y1} {y2} {z1} {z2}\n"
    R4Ser.write(data.encode('utf-8'))

def readPWMValues(R4Ser):
    print(R4Ser.readline().decode('utf-8').rstrip())

def readMagnetometerValues(nanoSer):
    return nanoSer.readline().decode('utf-8').strip().split()
    # return nanoSer.readline().decode('utf-8').rstrip()


            