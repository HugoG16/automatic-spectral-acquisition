/*
Can receive a position to move the motor to, or a request to take measurements with an adc.
11/06/2024 
Hugo Gomes
*/

#include <AccelStepper.h>
#include <Wire.h>
#include <MCP342x.h>

#define dirPin 2 
#define stepPin 3 // pwm compatible
#define stopPin 4
#define m0Pin 10
#define m1Pin 9
#define m2Pin 8

// Define commands
#define GOTO    "GOTO"      // Receive - move motor
#define MEAS    "MEAS"      // Receive - take measurement 
#define DONE    "DONE~"     // Send - completed request
#define INVALID "INVALID~"  // Send - invalid request
#define RUNNING "RUNNING~"  // Send - motor is moving
#define STOP    "STOP~"     // Send - stop button was pressed
#define ERROR   "ERROR~"    // Send - error with ADC measurement

// Define stepper properties
#define maxSpeed 300
#define acceleration 50
#define mode0 LOW
#define mode1 HIGH
#define mode2 LOW

// Define global variables
AccelStepper stepper(AccelStepper::DRIVER, stepPin, dirPin);

uint8_t address = 0x68;
MCP342x adc = MCP342x(address);
long measurement = 0;
MCP342x::Config status;

String command;
String prefix;
String value;
int isRunning;
int donePending = 0;       // is the done command waiting to be send?


int isInt(String str) {
  int strLength = str.length();
  if (strLength == 0) {
    return 0;
  }

  for(int i=0; i<strLength; i++) {
    if (str.charAt(i)=='-' && i==0) {
      continue;
    }

    if (!isDigit(str.charAt(i))) {
      return 0;
    }
  }
  return 1;
}


void writeSerial(String text) {
  Serial.print(text);
}


void readSerial() {
  command = Serial.readStringUntil('~');
}


// Performs measurement with ADC
void makeMeasurement(){
  uint8_t err = adc.convertAndRead(MCP342x::channel1, MCP342x::oneShot,
                                  MCP342x::resolution18, MCP342x::gain1,
                                  1000000, measurement, status);
  if (err)
    writeSerial(ERROR);
  else
    writeSerial(String(measurement)+"~");
}


void processCommand() {
  if (isRunning) {
    writeSerial(RUNNING);
    return;
  }

  command.trim(); // remove excess spaces
  prefix = command.substring(0, 4);
  
  if (prefix==GOTO) {
    value = command;
    value.remove(0, 4);
    value.trim();
    
    if (! isInt(value)) {
      writeSerial(INVALID);
      return;
    }

    stepper.moveTo(value.toInt());
    donePending = 1;
  }
  else if (prefix==MEAS) {
    makeMeasurement();
  }
  else {
    writeSerial(INVALID);
    return;
  }
}

void setup() {
  Serial.begin(9600);
  while (!Serial) {delay(10);}

  ////// Motor //////
  pinMode(stopPin, INPUT);

  pinMode(m0Pin, OUTPUT);
  pinMode(m1Pin, OUTPUT);
  pinMode(m2Pin, OUTPUT);

  // chose microstepping mode
  digitalWrite(m0Pin, mode0);
  digitalWrite(m1Pin, mode1);
  digitalWrite(m2Pin, mode2);
  
  stepper.setMaxSpeed(maxSpeed);
  stepper.setAcceleration(acceleration);

  stepper.setCurrentPosition(0);

  ////// ADC //////
  Wire.begin();
  // Reset devices
  MCP342x::generalCallReset();
  delay(1);

  // Check device present
  Wire.requestFrom(address, (uint8_t)1);
  if (!Wire.available()) {
    Serial.print("No device found at address ");
    Serial.println(address, HEX);
    while (1) {delay(10);}
  }
}

void loop() {
  if (digitalRead(stopPin) == HIGH) {
    stepper.stop();
    writeSerial(STOP);
    return;
  } 

  isRunning = stepper.isRunning();

  if (! isRunning && donePending) { // tests if motor has finished moving to position and done command has not been send
    writeSerial(DONE);
    donePending = 0;
  }

  if (Serial.available()) { // if received command
    readSerial();
    processCommand();
  }

  stepper.run();
}
