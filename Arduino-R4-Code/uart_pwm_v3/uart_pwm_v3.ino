#include "pwm.h" // Arduino PWM library

// H-Bridge pin definitions
#define X1 3
#define X2 5
#define Y1 6
#define Y2 9
#define Z1 10
#define Z2 11

// PWM objects
PwmOut xBridge1(X1);
PwmOut xBridge2(X2);
PwmOut yBridge1(Y1);
PwmOut yBridge2(Y2);
PwmOut zBridge1(Z1); 
PwmOut zBridge2(Z2);

// PWM control variables
float x1_duty = 0, x2_duty = 0, y1_duty = 0, y2_duty = 0, z1_duty = 0, z2_duty = 0;
String incomingData = "";

void setup() {
    Serial.begin(9600);
    
    // Initialize PWM outputs with 0% duty cycle
    // freq in microseconds
    xBridge1.begin(147, 0.0);
    xBridge2.begin(147, 0.0);
    yBridge1.begin(147, 0.0);
    yBridge2.begin(147, 0.0);
    zBridge1.begin(147, 0.0);
    zBridge2.begin(147, 0.0);

    xBridge1.pulse_perc(0);
    xBridge2.pulse_perc(0);
    yBridge1.pulse_perc(0);
    yBridge2.pulse_perc(0);
    zBridge1.pulse_perc(0);
    zBridge2.pulse_perc(0);
}

void loop() {
    if (Serial.available() > 0) {
        char receivedChar = Serial.read();
        if (receivedChar == '\n') {
            if (parseValues(incomingData)) {
                updatePWM();
                Serial.println("HEHHEHEHE");
            }
            incomingData = "";  // Clear buffer
        } else {
            incomingData += receivedChar;
        }
    }
}

void updatePWM() {
    // Update duty cycles
    xBridge1.pulse_perc(x1_duty);
    xBridge2.pulse_perc(x2_duty);
    yBridge1.pulse_perc(y1_duty);
    yBridge2.pulse_perc(y2_duty);
    zBridge1.pulse_perc(z1_duty);
    zBridge2.pulse_perc(z2_duty);
}

bool parseValues(String input) {
    input.trim();  // Remove leading/trailing whitespace
    int startIdx = 0, spaceIdx;
    float* values[] = { &x1_duty, &x2_duty, &y1_duty, &y2_duty, &z1_duty, &z2_duty };

    for (int i = 0; i < 6; i++) {
        spaceIdx = input.indexOf(' ', startIdx);
        if (spaceIdx == -1 && i < 5) return false; // Ensure we have all 6 values

        *values[i] = input.substring(startIdx, (i < 5) ? spaceIdx : input.length()).toFloat();
        startIdx = spaceIdx + 1;
    }

    return true;
}
