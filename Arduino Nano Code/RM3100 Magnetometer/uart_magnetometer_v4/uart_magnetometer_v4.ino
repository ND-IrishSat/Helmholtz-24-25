// connects arduino nano via uart to rpi

// SOURCE https://github.com/hnguy169/RM3100-Arduino

// CONNECTIONS

// chip -> arduino
// vcc -> 3.3v
// 2 x gnd -> 2 x gnd
// DRDY -> D9
// SSN -> D10 
// MISO -> D12 (MISO)
// MOSI -> D11 (MOSI)
// CLK -> D13


#include <Arduino.h>
#include <SPI.h>

//pin definitions
#define PIN_DRDY 9 //Set pin D9 to be the Data Ready Pin
#define PIN_CS 10 //Chip Select (SS) is set to Pin 10

//internal register values without the R/W bit
#define RM3100_REVID_REG 0x36 // Hexadecimal address for the Revid internal register
#define RM3100_POLL_REG 0x00 // Hexadecimal address for the Poll internal register
#define RM3100_CMM_REG 0x01 // Hexadecimal address for the Continuous Measurement Mode internal register
#define RM3100_STATUS_REG 0x34 // Hexadecimal address for the Status internal register
#define RM3100_CCX1_REG 0x04 // Hexadecimal address for the Cycle Count X1 internal register
#define RM3100_CCX0_REG 0x05 // Hexadecimal address for the Cycle Count X0 internal register

//options
#define initialCC 100 // Set the cycle count
#define singleMode 0 //0 = use continuous measurement mode; 1 = use single measurement mode
#define useDRDYPin 1 //0 = not using DRDYPin ; 1 = using DRDYPin to wait for data


// Hard-iron calibration settings
const float hard_iron[3] = {
    2.0485,    0.9343,    0.3828
};
// Soft-iron calibration settings
const float soft_iron[3][3] = {
  { 0.9874,   -0.0073,   -0.0266},
  {-0.0073,    1.0336,    0.0080},
  {-0.0266,    0.0080,    0.9806}
};


uint8_t revid;
uint16_t cycleCount;
float gain;

void setup() {
  pinMode(PIN_DRDY, INPUT);  
  pinMode(PIN_CS, OUTPUT);
  digitalWrite(PIN_CS, HIGH);
  SPI.begin(); // Initiate the SPI library
  SPI.beginTransaction(SPISettings(1000000, MSBFIRST, SPI_MODE0));  

  Serial.begin(115200);
  // while(true) {
  //   if (Serial.available()) {
  //       String command = Serial.readStringUntil('\n');
  //       if (command == "IDENTIFY") {
  //           Serial.println("NANO");
  //           break;
  //       }
  //   }
  // }  
  
  delay(100);

  revid = readReg(RM3100_REVID_REG);
  
  Serial.print("REVID ID = 0x"); //REVID ID should be 0x22
  Serial.println(revid, HEX);

  changeCycleCount(initialCC); //change the cycle count; default = 200 (lower cycle count = higher data rates but lower resolution)

  cycleCount = readReg(RM3100_CCX1_REG);
  cycleCount = (cycleCount << 8) | readReg(RM3100_CCX0_REG);

  Serial.print("Cycle Counts = "); //display cycle count
  Serial.println(cycleCount);

  gain = 38; //(0.3671 * (float)cycleCount) + 1.5; //linear equation to calculate the gain from cycle count

  Serial.print("Gain = "); //display gain; default gain should be around 75 for the default cycle count of 200
  Serial.println(gain);

  if (singleMode){
    //set up single measurement mode
    writeReg(RM3100_CMM_REG, 0);
    writeReg(RM3100_POLL_REG, 0x70);
  }
  else{
    // Enable transmission to take continuous measurement with Alarm functions off
    writeReg(RM3100_CMM_REG, 0x79);
  }

 writeReg(0x0B, 0x93);

  digitalWrite(PIN_CS, LOW);
}

