# applies calibrated coefficient values to raw magnetometer data

import numpy

# A coefficients
A = numpy.array([[1.0030, -0.0063, -0.0272], 
                 [-0.0063, 1.0607, -0.0042], 
                 [-0.0272, -0.0042, 0.9407]])

# b coefficients
b = numpy.array([-15.6258, -8.1023, -2.5412])

def calibrate(magX, magY, magZ):
    values = numpy.array([magX, magY, magZ])

    results = numpy.dot(numpy.subtract(values,b), A)

    return results
    