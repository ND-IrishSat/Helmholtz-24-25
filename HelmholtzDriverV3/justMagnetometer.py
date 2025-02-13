
import time
import matplotlib.pyplot as plt

from Dependencies.R4UART import initiateUART # UART code 
from Dependencies.extraneous import millis # import extraneous functions

#                x  y  z
timeVector = []
timeVar = 0

terminals = initiateUART(True, False)
time.sleep(1)
nanoSer = terminals[0]
R4Ser = terminals[1]

magOutputX = []
magOutputY = []
magOutputZ = []

startTime = millis()

while(True):

    magnetometerOutput = nanoSer.readline().decode('utf-8').strip().split()
    if magnetometerOutput:
        
        magX = round(float(magnetometerOutput[0]), 2)
        magY = round(float(magnetometerOutput[1]), 2)
        magZ = round(float(magnetometerOutput[2]), 2)
        print(str(magX) + " " + str(magY) + " " + str(magZ))

    magOutputX.append(magX)
    magOutputY.append(magY)
    magOutputZ.append(magZ)

    # nanoSer.reset_input_buffer()
    # nanoSer.reset_output_buffer()
    
    # R4Ser.reset_input_buffer()
    # R4Ser.reset_output_buffer()
    
    timeVector.append(timeVar)
    timeVar += 1

    if(startTime - millis() > 10000):
        break

fig, ax = plt.subplots(3)

ax[0].plot(timeVector,magOutputX, color = "red", label = "Real")

ax[1].plot(timeVector,magOutputY, color = "red")

ax[2].plot(timeVector,magOutputZ, color = "red")

plt.show()