void loop() {
  long x = 0;
  long y = 0;
  long z = 0;
  uint8_t x2,x1,x0,y2,y1,y0,z2,z1,z0;

  // Mag Data Array {x, y , z}
  float magData[3] = {0, 0, 0};
  // float xMag = 0;
  // float yMag = 0;
  // float zMag = 0;

  //wait until data is ready using 1 of two methods (chosen in options at top of code)
  if(useDRDYPin){ 
    while(digitalRead(PIN_DRDY) == LOW); //check RDRY pin
  }
  else{
    while((readReg(RM3100_STATUS_REG) & 0x80) != 0x80); //read internal status register
  }
  
  //read measurements
  digitalWrite(PIN_CS, LOW);
  delay(0.0001);
  SPI.transfer(0xA4);
  x2 = SPI.transfer(0xA5);
  x1 = SPI.transfer(0xA6);
  x0 = SPI.transfer(0xA7);
  
  y2 = SPI.transfer(0xA8);
  y1 = SPI.transfer(0xA9);
  y0 = SPI.transfer(0xAA);
  
  z2 = SPI.transfer(0xAB);
  z1 = SPI.transfer(0xAC);
  z0 = SPI.transfer(0);
  
  digitalWrite(PIN_CS, HIGH);

  //special bit manipulation since there is not a 24 bit signed int data type
  if (x2 & 0x80){
      x = 0xFF;
  }
  if (y2 & 0x80){
      y = 0xFF;
  }
  if (z2 & 0x80){
      z = 0xFF;
  }

  //format results into single 32 bit signed value
  x = (x * 256 * 256 * 256) | (int32_t)(x2) * 256 * 256 | (uint16_t)(x1) * 256 | x0;
  y = (y * 256 * 256 * 256) | (int32_t)(y2) * 256 * 256 | (uint16_t)(y1) * 256 | y0;
  z = (z * 256 * 256 * 256) | (int32_t)(z2) * 256 * 256 | (uint16_t)(z1) * 256 | z0;

  //calculate magnitude of results
  //double uT = sqrt(pow(((float)(x)/gain),2) + pow(((float)(y)/gain),2)+ pow(((float)(z)/gain),2));

  magData[0] = (float)(x)/gain;
  magData[1] = (float)(y)/gain;
  magData[2] = (float)(z)/gain; 

  float normData[3];

  // Perform calibration
  //magCalFunc(magData, normData);

  Serial.print(magData[0]);
  Serial.print(" ");
  Serial.print(magData[1]);
  Serial.print(" ");
  Serial.println(magData[2]);

}

//addr is the 7 bit value of the register's address (without the R/W bit)
uint8_t readReg(uint8_t addr){

  uint8_t data = 0;
  digitalWrite(PIN_CS, LOW);
  delay(2);
  SPI.transfer(addr | 0x80); //OR with 0x80 to make first bit(read/write bit) high for read
  data = SPI.transfer(0);
  digitalWrite(PIN_CS, HIGH);
  return data;
}

//addr is the 7 bit (No r/w bit) value of the internal register's address, data is 8 bit data being written
void writeReg(uint8_t addr, uint8_t data){

  digitalWrite(PIN_CS, LOW); 
  
  SPI.transfer(addr & 0x7F); //AND with 0x7F to make first bit(read/write bit) low for write
  SPI.transfer(data);
  digitalWrite(PIN_CS, HIGH);
}

//newCC is the new cycle count value (16 bits) to change the data acquisition
void changeCycleCount(uint16_t newCC){

  uint8_t CCMSB = (newCC & 0xFF00) >> 8; //get the most significant byte
  uint8_t CCLSB = newCC & 0xFF; //get the least significant byte
    
  digitalWrite(PIN_CS, LOW); 
  delay(2);
  SPI.transfer(RM3100_CCX1_REG & 0x7F); //AND with 0x7F to make first bit(read/write bit) low for write
  SPI.transfer(CCMSB);  //write new cycle count to ccx1
  SPI.transfer(CCLSB);  //write new cycle count to ccx0
  SPI.transfer(CCMSB);  //write new cycle count to ccy1
  SPI.transfer(CCLSB);  //write new cycle count to ccy0
  SPI.transfer(CCMSB);  //write new cycle count to ccz1
  SPI.transfer(CCLSB);  //write new cycle count to ccz0

  digitalWrite(PIN_CS, HIGH);
}

// Calibration Function
void magCalFunc(const float mag_data[3], float normData[3]) {
    float hi_cal[3];

    // Apply hard-iron offsets
    for (int i = 0; i < 3; i++) {
        hi_cal[i] = mag_data[i] - hard_iron[i];
    }

    // Apply soft-iron scaling
    for (int i = 0; i < 3; i++) {
        normData[i] = (soft_iron[i][0] * hi_cal[0]) + 
                      (soft_iron[i][1] * hi_cal[1]) + 
                      (soft_iron[i][2] * hi_cal[2]);
    }
}


