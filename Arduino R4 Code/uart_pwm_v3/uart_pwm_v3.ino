#include "pwm.h" // Arduino PWM library

// H-Bridge pin definitions
#define X1 3
#define X2 5
#define Y1 6
#define Y2 9
#define Z1 10
#define Z2 11

// PWM objects
PwmOut pwmBridges[] = { PwmOut(X1), PwmOut(X2), PwmOut(Y1), PwmOut(Y2), PwmOut(Z1), PwmOut(Z2) };

// PWM control variables
float dutyCycles[6] = {0}, freqs[3] = {200, 200, 200}, prevFreqs[3] = {200, 200, 200};
String incomingData = "";

void setup() {
    Serial.begin(9600);
    
    // Initialize all PWM outputs with default frequency and 0% duty cycle
    for (int i = 0; i < 6; i++) {
        pwmBridges[i].begin(5000, 0.0);
        pwmBridges[i].pulse_perc(0);
    }
}

void loop() {
    if (Serial.available() > 0) {
        char receivedChar = Serial.read();
        if (receivedChar == '\n') {
            if (parseValues(incomingData)) {
                updatePWM();
            }
            incomingData = "";  // Clear buffer
        } else {
            incomingData += receivedChar;
        }
    }
}

void updatePWM() {
    // Update duty cycles
    for (int i = 0; i < 6; i++) {
        pwmBridges[i].pulse_perc(dutyCycles[i]);
    }

    // Update frequencies if changed
    for (int i = 0; i < 3; i++) {
        if (freqs[i] != prevFreqs[i]) {
            pwmBridges[i * 2].period_us((freqs[i]) * 1000);    // Update first H-Bridge pin
            pwmBridges[i * 2 + 1].period_us((freqs[i]) * 1000); // Update second H-Bridge pin
            prevFreqs[i] = freqs[i];  // Store new frequency
        }
    }
}

bool parseValues(String input) {
    return sscanf(input.c_str(), "%f %f %f %f %f %f %f %f %f",
                  &dutyCycles[0], &dutyCycles[1], &dutyCycles[2],
                  &dutyCycles[3], &dutyCycles[4], &dutyCycles[5],
                  &freqs[0], &freqs[1], &freqs[2]) == 9;
}
