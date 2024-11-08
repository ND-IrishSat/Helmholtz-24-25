#include "pwm.h" // arduino pwm library

// pin definitions for each h-bridge
#define x1 3
#define x2 5

#define y1 6
#define y2 9

#define z1 10
#define z2 11

// instantiate pwm objects at each pin
PwmOut xBridge1(x1);
PwmOut xBridge2(x2);

PwmOut yBridge1(y1);
PwmOut yBridge2(y2);

PwmOut zBridge1(z1);
PwmOut zBridge2(z2);

float x_1, x_2, y_1, y_2, z_1, z_2;

// String data="";

void setup() {
  Serial.begin(9600);
  
  // if (Serial.available() > 0) {
  //   String data = Serial.readStringUntil('\n');
  //   parseValues(data, x_1, x_2, y_1, y_2, z_1, z_2);
  // }
  
  // period in microseconds, starting pulse in microseconds
  xBridge1.begin(200, 0.0, false);
  xBridge2.begin(200, 0.0, false);

  yBridge1.begin(200, 0.0, false);
  yBridge2.begin(200, 0.0, false);

  zBridge1.begin(200, 0.0, false);
  zBridge2.begin(200, 0.0, false);

  // duty cycle percentage 
  xBridge1.pulse_perc(0);
  xBridge2.pulse_perc(0);

  yBridge1.pulse_perc(0);
  yBridge2.pulse_perc(0);

  zBridge1.pulse_perc(0);
  zBridge2.pulse_perc(0);
}

void loop() {
  // There is no war in ba sing se

  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    parseValues(data, x_1, x_2, y_1, y_2, z_1, z_2);
    Serial.println(data);
  }
  
  // duty cycle percentage 
  xBridge1.pulse_perc(x_1);
  xBridge2.pulse_perc(x_2);

  yBridge1.pulse_perc(y_1);
  yBridge2.pulse_perc(y_2);

  zBridge1.pulse_perc(z_1);
  zBridge2.pulse_perc(z_2);
}

void parseValues(String input, float &x_1, float &x_2, float &y_1, float &y_2, float &z_1, float &z_2) {
  int startIdx = 0;  // Starting index for each substring
  int spaceIdx;      // Index of the next space

  // Find and convert each value
  spaceIdx = input.indexOf(' ', startIdx);
  x_1 = input.substring(startIdx, spaceIdx).toFloat();

  startIdx = spaceIdx + 1;
  spaceIdx = input.indexOf(' ', startIdx);
  x_2 = input.substring(startIdx, spaceIdx).toFloat();

  startIdx = spaceIdx + 1;
  spaceIdx = input.indexOf(' ', startIdx);
  y_1 = input.substring(startIdx, spaceIdx).toFloat();

  startIdx = spaceIdx + 1;
  spaceIdx = input.indexOf(' ', startIdx);
  y_2 = input.substring(startIdx, spaceIdx).toFloat();

  startIdx = spaceIdx + 1;
  spaceIdx = input.indexOf(' ', startIdx);
  z_1 = input.substring(startIdx, spaceIdx).toFloat();

  startIdx = spaceIdx + 1;
  z_2 = input.substring(startIdx).toFloat();
}
