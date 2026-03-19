# RM3100 Magnetometer Library
Used for communication between Arduino and RM3100 (because someone didn't bother to make a library with the magnetometer)

To be used with the 2024-25 GOAT Helmholtz cage magnetic field readings

# WARNING
As of 10/09/2024, library is untested. It compiles (I think), but since RM3100 has not arrived, it may or may not work

# Usage & Installation
Library includes .h header file and .cpp code file. They should not need to be modified, just included in arduino.ino file as a header with easy end-user operation afterwards.

Look at example file for usage within arduino code, includes all accessable library functions:

```cpp
#include <Wire.h>
#include <RM3100.h>

#define RM3100_SLAVE_ADDRESS 0x20 // I2C Address

RM3100 mag(RM3100_SLAVE_ADDRESS); // RM3100 object

void setup() {
    Serial.begin(9600);
    mag.begin();
    mag.setCycleCount(100, 100, 100); // Sets cycle count (50, 100, or 200 (larger = more data, smaller = more accurate))
    mag.initiateContinuousMeasurement();
}

void loop() {
    float x, y, z;
    if (mag.isDataReady()) {
        mag.readXYZuT(x, y, z); // Reads x, y, z in uT
        // For not uT reading, multiply return values according to equation:
        // x * gain where gain = 0.3671 * cycle_count + 1.5
    }
    // Float values cast into integers
    Serial.print("X:");
    Serial.print((int) x);
    Serial.print("Y:");
    Serial.print((int) y);
    Serial.print("Z:");
    Serial.print((int) z);
}

/* Extra bits of information: 
mag.reset(); resets magnetometer
mag.initiateSingleMeasurement(); gives one measurement
mag.stopContinuousMeasurement(); stops measurements
mag.stopSingleMeasurement(); stops single measurement (might be redundant)


--NOT CALIBRATED--
Calibration must be done by collecting a TON of values, sending them to MATLAB and running script
Matrix with calibrated offsets would be required and the x, y, z variables would need to be modified
*/
```


For how to connect magnetometer with arduino, see magnetometer documentation:
https://www.tri-m.com/products/pni/RM3100-User-Manual.pdf

(in this same datasheet you will NOT find a library so here I am)

Install library into arduino via zip library:

Download ZIP file from github

In arduino IDE:
sketch -> include library -> add .zip library -> open .zip file

# Credits
Library adapted by Bernardo Lozano

Significant inspiration from (how to operate the RM3100, memory addresses, and general structure, but made into a library): https://github.com/hnguy169/RM3100-Arduino/blob/main/RM3100_Arduino_I2C/RM3100_Arduino_I2C.ino

And with help from ChatGPT for bitwise operations bcs OH LORD and general cpp help