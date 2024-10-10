/* RM3100.h */
/*******************
 * RM3100 Magnetometer Library Header File
 * 
 * Developed for IrishSat GOAT Lab EE 2024-25
 * Bernardo Lozano
 *******************/

#ifndef RM3100_H
#define RM3100_H

#include <Arduino.h>
#include <Wire.h>

class RM3100 {
    public:
        // Constructor
        RM3100(uint8_t i2cAddress = 0x20);

        // Initialization
        void begin();

        // Reset
        void reset();

        // Configuration
        void setCycleCount(uint16_t cycleCountX, uint16_t cycleCountY, uint16_t cycleCountZ);

        // Measurement Functions
        void initiateSingleMeasurement();
        void stopSingleMeasurement();
        void initiateContinuousMeasurement();
        void stopContinuousMeasurement();
        bool isDataReady();
        
        // Read Axis Data
        int32_t readXAxis();
        int32_t readYAxis();
        int32_t readZAxis();
        void readXYZuT(int32_t &x, int32_t &y, int32_t &z);  // Read all axes in one call

    private:
        // I2C Communication Functions
        bool writeRegister8(uint8_t reg, uint8_t value);
        bool writeRegister16(uint8_t reg, uint16_t value);
        int32_t readRegister24(uint8_t reg);

        // Internal variables
        uint8_t _i2cAddress;
    private:
}

#endif