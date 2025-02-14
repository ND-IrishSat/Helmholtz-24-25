
import time
import matplotlib.pyplot as plt

from Dependencies.R4UART import initiateUART # UART code 
from Dependencies.extraneous import millis # import extraneous functions
from Dependencies.R4UART import sendPWMValues, initiateUART # UART code 

#                x  y  z
timeVector = []
timeVar = 0

terminals = initiateUART(True, True)
time.sleep(1)
nanoSer = terminals[0]
R4Ser = terminals[1]

magOutputX = []
magOutputY = []
magOutputZ = []

startTime = millis()

print("starting")

xPWM = 20
yPWM = 20
zPWM = 20
freq_PWM = 1000
period = (1/freq_PWM)*100000
time.sleep(2)
sendPWMValues(0, 0, 40, 0, 80, 0, 10000, 0, 0, R4Ser)

while(True):
    
    magnetometerOutput = nanoSer.readline().decode('utf-8').strip().split()
    try: 
        
        magX = round(float(magnetometerOutput[0]), 2)
        magY = round(float(magnetometerOutput[1]), 2)
        magZ = round(float(magnetometerOutput[2]), 2)
        # print(str(magX) + " " + str(magY) + " " + str(magZ))
    
        magOutputX.append(magX)
        magOutputY.append(magY)
        magOutputZ.append(magZ)
    except:
        magOutputX.append(magOutputX[len(magOutputX) - 1])
        magOutputY.append(magOutputY[len(magOutputY) - 1])
        magOutputZ.append(magOutputZ[len(magOutputZ) - 1])
    
    nanoSer.reset_input_buffer()
    nanoSer.reset_output_buffer()
    
    R4Ser.reset_input_buffer()
    R4Ser.reset_output_buffer()
    
    timeVector.append(timeVar)
    timeVar += 1

    if(millis() - startTime > 3000):
        break

# print(timeVector[len(timeVector - 1)])
                  
fig, ax = plt.subplots(3)

ax[0].plot(timeVector,magOutputX, color = "red", label = "Real")
ax[0].set_ylim(-100, 100)
ax[1].plot(timeVector,magOutputY, color = "red")
ax[1].set_ylim(-100, 100)
ax[2].plot(timeVector,magOutputZ, color = "red")
ax[2].set_ylim(50, 150)
plt.show()
