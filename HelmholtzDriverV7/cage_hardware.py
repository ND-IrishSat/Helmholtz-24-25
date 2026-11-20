import threading
import time

from Dependencies.R4UART import (
    initiateUART,
    sendPWMValues,
    sendSIMValues,
    readMagnetometerValues,
    refresh_buffers,
)

class CageHardware:
    def __init__(self):
        # 1. Initialize UART ONCE for the entire application lifecycle
        terminals = initiateUART(True, True)
        time.sleep(1)
        self.nanoSer = terminals[0]
        self.R4Ser = terminals[1]
        
        self._serial_lock = threading.Lock()
        self._data_lock = threading.Lock()
        
        self._latest_mag = (0.0, 0.0, 0.0)
        self._running = True
        
        # 2. Start dedicated magnetometer polling thread
        self._reader_thread = threading.Thread(target=self._poll_magnetometer, daemon=True)
        self._reader_thread.start()

    def _poll_magnetometer(self):
        """Continuously reads nanoSer at max speed regardless of current mode."""
        while self._running:
            with self._serial_lock:
                mag_out = readMagnetometerValues(self.nanoSer)
            
            # The mag output has a trailing 0.0 term with the magnetic field values, so we need the >= chk
            if mag_out and len(mag_out) >= 3:
                try:
                    x, y, z = round(float(mag_out[0]), 2), round(float(mag_out[1]), 2), round(float(mag_out[2]), 2)
                    with self._data_lock:
                        self._latest_mag = (x, y, z)
                except ValueError:
                    pass
            time.sleep(0.05) # Prevent 100% CPU spin; tune to your Nano's baud/publish rate

    def get_magnetometer(self):
        """Called by BOTH the GUI and gen_sim() safely at any time."""
        with self._data_lock:
            return self._latest_mag

    def set_pwm(self, yp, yn, xn, xp, zp, zn):
        """Thread-safe PWM output to R4Ser."""
        with self._serial_lock:
            sendPWMValues(yp, yn, xn, xp, zp, zn, self.R4Ser)

    def send_sim_value(self, sim_tot):
        """Thread-safe simulated field output to nanoSer."""
        with self._serial_lock:
            sendSIMValues(sim_tot, self.nanoSer)

    def shutdown(self):
        self.set_pwm(0, 0, 0, 0, 0, 0)
        self._running = False