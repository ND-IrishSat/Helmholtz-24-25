//Gimbal BLE Transmitter
//authored by Will Stotz for Notre Dame IrishSat, 2024

#include <ArduinoBLE.h>


#define ENCODER_1 2
#define ENCODER_2 4

BLEByteCharacteristic encoder1("fd0f3499-4289-46b1-8ee5-c7781cb46b77", BLERead);
BLEByteCharacteristic encoder2("11a6ddf2-12e4-4804-a75e-6f0185a59326", BLERead);

void setup() {
  Serial.begin(9600);
  while (!Serial);

  //setup pins
  pinMode(ENCODER_1, INPUT);
  pinMode(ENCODER_2, INPUT);

  BLE.begin();

  BLE.setLocalName("IrishSat Gimbal Encoder");

  BLEService encoderService("a3d43078-59e6-4136-b98b-66ca6fda6dd3");

  BLE.setAdvertisedService(encoderService);

  encoderService.addCharacteristic(encoder1);
  encoderService.addCharacteristic(encoder2);

  BLE.addService(encoderService);

  //encoder1.write(current1);
  //encoder2.write(current2);

  BLE.advertise();

  Serial.println("Bluetooth started.");
}

void loop() {
  BLEDevice central = BLE.central();  //connected PC
  if (central) {
    Serial.print("Connected to: ");
    Serial.println(central.address());

    bool pin1 = digitalRead(ENCODER_1);
    bool pin2 = digitalRead(ENCODER_2);
    while (central.connected()) {
      bool newPin1 = digitalRead(ENCODER_1);
      bool newPin2 = digitalRead(ENCODER_2);
      if (pin1 != newPin1) {
        encoder1.writeValue(newPin1);
        Serial.print("Encoder 1 state change: ");
        Serial.println(newPin1);
      }
      if (pin2 != newPin2) {
        encoder2.writeValue(newPin2);
        Serial.print("Encoder 2 state change: ");
        Serial.println(newPin2);
      }
      pin1 = newPin1;
      pin2 = newPin2;
    }
  }
}