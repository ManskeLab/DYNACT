#include "ServoEasing.h"
#include <Servo.h>

ServoEasing Servo1;

int pos = 0;
const int SERVO1_PIN = 10;
void setup() {

  Serial.begin(9600);

    // Attach servo to pin
    //Serial.print(F("Attach servo at pin "));
    //Serial.println(SERVO1_PIN);
    if (Servo1.attach(SERVO1_PIN) == INVALID_SERVO) {
        Serial.println(F("Error attaching servo"));
    }

    /**************************************************
     * Set servos to start position.
     * This is the position where the movement starts.
     *************************************************/
    Servo1.write(0);

    // Wait for servo to reach start position.
    delay(500);
  
}

void loop() {
  //Serial.println("hello");
  if(Serial.available() != NULL) {
      int value = Serial.read();
      //Serial.println(value);
      switch (value) {
        case 1:
          rotate(25, 90);
        case 2:
          rotate(45, 90);
        case 3:
          rotate(65, 90);
        default:
          break;
      }
      //delay(100);
  }
}

void rotate(int speed, int angle) {
  while (true) {
    int value = Serial.read();
    Serial.println( value);
    if (value == 'f') {
      return;
    }

    Servo1.setSpeed(speed);
    Servo1.easeTo(angle);
    Servo1.easeTo(0);
    
  }
}
