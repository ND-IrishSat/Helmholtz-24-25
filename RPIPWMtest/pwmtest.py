from gpiozero import PWMOutputDevice
import time

# hbridge gpio pins
x1 = 14
x2 = 15

y1 = 17
y2= 18

z1 = 22
z2 = 23

pwm1 = PWMOutputDevice(x1, frequency = 6803)

pwm2 = PWMOutputDevice(x2, frequency = 6803)

pwm3 = PWMOutputDevice(y1, frequency = 6803)

pwm4 = PWMOutputDevice(y2, frequency = 6803)

pwm5 = PWMOutputDevice(z1, frequency = 6803)

pwm6 = PWMOutputDevice(z2, frequency = 6803)

pwm1.value = 0.5
pwm2.value = 0.3
pwm3.value = 0.5
pwm4.value = 0.5
pwm5.value = 0.1
pwm6.value = 0.7

freq = 6803


