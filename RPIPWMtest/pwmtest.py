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

freq = 6803
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
