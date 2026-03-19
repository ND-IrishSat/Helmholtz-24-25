import serial

class SerialCtrl:
    def __init__(self, port='/dev/serial/by-id/usb-Arduino_LLC_Arduino_NANO_33_IoT_8845351E50304D48502E3120FF0E180B-if00', baudrate=115200, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout= timeout
        self.ser = serial.Serial(self.port, baudrate, timeout=timeout)
        self.ser.flushInput()
        self.previous_value = [0.0,0.0,0.0]
    
    def serial_open(self):
        if self.ser and self.ser.is_open:
            print(f"SO. serial Port is already opened; port: {self.port}")
            return
        try:
            # if ser object exists open up the port, else open a new port. Reset the buffer 
            if self.ser:
                self.ser.open()
            else:
                self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            self.ser.reset_input_buffer()
            
        except Exception as e:
            print(f"SO. serial port opening failure: {e}")
            self.ser = None

    def isValidString(self, s: str) -> bool:
        return "." in s and not s.startswith(".")
    
    def read_value(self):
        try:
            latest_valid_data = None
            # reads and keeps the most recent valid data
            while self.ser.in_waiting > 0:
                line = self.ser.readline().decode('utf-8').strip()
                # skips empty lines
                if not line:
                    continue # changed from returning none to continue
                
                # parses and does string validation
                line_parts = line.split()
                if line_parts and self.isValidString(line_parts[0]) and len(line_parts) == 4:
                    try:
                        mag_array = [float(x) for x in line_parts]
                        latest_valid_data = mag_array
                        
                    except ValueError:
                        continue
                    
            if latest_valid_data is not None:
                self.previous_value = latest_valid_data
                # print(f"previous value is now : {self.previous_value}")
                return latest_valid_data
            
            return None
        except Exception as e:
            print(f"RV. serial errors : {e}\n------------------------\nwill return {self.previous_value}\n------------------------\n")
            return self.previous_value
    
    def serial_close(self):
        try:
            if self.ser and self.ser.is_open:
                self.ser.close()
        except Exception as e:
            print(f"SC. serial closing error {e}\n")
        finally:
            self.ser = None