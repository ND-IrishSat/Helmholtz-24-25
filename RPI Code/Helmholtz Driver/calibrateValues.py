
import numpy

# A coefficients
A = numpy.array([[0.9966, -0.0040, -0.027], 
                 [-0.004, 1.0545, -0.0016], 
                 [-0.0270, -0.0016, 0.9522]])

# b coefficients
b = numpy.array([-17.3563, -8.4044, -3.5274])

def calibrate(magX, magY, magZ):
    values = numpy.array([magX, magY, magZ])

    results = numpy.dot(numpy.subtract(values,b), A)

    return results
    