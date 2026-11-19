#!/usr/bin/env python3

from generateSimulation import gen_sim_2

import os
import sys

'''

We're going to have one dedicated hardware controller for the Arduino Nano and R4.

'''

import threading
import time
from Dependencies.R4UART import (
    initiateUART,
    sendPWMValues,
    sendSIMValues,
    readMagnetometerValues,
    refresh_buffers,
)

class CageHardware:
    def __init__(self):
        # 1. Initialize UART ONCE for the entire application lifecycle
        terminals = initiateUART(True, True)
        time.sleep(1)
        self.nanoSer = terminals[0]
        self.R4Ser = terminals[1]
        
        self._serial_lock = threading.Lock()
        self._data_lock = threading.Lock()
        
        self._latest_mag = (0.0, 0.0, 0.0)
        self._running = True
        
        # 2. Start dedicated magnetometer polling thread
        self._reader_thread = threading.Thread(target=self._poll_magnetometer, daemon=True)
        self._reader_thread.start()

    def _poll_magnetometer(self):
        """Continuously reads nanoSer at max speed regardless of current mode."""
        while self._running:
            with self._serial_lock:
                # Note: Ensure refresh_buffers doesn't wipe outgoing TX data
                mag_out = readMagnetometerValues(self.nanoSer)
                
            if mag_out and len(mag_out) == 3:
                try:
                    x, y, z = round(float(mag_out[0]), 2), round(float(mag_out[1]), 2), round(float(mag_out[2]), 2)
                    with self._data_lock:
                        self._latest_mag = (x, y, z)
                except ValueError:
                    pass
            time.sleep(0.005) # Prevent 100% CPU spin; tune to your Nano's baud/publish rate

    def get_magnetometer(self):
        """Called by BOTH the GUI and gen_sim() safely at any time."""
        with self._data_lock:
            return self._latest_mag

    def set_pwm(self, yp, yn, xn, xp, zp, zn):
        """Thread-safe PWM output to R4Ser."""
        with self._serial_lock:
            sendPWMValues(yp, yn, xn, xp, zp, zn, self.R4Ser)

    def send_sim_value(self, sim_tot):
        """Thread-safe simulated field output to nanoSer."""
        with self._serial_lock:
            sendSIMValues(sim_tot, self.nanoSer)

    def shutdown(self):
        self.set_pwm(0, 0, 0, 0, 0, 0)
        self._running = False

def main(args: list[str]=sys.argv[1:]) -> None:

    CageMaster = CageHardware()

    while(True):
        print(CageMaster.get_magnetometer())
        time.sleep(0.005)

    # Current the rest of the code never reaches

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