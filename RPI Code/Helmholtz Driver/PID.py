# pid computations
# p is positive direction
# n is negative direction

from simple_pid import PID

kP = 0.25
kI = 0.25
kD = 0.25

pidX = PID(kP, kI, kD, setpoint=0)

pidY = PID(kP, kI, kD, setpoint=0)

pidZ = PID(kP, kI, kD, setpoint=0)

pidX.output_limits = (-100.00, 100.00)
pidY.output_limits = (-100.00, 100.00)
pidZ.output_limits = (-100.00, 100.00)


# change the setpoints of each axis
def PIDsetpoints(x, y, z):

    # set each direction setpoint to same
    pidX.setpoint = x
    pidY.setpoint = y
    pidZ.setpoint = z


def computePID(magX, magY, magZ):
    result = [0, 0, 0] # resulting duty cycles from PID in Xp Xm Yp Ym Zp Zm

    result[0] = pidX(magX)
    result[1] = pidY(magY)
    result[2] = pidZ(magZ)

    return result


