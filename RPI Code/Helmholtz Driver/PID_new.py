# PID set points
xMagSet = 0

# Proportional Gain
kp = 4

def PID_fun(goalPoint, currentPoint, prevPoint, maxVal, dt):
    # output is pwm signal (0-100)
    # magnetic field is (-75,100)
    kp = 8
    kd = 0
    
    # Approx deriv
    magDot = (currentPoint-prevPoint)/dt
    
    output = -kp*(currentPoint-goalPoint) - kd*magDot
    
    print("current point: ", currentPoint)
    
    print("Output: ", output)
    print("magDot: ", magDot)

    # init directions 
    magPlusMinus = [0,0] # magPlusMins[0] = positive magnetic field coil, magPlusMinus[1] = negative
    
    if output > 0:
        magPlusMinus = [output, 0]
    if output < 0:
        magPlusMinus = [0,-output]
    if output > maxVal:
        magPlusMinus = [maxVal,0]
    if output < -maxVal:
        magPlusMinus = [0,maxVal]
    print("Positive Value: ", str(magPlusMinus[0]))
    print("Negative Value: ", str(magPlusMinus[1]))
    print(" ")
    
    return magPlusMinus
    