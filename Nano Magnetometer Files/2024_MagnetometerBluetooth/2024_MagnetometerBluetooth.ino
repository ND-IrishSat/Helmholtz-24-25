//Gimbal BLE Transmitter
//authored by Will Stotz for Notre Dame IrishSat, 2024

#include <ArduinoBLE.h>

BLEFloatCharacteristic magnetometerX("fd0f3499-4289-46b1-8ee5-c7781cb46b77", BLERead);
BLEFloatCharacteristic magnetometerY("0bea22dc-8371-4193-8e1a-1c8e46550f3f", BLERead);
BLEFloatCharacteristic magnetometerZ("ab134932-3915-45bd-8366-8ee0ce7535f8", BLERead);

void setup() {
  Serial.begin(9600);

  BLE.begin();

  BLE.setLocalName("Magnetometer");

  BLEService magnetometerService("C6BAA48B-B8CC-B6B7-A520-74167FD37462");

  BLE.setAdvertisedService(magnetometerService);

  magnetometerService.addCharacteristic(magnetometerX);
  magnetometerService.addCharacteristic(magnetometerY);
  magnetometerService.addCharacteristic(magnetometerZ);

  BLE.addService(magnetometerService);

  //encoder1.write(current1);
  //encoder2.write(current2);

  BLE.advertise();

  Serial.println("Bluetooth started.");
}
int x = 0;
void loop() {
  BLEDevice central = BLE.central();  //connected PC

  if (central) {
    Serial.print("Connected to: ");
    Serial.println(central.address());

        magnetometerX.writeValue(unsigned short value));
        magnetometerY.writeValue(2*x);
        magnetometerZ.writeValue(3*x);
        x++;
       delay(350);
      Serial.println(x);
  }
}