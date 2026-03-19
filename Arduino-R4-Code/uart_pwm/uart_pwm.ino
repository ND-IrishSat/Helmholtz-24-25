#include "pwm.h" // Arduino PWM library

// Pin definitions for each H-bridge
#define x1 3
#define x2 5

#define y1 6
#define y2 9

#define z1 10
#define z2 11

// Instantiate PWM objects at each pin
PwmOut xBridge1(x1);
PwmOut xBridge2(x2);

PwmOut yBridge1(y1);
PwmOut yBridge2(y2);

PwmOut zBridge1(z1);
PwmOut zBridge2(z2);

float x_1 = 0, x_2 = 0, y_1 = 0, y_2 = 0, z_1 = 0, z_2 = 0, freqX = 0, freqY = 0, freqZ = 0;
float prevFreqX = 800;
float prevFreqY = 800;
float prevFreqZ = 800;
String incomingData = "";  // Buffer for serial data

void setup() {
  Serial.begin(9600);
  // while(true) {
  //   if (Serial.available()) {
  //       String command = Serial.readStringUntil('\n');
  //       if (command == "IDENTIFY") {
  //           Serial.println("R4");
  //           break;
  //       }
  //   }
  // }

  // Set PWM period and initial duty cycle for each bridge
  // period in microsecond
  xBridge1.begin(800, 0.0);
  xBridge2.begin(800, 0.0);


  yBridge1.begin(800, 0.0);
  yBridge2.begin(800, 0.0);

  zBridge1.begin(800, 0.0);
  zBridge2.begin(800, 0.0);

  xBridge1.pulse_perc(0);
  xBridge2.pulse_perc(0.0);

  yBridge1.pulse_perc(0);
  yBridge2.pulse_perc(0.0);

  zBridge1.pulse_perc(0);
  zBridge2.pulse_perc(0.0);

}

void loop() {
  // Non-blocking serial data reading
  while (Serial.available() > 0) {
    char receivedChar = Serial.read();
    if (receivedChar == '\n') {
      // When newline is received, process the buffer
      if (parseValues(incomingData, x_1, x_2, y_1, y_2, z_1, z_2, freqX, freqY, freqZ)) {
        updatePwmDutyCycles();
        Serial.println("Data received and applied: " + incomingData);  // Optional feedback
      } else {
        //Serial.println("Error: Incorrect data format.");
      }
      incomingData = "";  // Clear the buffer
    } else {
      incomingData += receivedChar;  // Append to buffer
    }
  }

}

// Helper function to initialize PWM with a fixed period and 0% duty cycle
void initializePwm(PwmOut &pwm) {
  pwm.begin(200, 0.0, false);
  pwm.pulse_perc(0);
}

// Function to update PWM duty cycles for each H-bridge
void updatePwmDutyCycles() {
  xBridge1.pulse_perc(x_1);
  xBridge2.pulse_perc(x_2);
  yBridge1.pulse_perc(y_1);
  yBridge2.pulse_perc(y_2);
  zBridge1.pulse_perc(z_1);
  zBridge2.pulse_perc(z_2);

    xBridge1.period_us(freqX);
    xBridge2.period_us(freqX);
   
    prevFreqX = freqX;


  if(freqY != prevFreqY){
    yBridge1.period_us(freqY);
    yBridge2.period_us(freqY);
    
    prevFreqY = freqY;
  }

  if(freqZ != prevFreqZ){
    zBridge1.period_us(freqZ);
    zBridge2.period_us(freqZ);
   
    prevFreqZ = freqZ;
  }

}

// Parses space-separated values and assigns them to each variable
bool parseValues(String input, float &x_1, float &x_2, float &y_1, float &y_2, float &z_1, float &z_2, float &freqX, float &freqY, float &freqZ) {
  int startIdx = 0;
  int spaceIdx;
  float values[9];
  
  for (int i = 0; i < 9; i++) {
    spaceIdx = input.indexOf(' ', startIdx);
    if (spaceIdx == -1 && i < 8) return false;  
    
    String valueStr = (i < 8) ? input.substring(startIdx, spaceIdx) : input.substring(startIdx);
    values[i] = valueStr.toFloat();
    
    startIdx = spaceIdx + 1;
  }

  x_1 = values[0];
  x_2 = values[1];
  y_1 = values[2];
  y_2 = values[3];
  z_1 = values[4];
  z_2 = values[5];
  freqX = values[6];
  freqY = values[7];
  freqZ = values[8];
  
  return true;
}
