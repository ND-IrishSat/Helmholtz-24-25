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

void setup() {
  
  // period in microseconds, starting pulse in microseconds
  xBridge1.begin(200, 0.0);
  xBridge2.begin(200, 0.0);

  yBridge1.begin(200, 0.0);
  yBridge2.begin(200, 0.0);

  zBridge1.begin(200, 0.0);
  zBridge2.begin(200, 0.0);

  // duty cycle percentage 
  xBridge1.pulse_perc(100);
  xBridge2.pulse_perc(0);

  yBridge1.pulse_perc(50);
  yBridge2.pulse_perc(0);

  zBridge1.pulse_perc(0);
  zBridge2.pulse_perc(100);


}

void loop() {
  

}
