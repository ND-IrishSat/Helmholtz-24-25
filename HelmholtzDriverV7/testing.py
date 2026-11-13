#!/usr/bin/env python3

from generateSimulation import gen_sim_2

import os
import sys

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