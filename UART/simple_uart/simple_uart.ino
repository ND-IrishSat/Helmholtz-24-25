long unsigned int count = 0;

void setup() {
  // Start the serial communication at 9600 baud rate
  Serial.begin(9600);
}

void loop() {
  // Send a message over the serial port every second
  Serial.println(count);
  count++;
  delay(10);  // Wait for 1 second before sending the next message
}