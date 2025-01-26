
from PySol.sol_sim import generate_orbit_data
import pandas as pd
import os
import time

oe = [121, 6_800, 0.0000922, 51, -10, 80]
total_time = 3 # in hours
timestep = 1.0 # time step in seconds
file_name = "magneticFields.csv"
store_data = True
generate_GPS = False
generate_RAM = False

generate_orbit_data(oe, total_time, timestep, file_name, store_data, generate_GPS, generate_RAM)

script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, "outputs")
os.makedirs(output_dir, exist_ok=True)
        
# Full path to output file
output_path = os.path.join(output_dir, file_name)

time.sleep(2)

pd.read_csv(output_path)
