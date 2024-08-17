/*
Receives a position from the serial port and moves the motor.
11/06/2024 
Hugo Gomes
*/

/*
NOTES
MAYBE THE POSITION SHOULD BE KEPT A INTEGER AND NOT A FLOAT!!!

*/

#include <AccelStepper.h>

#define dirPin 2 
#define stepPin 3 // pwm compatible
#define stopPin 4
#define m0Pin 10
#define m1Pin 9
#define m2Pin 8

// Define commands
#define GOTO    "GOTO"      // Receive
#define DONE    "DONE~"     // Send - completed request
#define INVALID "INVALID~"  // Send - invalid request
#define RUNNING "RUNNING~"  // Send - motor is moving
#define STOP    "STOP~"     // Send - stop button was pressed

// Define stepper properties
#define maxSpeed 300
#define acceleration 50

// Define global variables
AccelStepper stepper(AccelStepper::DRIVER, stepPin, dirPin);
String command;
int isRunning;
int donePending = 0;       // is the done command waiting to be send?

// Function to write to serial
void writeSerial(String text) {
  Serial.print(text);
}

// Function to read from serial and save to variable command
void readSerial() {
  command = Serial.readStringUntil('~');
}

// Function to check if string is a float
int isFloat(String text) { // from https://forum.pjrc.com/index.php?threads/arduino-string-how-to-identify-valid-float.34705/
  int signCount = 0;
  int decPointCount = 0;
  int digitCount = 0;
  int otherCount = 0;
  for (int j=0; j<text.length(); j++) {
    char ch = text.charAt(j);
    if ( j==0 && ( ch=='-' || ch=='+' ) ) signCount++; //leading sign
    else if ( ch>='0' && ch<='9' ) digitCount++; //digit
    else if ( ch=='.' ) decPointCount++; //decimal point
    else otherCount++; //that's bad :(
  }
  if (signCount>1 || decPointCount>1 || digitCount<1 || otherCount>0) {
    return 0;
  }
  return 1;
}

// Function to set the position goal from command
void processCommand() {
  command.trim(); // remove excess spaces

  if (! command.startsWith(GOTO)) {
    writeSerial(INVALID);
    return;
  }

  command.remove(0, 4); // remove "GOTO"
  command.trim(); // remove excess spaces

  if (! isFloat(command)) {
    writeSerial(INVALID);
    return;
  }

  if (isRunning) {
    writeSerial(RUNNING);
    return;
  }

  stepper.moveTo(command.toFloat());
  donePending = 1;
}

void setup() {
  Serial.begin(9600);
  delay(2000); // wait for serial port to connect

  pinMode(stopPin, INPUT);

  pinMode(m0Pin, OUTPUT);
  pinMode(m1Pin, OUTPUT);
  pinMode(m2Pin, OUTPUT);

  // chose microstepping mode
  digitalWrite(m0Pin, LOW);
  digitalWrite(m1Pin, HIGH);
  digitalWrite(m2Pin, LOW);
  
  stepper.setMaxSpeed(maxSpeed);
  stepper.setAcceleration(acceleration);

  stepper.setCurrentPosition(0);

  writeSerial(DONE);
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
