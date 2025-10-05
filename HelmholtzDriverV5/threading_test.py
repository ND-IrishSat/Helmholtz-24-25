import serial
import serial.tools.list_ports

import threading

import time
import queue

def initiateUART(magnetometer, PWM):
    stop_event = threading.Event()
    
    try:
        if(magnetometer):
            nanoSer = serial.Serial('/dev/serial/by-id/usb-Arduino_LLC_Arduino_NANO_33_IoT_8845351E50304D48502E3120FF0E180B-if00',115200)
            nanoSer.flushInput()
        else:
            nanoSer = ""
            
        if(PWM):
            R4Ser = serial.Serial('/dev/serial/by-id/usb-Arduino_UNO_WiFi_R4_CMSIS-DAP_F412FA74EB4C-if01', 9600)
            R4Ser.flushInput()
        else:
            R4Ser = ""
            
        while not stop_event.is_set():
            if nanoSer.in_waiting > 0:
                line = nanoSer.readline()
                
                try:
                    data_str = line.decode('utf-8').strip()
                    print(data_str)
                except:
                    print("warnign: Received non UTF-8 serial data")
            time.sleep(0.001)
            
    except KeyboardInterrupt:
        stop_event.set()
        print("User Stopped the program")

initiateUART(True, True)

    
    
    