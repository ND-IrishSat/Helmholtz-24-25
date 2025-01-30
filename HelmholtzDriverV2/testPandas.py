
from PySol.sol_sim import generate_orbit_data
import pandas as pd
import os
import matplotlib.pyplot as plt
import time
import random

oe = [121, 6_800, 0.0000922, 51, -10, 80]
total_time = 0.5 # in hours
timestep = 1.0 # time step in seconds
file_name = "magneticFields.csv"
store_data = True
generate_GPS = False
generate_RAM = False

generate_orbit_data(oe, total_time, timestep, file_name, store_data, generate_GPS, generate_RAM)

script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, "PySol")
os.makedirs(output_dir, exist_ok=True)
        
# Full path to output file
output_path = os.path.join(output_dir, "outputs")
output_path = os.path.join(output_path, file_name)

dataFrame = pd.read_csv(output_path)

currentFields = [0, 0, 0]

currentFields[0] = dataFrame.loc[0, 'Bx']
currentFields[1] = dataFrame.loc[0, 'By']
currentFields[2] = dataFrame.loc[0, 'Bz']

print(len(dataFrame))

timevec = [0]
yvec = [0]
othervec = [0]

movingAverage = 75

fig, ax = plt.subplots(3)

i = 0
while(i < 1000):

    ax[0].plot(timevec,yvec)
    ax[0].plot(timevec, othervec)
   
    if(i % 10 == 0):
        fig.show()
    
        fig.canvas.draw()
 
        fig.canvas.flush_events()

    i+=1
    

    # if(i >= movingAverage):
    #     timevec.remove(i - movingAverage)
    #     del yvec[i - movingAverage]

    timevec.append(i)
    yvec.append(random.randint(3, 20))
    othervec.append(random.randint(10, 30))
    time.sleep(0.1)


ax[0].plot(timevec,yvec)

plt.show()

