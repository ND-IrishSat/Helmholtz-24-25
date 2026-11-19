#!/usr/bin/env python3

from generateSimulation import gen_sim_2

import os
import sys

import threading
import time
from Dependencies.R4UART import (
    initiateUART,
    refresh_buffers,
    sendPWMValues,
    sendSIMValues,
    readPWMValues,
    readMagnetometerValues,
)

'''

We're going to have one dedicated hardware controller for the Arduino Nano and R4.

'''

class CageHardware:
    def __init__(self):
        # Initialize UART ONCE 
        terminals = initiatUART(True, True)
        time.sleep(1)
        self.nanoSer = terminals[0]
        self.R4Ser = terminals[1]
        
        self._serial_lock = threading.Lock()
        self._data_lock = threading.Lock()
        
        self._latest_mag = [0.0, 0.0, 0.0]
        self._running = True
        
        # Continously Polling Thread    
        self._reader_thread = threading.Thread(target=self._poll_magnetometer, daemon=True)
        self._reader_thread.start()
    
        
        

def main(args: list[str]=sys.argv[1:]) -> None:
    
    input_file = "gen_csv/zeroed.csv"
    output_file = "run_csv/runZeroed.csv"
    pid_tries = 30
    pid_delay = 100
    
    while args:
        arg = args.pop(0)
        
        match arg:
            case '-f': input_file = args.pop(0)
            case '-o': output_file = args.pop(0)
            case '-t': pid_tries = args.pop(0)
            case '-d': pid_delay = args.pop(0)
        
    print(f'Input Name: {input_file} | Output Name: {output_file} | PID Tries: {pid_tries} | PID Delays: {pid_delay} \n')    
    print("running generate simulation")
    gen_sim_2(input_file, output_file, pid_tries, pid_delay)    
    print("finished generate simulation")
    
if __name__ == '__main__':
    main()	