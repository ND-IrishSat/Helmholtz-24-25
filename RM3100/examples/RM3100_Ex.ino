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