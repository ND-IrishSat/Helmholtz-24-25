#include <Arduino.h>
#include "pwm.h" // Arduino PWM library

// h-bridge input pins 
// here we are defining the positive (PX, PY, PZ) as input 1 on the h-bridge, so input 2 is (NX, NY, NZ)
#define PX_PIN 3
#define NX_PIN 5

#define PY_PIN 6
#define NY_PIN 9

#define PZ_PIN 10
#define NZ_PIN 11

// instantiate PWM objects that will PWM input 1 of each h-brigde
// only 3 are needed because the change notification interrupt is the inversion of this signal
// which is a total of 6 signals
PwmOut xBridge(PX_PIN);
PwmOut yBridge(PY_PIN);
PwmOut zBridge(PZ_PIN);

float X_PWM = 0, Y_PWM = 0, Z_PWM = 0; // x, y, z duty cycles 

float PWM_FREQ = 220; // pwm frequency in Hz
float PREV_PWM_FREQ = PWM_FREQ;
float PWM_PERIOD = (1/PWM_FREQ) * 1000; // initial period in miliseconds 
float PWM_PERIOD_US = (1/PWM_FREQ) * 1000000; // initial period in microseconds

String incomingData = "";  // Buffer for serial data

void setup(){

    Serial.begin(9600);

    pinMode(PX_PIN, OUTPUT);
    pinMode(NX_PIN, OUTPUT);
    pinMode(PY_PIN, OUTPUT);
    pinMode(NY_PIN, OUTPUT);
    pinMode(PZ_PIN, OUTPUT);
    pinMode(NZ_PIN, OUTPUT);

    // for interrupts: pins 2, 8, 12  
    // set each negative pin to be the inverse of each positve pin upon the positive pin changing 
    attachInterrupt(digitalPinToInterrupt(2), invertPWMX, CHANGE);
    attachInterrupt(digitalPinToInterrupt(8), invertPWMY, CHANGE);
    attachInterrupt(digitalPinToInterrupt(12), invertPWMZ, CHANGE);

    xBridge.begin(PWM_PERIOD_US, 0);
    yBridge.begin(PWM_PERIOD_US, 0);
    zBridge.begin(PWM_PERIOD_US, 0);

    // start all duty cycles at 0
    xBridge.pulse_perc(70);
    yBridge.pulse_perc(30);
    zBridge.pulse_perc(10);

}

void loop(){

   while (Serial.available() > 0) {
    char receivedChar = Serial.read();
    if (receivedChar == '\n') {
      // When newline is received, process the buffer
      if (parseValues(incomingData, X_PWM, Y_PWM, Z_PWM, PWM_FREQ)) {
        updatePWM();
        //Serial.println("Data received and applied: " + incomingData);  // Optional feedback
      } else {
        //Serial.println("Error: Incorrect data format.");
      }
      incomingData = "";  // Clear the buffer
    } else {
      incomingData += receivedChar;  // Append to buffer
    }
  }

}
void updatePWM(){

  xBridge.pulse_perc(X_PWM);
  yBridge.pulse_perc(Y_PWM);
  zBridge.pulse_perc(Z_PWM);

  if(PREV_PWM_FREQ != PWM_FREQ){

    PWM_PERIOD = ((1/PWM_FREQ) * 1000);
    xBridge.period(PWM_PERIOD);
    yBridge.period(PWM_PERIOD);
    zBridge.period(PWM_PERIOD);

    PREV_PWM_FREQ = PWM_FREQ;
  }

}

bool parseValues(String input, float &X_PWM, float &Y_PWM, float &Z_PWM, float &PWM_FREQ) {
  int startIdx = 0;
  int spaceIdx;
  float values[4];
  
  for (int i = 0; i < 4; i++) {
    spaceIdx = input.indexOf(' ', startIdx);
    if (spaceIdx == -1 && i < 3) return false;  
    
    String valueStr = (i < 3) ? input.substring(startIdx, spaceIdx) : input.substring(startIdx);
    values[i] = valueStr.toFloat();
    
    startIdx = spaceIdx + 1;
  }

  X_PWM = values[0];
  Y_PWM = values[1];
  Z_PWM = values[2];
  PWM_FREQ = values[3];

  return true;
}

void invertPWMX(){
    digitalWrite(NX_PIN, !digitalRead(PX_PIN)); //Write NX as opposite of PX
}

void invertPWMY(){
    digitalWrite(NY_PIN, !digitalRead(PY_PIN)); //Write NY as opposite of PY
}

void invertPWMZ(){
    digitalWrite(NZ_PIN, !digitalRead(PZ_PIN)); //Write NZ as opposite of PZ
}
