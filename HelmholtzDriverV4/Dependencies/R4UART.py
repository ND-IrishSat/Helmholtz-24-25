# communication from RPi -> Arduino R4 for PWM

import serial
import serial.tools.list_ports
import time

def initiateUART(magnetometer, PWM):
    
    if(magnetometer):
        nanoSer = serial.Serial('/dev/ttyACM3',115200)
    else:
        nanoSer = ""
        
    if(PWM):
        R4Ser = serial.Serial('/dev/ttyACM1', 9600)
    else:
        R4Ser = ""
   
#    ports = serial.tools.list_ports.comports()
#     devices = {}
    
#     for port in ports:
#         try:
#             ser = serial.Serial(port.device, 9600, timeout=1)
#             ser.write(b'IDENTIFY\n')
#             response = ser.readline().decode('utf-8').strip()
#             ser.close()
#             
#             print(port.device)
#             if response == "R4":
#                 devices["r4"] = port.device
#                 print("cooool")
#             elif response == "NANO":
#                 devices["nano"] = port.device
#                 print("colroool")
#         except:
#             (serial.SerialException, serial.SerialTimeoutException)
#             print(exception);
#             continue
        
#     if "r4" in devices and "nano" in devices:
#         r4 = serial.Serial(devices["r4"], 9600)
#         nan = serial.Serial(devices["nano"], 9600)
#         print("Connection to r4 and nano successful")
#     else:
#         print("Could not connect to both r4 and nano")
#         return

#     nano.reset_input_buffer()
#     nano.reset_output_buffer()
#     
#     r4.reset_input_buffer()
#     r4.reset_output_buffer()
    
#     nanoSer.reset_input_buffer()
#     nanoSer.reset_output_buffer()
    
#     R4Ser.reset_input_buffer()
#     R4Ser.reset_output_buffer()
    
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


            