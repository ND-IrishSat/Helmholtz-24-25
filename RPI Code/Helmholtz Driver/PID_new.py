# PID set points
xMagSet = 0

#              P  I  D
xParameters = [2.1, 0, 0]
yParameters = [2, 0, 0]
zParameters = [0.6, 0, 0]

def xPID(goalPoint, currentPoint, prevPoint, prevCntrlPos, prevCntrlNeg, maxVal, dt):
    # output is pwm signal (0-100)
    # magnetic field is (-75,100)
    kp = xParameters[0]
    ki = xParameters[1]
    kd = xParameters[2]



    kp = 2.1 - (goalPoint * 0.016)

        
    if (prevCntrlPos == 0):
        prevCntrl = -prevCntrlNeg
    else:
         prevCntrl = prevCntrlPos
         
    # Approx deriv
    magDot = (currentPoint-prevPoint)/dt
    
    delta_pwm = -kp*(currentPoint-goalPoint) - kd*magDot
    
    output = prevCntrl + delta_pwm
    
    # print("current point: ", currentPoint)
    
    # print("Output: ", output)
    # print("magDot: ", magDot)

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

    # print("Positive Value: ", str(magPlusMinus[0]))
    # print("Negative Value: ", str(magPlusMinus[1]))
    # print(" ")
    
    return magPlusMinus
    

def yPID(goalPoint, currentPoint, prevPoint, prevCntrlPos, prevCntrlNeg, maxVal, dt):
    # output is pwm signal (0-100)
    # magnetic field is (-75,100)
    kp = yParameters[0]
    ki = yParameters[1]
    kd = yParameters[2]
    
    if(goalPoint > 20):
        kp = 1

    if (prevCntrlPos == 0):
        prevCntrl = -prevCntrlNeg
    else:
         prevCntrl = prevCntrlPos
         
    # Approx deriv
    magDot = (currentPoint-prevPoint)/dt
    
    delta_pwm = -kp*(currentPoint-goalPoint) - kd*magDot
    
    output = prevCntrl + delta_pwm
    
    # print("current point: ", currentPoint)
    
    # print("Output: ", output)
    # print("magDot: ", magDot)

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

    # print("Positive Value: ", str(magPlusMinus[0]))
    # print("Negative Value: ", str(magPlusMinus[1]))
    # print(" ")
    
    return magPlusMinus

def zPID(goalPoint, currentPoint, prevPoint, prevCntrlPos, prevCntrlNeg, maxVal, dt):
    # output is pwm signal (0-100)
    # magnetic field is (-75,100)
    kp = zParameters[0]
    ki = zParameters[1]
    kd = zParameters[2]

    if (prevCntrlPos == 0):
        prevCntrl = -prevCntrlNeg
    else:
         prevCntrl = prevCntrlPos
         
    # Approx deriv
    magDot = (currentPoint-prevPoint)/dt
    
    delta_pwm = -kp*(currentPoint-goalPoint) - kd*magDot
    
    output = prevCntrl + delta_pwm
    
    # print("current point: ", currentPoint)
    
    # print("Output: ", output)
    # print("magDot: ", magDot)

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

    # print("Positive Value: ", str(magPlusMinus[0]))
    # print("Negative Value: ", str(magPlusMinus[1]))
    # print(" ")
    
    return magPlusMinus
    