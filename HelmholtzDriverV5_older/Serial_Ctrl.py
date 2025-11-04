import serial

class SerialCtrl:
    def __init__(self, port='/dev/serial/by-id/usb-Arduino_LLC_Arduino_NANO_33_IoT_8845351E50304D48502E3120FF0E180B-if00', baudrate=115200, timeout=1):
        self.ser = serial.Serial(port, baudrate, timeout=timeout)
        self.ser.flushInput()
        self.previous_value = [0,0,0]
        
    def isValidString(self, s: str) -> bool:
        return "." in s and not s.startswith(".")
    
    def read_value(self):
        try:
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()
            
            line = self.ser.readline().decode('utf-8').strip().split()
                 
            if line and self.isValidString(line[0]) and len(line) == 3:
                mag_array = [float(x) for x in line]
                self.previous_value = mag_array
                return mag_array
            
            return self.previous_value
        
        except Exception as e:
            print(f"serial errors : {e}")
            
        return self.previous_value
    
    def read_value_1(self):
        try:
            # Clean Start
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()
            
            line = self.ser.readline().decode('utf-8').strip().split()
            # if we were to read in the values they would be read as .5 which would induce a large error
            # thus the isValidString is need to prevent large jump in values
            # spilt needs to be before the valid string
            if line and self.isValidString(line[0]):
                # Check that Data is here 
                mag_array = [float(x) for x in line]
                
                if len(mag_array) == 3:
                    self.previous_value = mag_array
                    return mag_array
                else:
                    return None
            else:
                return self.previous_value
          
        except Exception as e:
            print(f"Serial read error: {e}")
        return None
    