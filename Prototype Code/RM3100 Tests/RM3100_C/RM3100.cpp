/* RM3100.cpp */
/*******************
 * RM3100 Magnetometer Library Code File
 * 
 * Developed for IrishSat GOAT Lab EE 2024-25
 * 
 * Heavily Based Off: https://github.com/hnguy169/RM3100-Arduino/blob/main/RM3100_Arduino_I2C/RM3100_Arduino_I2C.ino
 * RM3100 Datasheet: https://www.tri-m.com/products/pni/RM3100-User-Manual.pdf
 * With lots of bitwise, cpp & wire.h help from Chat <3
 * And many thanks to Geeks4Geeks cpp tutorials
 * 
 * Bernardo Lozano
 *******************/

#include "RM3100.h"
#include <iostream>

#define RM3100SlAddress 0x20 // Slave address

// pin definitions
#define DPinReady 9// Data Pin Ready

// internal register locations (without the Read/Write bit) // good
#define RM3100_REVID_REG 0x36 // Hexadecimal address for the Revid internal register
#define RM3100_POLL_REG 0x00 // Hexadecimal address for the Poll internal register
#define RM3100_CMM_REG 0x01 // Hexadecimal address for the CMM internal register
#define RM3100_STATUS_REG 0x34 // Hexadecimal address for the Status internal register

// internal register locations (x, y, z values) // good
#define RM3100_CCX00 0x04 // x cycle count - MSB
#define RM3100_CCX01 0x05 // x cycle count - LSB
#define RM3100_CCY00 0x06 // y cycle count - MSB
#define RM3100_CCY01 0x07 // y cycle count - LSB
#define RM3100_CCZ00 0x08 // z cycle count - MSB
#define RM3100_CCZ01 0x09 // z cycle count - LSB

// internal measurement register locations (x, y, z values)
#define RM3100_MXREG 0x24
#define RM3100_MYREG 0x27
#define RM3100_MZREG 0x2A

// gain global variables
float GAIN_X;
float GAIN_Y;
float GAIN_Z;

// Constructor
RM3100::RM3100(uint8_t i2cAddress) : _i2cAddress(i2cAddress) {}

// Initialization
void RM3100::begin() {
  Wire.begin();  // Start I2C communication
}

// Reset function
void RM3100::reset() {
  writeRegister8(RM3100_POLL_REG, 0x02);  // Reset command as per the datasheet
}

// Set Cycle Count
// Acceptable values: 50, 100, 200 (higher = more data, less accurate)
void RM3100::setCycleCount(uint16_t cycleCountX, uint16_t cycleCountY, uint16_t cycleCountZ) {
    writeRegister16(RM3100_CCX00, cycleCountX);
    writeRegister16(RM3100_CCY00, cycleCountY);
    writeRegister16(RM3100_CCZ00, cycleCountZ);
    // Gain equations to set gain according to datasheet 3.1
    GAIN_X = 0.3671 * (float)cycleCountX + 1.5;
    GAIN_Y = 0.3671 * (float)cycleCountY + 1.5;
    GAIN_Z = 0.3671 * (float)cycleCountZ + 1.5;
}

// Turns on/off Single-Time Measurement (all axes)
// see 5.3 on manual for 0x70
void RM3100::initiateSingleMeasurement() {
    writeRegister16(RM3100_POLL_REG, 0x70);
}

void RM3100::stopSingleMeasurement() {
    writeRegister16(RM3100_POLL_REG, 0x00);
}

// Turns on/off Continuous Measurement (all axes)
// see 5.2 on manual for 0x79
void RM3100::initiateContinuousMeasurement() {
    writeRegister16(RM3100_CMM_REG, 0x79);
}

// start: 1
// alarm: 0 
// drdm: 1
// drdm: 0
// cmx, cmy, cmz: 1 
// LDM: 1
// 01111001

void RM3100::stopContinuousMeasurement() {
    writeRegister16(RM3100_CMM_REG, 0x00);
}

// Handshake with RM3100
// returns false if handshake failed
bool RM3100::isDataReady() {
    Wire.beginTransmission(_i2cAddress);
    Wire.write(RM3100_STATUS_REG);
    Wire.endTransmission();
    Wire.requestFrom(_i2cAddress, 1);
    if (Wire.available()) {
        return (Wire.read() & 0x80) != 0;
    }
    return false;
}

// Functions to read RM3100 values
int32_t RM3100::readXAxis() {
    return readRegister24(RM3100_MXREG);
}

int32_t RM3100::readYAxis() {
    return readRegister24(RM3100_MYREG);
}

int32_t RM3100::readZAxis() {
    return readRegister24(RM3100_MZREG);
}

// Reads all registers at once (in uT)
// For not uT, multiply values by gain = 0.3671 * (float)cycleCountX + 1.5
void RM3100::readXYZuT(float &x, float &y, float &z) {
    x = (float) readXAxis() / GAIN_X;
    y = (float) readYAxis() / GAIN_Y;
    z = (float) readZAxis() / GAIN_Z;
}

// Helper Functions
// Write a 16-bit value to two consecutive registers
bool RM3100::writeRegister16(uint8_t reg, uint16_t value) {
  Wire.beginTransmission(_i2cAddress);
  Wire.write(reg);
  Wire.write(value >> 8);  // Most Significat Byte
  Wire.write(value & 0xFF);  // Least Significant Byte
  if (Wire.endTransmission() != 0) {  // Check for I2C error
    return false;  // Transmission failed
  }
  return true;
}

// Write an 8-bit value to a register
bool RM3100::writeRegister8(uint8_t reg, uint8_t value) {
  Wire.beginTransmission(_i2cAddress);
  Wire.write(reg);
  Wire.write(value);
  if (Wire.endTransmission() != 0) {  // Check for I2C error
    return false;  // Transmission failed
  }
  return true;
}

// Read a 24-bit value (3 bytes) from three consecutive registers
int32_t RM3100::readRegister24(uint8_t reg) {
  int32_t result = 0;
  Wire.beginTransmission(_i2cAddress);
  Wire.write(reg);
  Wire.endTransmission();
  Wire.requestFrom(_i2cAddress, 3);

  if (Wire.available() == 3) {
    result = (Wire.read() << 16);  // Most Significant Byte
    result |= (Wire.read() << 8);  // Mid Byte
    result |= Wire.read();  // Least Significant Byte
  }
  return result;
}