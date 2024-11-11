# pid computations
# p is positive direction
# n is negative direction

from simple_pid import PID

pidXp = PID(5, 2, 2, setpoint=0)
pidXn = PID(5, 2, 2, setpoint=0)

pidYp = PID(5, 2, 2, setpoint=0)
pidYn = PID(5, 2, 2, setpoint=0)

pidZp = PID(5, 2, 2, setpoint=0)
pidZn = PID(5, 2, 2, setpoint=0)

# postive limits
pidXp.output_limits = (0.00, 100.00)
pidYp.output_limits = (0.00, 100.00)
pidZp.output_limits = (0.00, 100.00)

# negative limits
pidXn.output_limits = (-100.0, 0.0)
pidYn.output_limits = (-100.0, 0.0)
pidZn.output_limits = (-100.0, 0.0)

# change the setpoints of each axis
def PIDsetpoints(x, y, z):

    # set each direction setpoint to same
    pidXp.setpoint = x
    pidXn.setpoint = x

    pidYp.setpoint = y
    pidYn.setpoint = y

    pidZp.setpoint = z
    pidZn.setpoint = z


def computePID(magX, magY, magZ):
    result = [0, 0, 0, 0, 0, 0] # resulting duty cycles from PID in Xp Xm Yp Ym Zp Zm

    result[0] = pidXp(magX)
    result[1] = pidXn(magX)

    result[2] = pidYp(magY)
    result[3] = pidYn(magY)

    result[4] = pidZp(magZ)
    result[5] = pidZn(magZ)

    return result


