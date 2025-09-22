#include <Servo.h>
Servo servo1;
Servo servo2;
const int servo1Pin = 9;
const int servo2Pin = 10;
const int servoStep = 20;
const int motor1In1 = 7;
const int motor1In2 = 6;
const int motor1Ena = 5;
const int movementSpeed = 255;
const int motor2In3 = 8;
const int motor2In4 = 12;
const int motor2Enb = 11;
const int motor3In1 = 4;
const int motor3In2 = 2;
const int motor3Ena = 3;
const int armSpeed = 255; 
const int motor4In1 = 14; // A0
const int motor4In2 = 15; // A1
const int motor4Ena = 16; // A2
const int clawSpeed = 255;
int servo1Pos = 90;
int servo2Pos = 90;

void setup() {
  servo1.attach(servo1Pin);
  servo2.attach(servo2Pin);
  Serial.begin(9600);
  servo1.write(servo1Pos);
  servo2.write(servo2Pos);

  pinMode(motor1In1, OUTPUT);
  pinMode(motor1In2, OUTPUT);
  pinMode(motor1Ena, OUTPUT);
  pinMode(motor2In3, OUTPUT);
  pinMode(motor2In4, OUTPUT);
  pinMode(motor2Enb, OUTPUT);
  pinMode(motor3In1, OUTPUT);
  pinMode(motor3In2, OUTPUT);
  pinMode(motor3Ena, OUTPUT);
  pinMode(motor4In1, OUTPUT);
  pinMode(motor4In2, OUTPUT);
  pinMode(motor4Ena, OUTPUT);
  
  stopAllMotors();
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();

    if (command == 'h') {
      servo1Pos -= servoStep;
      if (servo1Pos < 0) servo1Pos = 0;
      servo1.write(servo1Pos);
    } else if (command == 'k') {
      servo1Pos += servoStep;
      if (servo1Pos > 180) servo1Pos = 180;
      servo1.write(servo1Pos);
    } else if (command == 'u') {
      servo2Pos += servoStep;
      if (servo2Pos > 180) servo2Pos = 180;
      servo2.write(servo2Pos);
    } else if (command == 'j') {
      servo2Pos -= servoStep;
      if (servo2Pos < 0) servo2Pos = 0;
      servo2.write(servo2Pos);
    } else if (command == 'w') {
      moveForward();
    } else if (command == 's') {
      moveBackward();
    } else if (command == 'a') {
      armForward(); 
    } else if (command == 'd') {
      armBackward();
    } else if (command == 'z') {
      clawForward();
    } else if (command == 'x') {
      clawBackward();
    } else if (command == 'q') {
      stopAllMotors();
    }
    
    while (Serial.available()) {
      Serial.read();
    }
  }
}

void moveForward() {
  digitalWrite(motor1In1, HIGH);
  digitalWrite(motor1In2, LOW);
  analogWrite(motor1Ena, movementSpeed);
  
  digitalWrite(motor2In3, HIGH);
  digitalWrite(motor2In4, LOW);
  analogWrite(motor2Enb, movementSpeed);
}

void moveBackward() {
  digitalWrite(motor1In1, LOW);
  digitalWrite(motor1In2, HIGH);
  analogWrite(motor1Ena, movementSpeed);
  
  digitalWrite(motor2In3, LOW);
  digitalWrite(motor2In4, HIGH);
  analogWrite(motor2Enb, movementSpeed);
}

void armForward() {
  digitalWrite(motor3In1, HIGH);
  digitalWrite(motor3In2, LOW);
  analogWrite(motor3Ena, armSpeed);
}

void armBackward() {
  digitalWrite(motor3In1, LOW);
  digitalWrite(motor3In2, HIGH);
  analogWrite(motor3Ena, armSpeed);
}

void clawForward() {
  digitalWrite(motor4In1, HIGH);
  digitalWrite(motor4In2, LOW);
  analogWrite(motor4Ena, clawSpeed);
}

void clawBackward() {
  digitalWrite(motor4In1, LOW);
  digitalWrite(motor4In2, HIGH);
  analogWrite(motor4Ena, clawSpeed);
}

void stopAllMotors() {
  analogWrite(motor1Ena, 0);
  analogWrite(motor2Enb, 0);
  analogWrite(motor3Ena, 0);
  analogWrite(motor4Ena, 0);
}