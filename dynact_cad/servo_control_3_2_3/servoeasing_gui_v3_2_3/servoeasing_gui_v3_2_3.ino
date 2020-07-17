/* **********************************************************************************************************************************
* SERVO CONTROL GUI V3.2.2
*
* Created By: Kendra Wang
* Created On: 01-03-2020
* 
* Modified By:         Michael Kuczynski
* Modified On:         15-07-2020
* Modification Notes:  -Updated servo starting position
*                      -
* 
* PURPOSE: To control servomotor motion speed and angle
* TO RUN:  Upload this sketch to the Arduino first, then run the corresponding Processing sketch (servo_control_v3_2_2.pde)
* GUI SHORTCUTS:
*    Reset: CTRL 
*    Enter: ENTER / RETURN
*    Switch from speed to angle textfield: TAB
* GUI INSTRUCTIONS:
*    To acutuate or 'turn on' the servo motor, begin by either entering a desired speed and angle into the respective text fields
*       OR press one of the preprogrammed speed buttons and press the 'Enter' button
*    The 'Reset' button stops the servo motor at the end of its cycle and resets the entire GUI to its default setting
*    Once actuated, the servomotor will rotate continously until the Reset button is pressed
*    The user must press the Reset button before switching speed/angle settings
* NOTES:
*    Printing to the serial monitor from Arduino while the Processing sketch is running can cause serial miscommunication
************************************************************************************************************************************/ 

#include "ServoEasing.h"

// Create servo object
ServoEasing servo;

int position = 0;
int speed = 0;
int angle = 0;
int status = 0;

const int SERVO_PIN = 10;


/*
*
*
*
*/
void setup() 
{
  // Set the baud rate. Add delay to give time for connection.
  Serial.begin( 9600 );

  // Attach servo to pin #9 on the Arduino (can only use pin #9 or #10 for PWM).
  Serial.print( F("Attempting to connect to pin #") );
  Serial.print( SERVO_PIN );
  Serial.println();

  if ( servo.attach(SERVO_PIN) == INVALID_SERVO ) 
  {
    Serial.println( F("Error: Cannot attach servo!") );
  }

  Serial.print( F("Successfully connected to pin #") );
  Serial.print( SERVO_PIN );
  Serial.println();

  // Set servo to start position.
  servo.write(0);
  delay(500);
}

void loop() 
{
//  Serial.print( "HELLO" );
//  delay(15);
  // for (position = 0; position <= 90; position += 1) 
  // { 
  //   // goes from 0 degrees to 180 degrees
  //   // in steps of 1 degree
  //   servo.write(position);              // tell servo to go to position in variable 'pos'
  //   delay(15);                       // waits 15ms for the servo to reach the position
  // }
  // for (position = 90; position >= 0; position -= 1) 
  // { 
  //   // goes from 180 degrees to 0 degrees
  //   servo.write(position);              // tell servo to go to position in variable 'pos'
  //   delay(15);                       // waits 15ms for the servo to reach the position
  // }



  while(Serial.available()) 
  {
    String input = read();
    status = checkStatus(input); // check what setting (Speed1, Speed2, Speed3, Custom speed & angle, or reset) Processing is sending through the serial port
    //Serial.println(stat);
    
    switch (status) 
    {
      case 0: // Custom speed & angle mode
        speed = getSpeed(input);
        angle = getAngle(input);
        rotate(speed, angle);
        break;
      case 1: // Speed1 mode
        rotate(30, 90);
        break;
      case 2: // Speed2 mode
        rotate(45, 90);
        break;
      case 3: // Speed3 mode
        rotate(60, 90);
        break;
      case 4: // Reset mode
        break;
      case 5: // Stop at current position
        // speed = 0;
        // angle = 
        break;
      default:
        break;
    }
  }  
}

int checkStatus(String str) 
{
  if (str[0] == '0' && str[1] == '0' && str[2] == '0' && str[3] == '0' && str[4] == '0') 
  { 
    // check if first 5 characters are zeroes
    return str[5] - '0'; // Convert char to int and return the 6th character which designates if Speed1, 2, 3, or reset has been selected
  }
      
  else 
  {
    return 0; // 0 designates that a custom speed & angle has been enter
  }     
}

String read() 
{ 
  // Receive and process data from serial port 
  if (!Serial.available()); //wait for user input
  //there is something in the buffer now
  
  char str[6]; // Make string to store data in
  int index = 0;
  while (Serial.available()) 
  {
    if (index == 6) 
    {
      str[index] = '\0'; // null terminate string
      break; 
    }

    str[index] = Serial.read();

    delay(2); //wait for the next byte, if after this nothing has arrived it means the text was not part of the same stream entered by the user

    index++;
  }
  //Serial.println(str);
  return str;
}

int getSpeed(String original) 
{ 
  // Split input string into speed portion and convert to int
  return (original.substring(0,3).toInt());
}


int getAngle(String original)
{ 
  // Split input string into angle portion and convert to int
  return (original.substring(3,7).toInt());
}

void rotate(int speed, int angle) 
{ 
  // Rotate servo at specified speed and to specified angle
  int value = 0;
  
  while (value != 4) 
  { 
    // if value == 4 then reset has been pressed
    servo.setSpeed(speed);
    servo.easeTo(angle);
    servo.easeTo(0);

    value = checkStatus(read()); // update value to see if reset button has been pressed
  }
}
