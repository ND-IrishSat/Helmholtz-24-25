import RPi.GPIO as GPIO
import time

# hbridge gpio pins
x1 = 14
x2 = 15

y1 = 17
y2 = 18

z1 = 22
z2 = 23

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


GPIO.setup(x1, GPIO.OUT)
GPIO.setup(x2, GPIO.OUT)
GPIO.setup(y1, GPIO.OUT)
GPIO.setup(y2, GPIO.OUT)
GPIO.setup(z1, GPIO.OUT)
GPIO.setup(z2, GPIO.OUT)

freq = 3000
x1PWM = GPIO.PWM(x1, freq)
x2PWM = GPIO.PWM(x2, freq)
y1PWM = GPIO.PWM(y1, freq)
y2PWM = GPIO.PWM(y2, freq)
z1PWM = GPIO.PWM(z1, freq)
z2PWM = GPIO.PWM(z2, freq)
x1PWM.start(0)
x2PWM.start(0)
y1PWM.start(0)
y2PWM.start(0)
z1PWM.start(0)
z2PWM.start(0)




# PWM setup
# freq = int(input("Enter the frequency: "))



# start pwm at 0



#ramp function:
def rampDutyCycle():
     
     rampX = False
     rampY = False
     rampZ = False
     
     incDelay = float(input("Enter delay b/w increments (in sec): "))
     
     ansX = input("Ramp x coil? (Y/N): ")
     if((ansX == 'Y') or (ansX == 'y')):
         rampX = True
     ansY = input("Ramp y coil? (Y/N): ")
     if((ansY == 'Y') or (ansY == 'y')):
         rampY = True 
     ansZ = input("Ramp z coil? (Y/N): ")
     if((ansX == 'Y') or (ansX == 'y')):
         rampZ = True
     
     while True: # run forever
         if not(rampX or rampY or rampZ):
            print("No coil selected.")
            break
         for i in range(0,100):
             if rampX:
                x1PWM.ChangeDutyCycle(i)
                print("xDyC: ",i)
             if rampY:
                 y1PWM.ChangeDutyCycle(i)
             if rampZ:
                 z1PWM.ChangeDutyCycle(i)
                 
             time.sleep(incDelay)
         for i in range(100, 0, -1):
            if rampX:
                x1PWM.ChangeDutyCycle(i)
                print("xDyC: ",i)
            if rampY:
                y1PWM.ChangeDutyCycle(i)
            if rampZ:
                z1PWM.ChangeDutyCycle(i)
            time.sleep(incDelay)
     
    
ans = input("Do you want the duty cycle as a ramp? (Y/N): ")
if((ans == 'Y') or (ans == 'y')):
    rampDutyCycle()
else:
    # User Input duty cycles:
    x1_cyc = float(input("x1 duty cycle: "))
    x2_cyc = float(input("x2 duty cycle: "))
    y1_cyc = float(input("y1 duty cycle: "))
    y2_cyc = float(input("y2 duty cycle: "))
    z1_cyc = float(input("z1 duty cycle: "))
    z2_cyc = float(input("z2 duty cycle: "))

    # start duty cycles
    x1PWM.ChangeDutyCycle(x1_cyc)
    x2PWM.ChangeDutyCycle(x2_cyc)
    y1PWM.ChangeDutyCycle(y1_cyc)
    y2PWM.ChangeDutyCycle(y2_cyc)
    z1PWM.ChangeDutyCycle(z1_cyc)
    z2PWM.ChangeDutyCycle(z2_cyc)
    

# 
# 