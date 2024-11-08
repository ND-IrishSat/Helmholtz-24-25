# pid computations

from simple_pid import PID

pidX = PID(5, 2, 2, setpoint=0)
pidY = PID(5, 2, 2, setpoint=0)
pidZ = PID(5, 2, 2, setpoint=0)

pidX.output_limits = (0.00, 100.00)
pidY.output_limits = (0.00, 100.00)
pidZ.output_limits = (0.00, 100.00)

# change the setpoints of each axis
def PIDsetpoints(x, y, z):
    pidX.setpoint = x
    pidY.setpoint = y
    pidZ.setpoint = z

def computePID(magX, magY, magZ):
    result = [0, 0, 0] # resulting duty cycles from PID in X Y Z

    result[0] = pidX(magX)
    result[1] = pidY(magY)
    result[2] = pidZ(magZ)

    return result


