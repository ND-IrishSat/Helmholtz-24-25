#!/usr/bin/env python3

from generateSimulation import gen_sim
from cage_hardware import CageHardware 
import sys
import threading

def main(args: list[str]=sys.argv[1:]) -> None:
    # Creates the hardware managers
    CageMaster = CageHardware()
    # Creates a stop flag
    gen_stop_event = threading.Event()

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

    print("Start Sim")
    gen_sim(CageMaster, gen_stop_event, input_file, output_file, pid_tries, pid_delay)
    print("End sim")
    
if __name__ == '__main__':
    main()	