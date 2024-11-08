# random matrix testing to determine application of matlab matrices

import numpy

D = numpy.array([9.65, 1.68, 31.41])

A = numpy.array([[0.9966, -0.0040, -0.027], [-0.004, 1.0545, -0.0016], [-0.0270, -0.0016, 0.9522]])
b = numpy.array([-17.3563, -8.4044, -3.5274])

# successful 
y = numpy.subtract(D,b)

x = numpy.dot(y, A)

print(x)