import serial

class SerialCtrl:
    def __init__(self, port='/dev/serial/by-id/usb-Arduino_LLC_Arduino_NANO_33_IoT_8845351E50304D48502E3120FF0E180B-if00', baudrate=115200, timeout=1):
        self.ser = serial.Serial(port, baudrate, timeout=timeout)
        self.ser.flushInput()
        self.previous_value = [0,0,0]
        
    def give_serial(self):
        return self.ser
    
    # Python decorator; method does not require an instance of the class to be called and cannot access instance-specific data
    @staticmethod
    def isValidString(s: str) -> bool:
        return "." in s and not s.startswith(".")
    
    def read_value(self):
        try:
            line=self.ser.readline().decode('utf-8', errors='replace').strip().split()
            if not line:
                return None
            # if we were to read in the values they would be read as .5 which would induce a large error
            # thus the isValidString is need to prevent large jump in values
            # spilt needs to be before the valid string
            if line and self.isValidString(line[0]) and len(line)== 3:
                mag_array = [float(value) for value in line]
                self.previous_value = mag_array
                print(mag_array)
                return mag_array
            else:
                print(self.previous_value)
                return self.previous_value
            
        except Exception as e:
            print(f"Serial read error: {e}")
        return None
    
    def close(self):
        # Safely closes the function 
        try:
            self.ser.close()
        except Exception:
            pass
