# this test verifies that it's something wrong with the cage code
# the values on the value does not seem to fluctate at the same rate so i wanted to run this test
# - andres 
from Serial_Ctrl import SerialCtrl

import time

serial_object = SerialCtrl()

while True:
    print(serial_object.read_value())

    time.sleep(0.1)