#include <Arduino.h>
#include "pwm.h" // Arduino PWM library

// H-Bridge input pins
#define PX_PIN 3
#define NX_PIN 5
#define PY_PIN 6
#define NY_PIN 9
#define PZ_PIN 10
#define NZ_PIN 11

// Instantiate PWM objects
PwmOut xBridge(PX_PIN);
PwmOut yBridge(PY_PIN);
PwmOut zBridge(PZ_PIN);

// PWM control variables
float X_PWM = 0, Y_PWM = 0, Z_PWM = 0;
float PWM_FREQ = 220, PREV_PWM_FREQ = 220;
float PWM_PERIOD_US = (1 / PWM_FREQ) * 1000000;

void setup() {
    Serial.begin(9600);

    // Set up negative H-Bridge pins
    pinMode(PX_PIN, OUTPUT);
    pinMode(PY_PIN, OUTPUT);
    pinMode(PZ_PIN, OUTPUT);

    pinMode(NX_PIN, OUTPUT);
    pinMode(NY_PIN, OUTPUT);
    pinMode(NZ_PIN, OUTPUT);

    // Initialize PWM signals
    xBridge.begin(PWM_PERIOD_US, 0);
    yBridge.begin(PWM_PERIOD_US, 0);
    zBridge.begin(PWM_PERIOD_US, 0);

    //attachInterrupt(digitalPinToInterrupt(2), invertPWMX, CHANGE);
    //attachInterrupt(digitalPinToInterrupt(8), invertPWMY, CHANGE);
    //attachInterrupt(digitalPinToInterrupt(12), invertPWMZ, CHANGE);
}

void loop() {
    if (Serial.available() > 0) {
        String command = Serial.readStringUntil('\n');
        command.trim();

        if (parseValues(command)) {
            updatePWM();
        } else {
            Serial.println("Error: Incorrect data format.");
        }
    }
}

void updatePWM() {
    xBridge.pulse_perc(X_PWM);
    yBridge.pulse_perc(Y_PWM);
    zBridge.pulse_perc(Z_PWM);

    if (PWM_FREQ != PREV_PWM_FREQ) {
        float newPeriod = (1 / PWM_FREQ) * 1000;
        xBridge.period(newPeriod);
        yBridge.period(newPeriod);
        zBridge.period(newPeriod);
        PREV_PWM_FREQ = PWM_FREQ;
    }
}

bool parseValues(String input) {
    return sscanf(input.c_str(), "%f %f %f %f", &X_PWM, &Y_PWM, &Z_PWM, &PWM_FREQ) == 4;
}

// Interrupt functions to invert PWM signals
void invertPWMX() { digitalWrite(NX_PIN, !digitalRead(PX_PIN)); }
void invertPWMY() { digitalWrite(NY_PIN, !digitalRead(PY_PIN)); }
void invertPWMZ() { digitalWrite(NZ_PIN, !digitalRead(PZ_PIN)); }
