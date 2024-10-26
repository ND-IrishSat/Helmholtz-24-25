import RPi.GPIO as GPIO

# hbridge gpio pins
x1 = 17
x2 = 18

y1 = 19
y2 = 20

z1 = 21
z2 = 22

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(x1, GPIO.OUT)
GPIO.setup(x2, GPIO.OUT)
GPIO.setup(y1, GPIO.OUT)
GPIO.setup(y2, GPIO.OUT)
GPIO.setup(z1, GPIO.OUT)
GPIO.setup(z2, GPIO.OUT)

# PWM setup
freq = 1000
x1PWM = GPIO.PWM(x1, freq)
x2PWM = GPIO.PWM(x2, freq)
y1PWM = GPIO.PWM(y1, freq)
y2PWM = GPIO.PWM(y2, freq)
z1PWM = GPIO.PWM(z1, freq)
z2PWM = GPIO.PWM(z2, freq)

# start all off
x1PWM.start(0)
x2PWM.start(0)
y1PWM.start(0)
y2PWM.start(0)
z1PWM.start(0)
z2PWM.start(0)

x1PWM.ChangeDutyCycle(55.65)


