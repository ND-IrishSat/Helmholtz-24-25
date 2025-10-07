import serial

class SerialCtrl:
    def __init__(self, port='/dev/serial/by-id/usb-Arduino_LLC_Arduino_NANO_33_IoT_8845351E50304D48502E3120FF0E180B-if00', baudrate=115200, timeout=1):
        self.ser = serial.Serial(port, baudrate, timeout=timeout)
        self.ser.flushInput()
    
    def read_value(self):
        try:
            line = self.ser.readline().decode('utf-8').strip()
            if line:
                # Check that Data is here 
                mag_array = [float(x) for x in line.split()]
                return mag_array
        except Exception as e:
            print(f"Serial read error: {e}")
        return None
    