/* SERVO CONTROL GUI V3.2.2
 * 2020-02-18   Written by Kendra Wang to power a servo motor continuously 
 *              and control the angle to which it moves and the speed at which it moves at.
 *
 * TO RUN: 
 *  - Upload the corresponding Arduino sketch (servoeasing_gui_v3_2_2.ino) first, and then run this sketch
 * KEYBOARD SHORTCUTS:
 *  - Reset: CTRL 
 *  - Enter: ENTER / RETURN
 *  - Switch from speed to angle textfield: TAB
 *  - Clear: SHIFT
 * GUI INSTRUCTIONS:
 *  - To acutuate or 'turn on' the servo motor, begin by either entering a desired speed and angle into the respective text fields
 *       OR press one of the preprogrammed speed buttons and press the 'Enter' button
 *  - The 'Reset' button stops the servo motor at the end of its cycle and resets the entire GUI to its default setting
 *  - Once actuated, the servomotor will rotate continously until the Reset button is pressed
 *  - The user must press the Reset button before switching speed/angle settings
 * NOTES:
 *  - Printing to the serial monitor from Arduino while the Processing sketch is running can cause serial miscommunication
 */


import controlP5.*; //import ControlP5 library
import processing.serial.*;

Serial port;

ControlP5 cp5; //create ControlP5 object
PFont font, font2, font3;
String inputSpeed = "";
String inputAngle = "";
String inputPos = "";
String val;
int intSpeed = 0;
int intAngle = 0;
String outputSpeed = "";
String outputAngle = "";
String outputPos = "";

void setup(){
  
  size (500,350); // window size, (width, height)
  
  printArray(Serial.list()); // prints all available serial ports
  
  port = new Serial(this,  Serial.list()[2], 9600); // Open the port that the Arduino board is connected to (in this case #1)
                                                    // Make sure to open the port at the same speed the Arduino is using (9600 bps)
  
  cp5 = new ControlP5(this);
  font = createFont("Avenir-Book", 20); // custom fonts for buttons and title
  font2 = createFont("DINCondensed-Bold", 16, true); // custom fonts for buttons and title
  font3 = createFont("Avenir-Book", 12, true); // custom fonts for buttons and title
  
  //print(PFont.list());

  // Create controllers
  
  cp5.addTextfield("speedInput") // create Textfield for entering speed
    .setPosition(125, 80) // x and y coords of upper left corner of button
    .setSize(100, 30) // size of Textfield
    .setFont(font3)
    .setColorBackground(0xFFFFFFFF)
    .setColorValue(0x000000)
    .setFocus(false)
    ;
  
  cp5.addTextlabel("label") // label for speedInput Textfield
    .setText("SPEED")
    .setPosition(175, 88)
    .setFont(font3)
    .setColorValue(0x000000)
    ;
  
  cp5.addTextfield("angleInput") // create Textfield for entering angle
    .setPosition(125, 130) // x and y coords of upper left corner of button
    .setSize(100, 30) // size of Textfield
    .setFont(font3)
    .setColorBackground(0xFFFFFFFF)
    .setColorValue(0x000000)
    .setFocus(false)
    ;
  
  cp5.addTextlabel("label2") // label for angleInput Textfield
    .setText("ANGLE")
    .setPosition(175, 138)
    .setFont(font3)
    .setColorValue(0x000000)
    ;
     
  cp5.addButton("Speed1") // create Speed1 button
    .setPosition(50, 190) // x and y coords of upper left corner of button
    .setSize(130, 40)
    .setFont(font3)
    ;
    
  cp5.addButton("Speed2") // create Speed2 button
    .setPosition(190, 190) // x and y coords of upper left corner of button
    .setSize(130, 40)
    .setFont(font3)
    ;
    
  cp5.addButton("Speed3") // create Speed3 button
    .setPosition(330, 190) // x and y coords of upper left corner of button
    .setSize(130, 40)
    .setFont(font3)
    ;
  
  cp5.addButton("Enter") // create Enter button
    .setPosition(240, 80) // x and y coords of upper left corner of button
    .setSize(150, 30)
    .setFont(font3)
    .setColorBackground(0xff00ace6)
    ;
  
  cp5.addButton("Clear") // create Clear button
    .setPosition(320, 130) // x and y coords of upper left corner of button
    .setSize(70, 30)
    .setFont(font3)
    ;
  
  cp5.addButton("Reset") // create Reset button
    .setPosition(240, 130) // x and y coords of upper left corner of button
    .setSize(70, 30)
    .setFont(font3)
    ;
    
  cp5.addTextlabel("speedWarning") // create label for handling unwanted speed inputs
    .setText("Please enter a speed" + '\n' + "of 3 or less digits.")
    .setPosition(5, 80)
    .setColorValue(0xff00ace6)
    .setVisible(false)
    ;
    
  cp5.addTextlabel("angleWarning") // create label for handling unwanted angle inputs
    .setText("Please enter an angle" + '\n' + "between 0 and 180" + '\n' + "degrees.")
    .setPosition(5, 125)
    .setColorValue(0xff00ace6)
    .setVisible(false)
    ;
  
  cp5.addTextlabel("charWarning") // create label for handling non-numerical inputs 
    .setText("Please enter" + '\n' + "numbers only.")
    .setPosition(400, 110)
    .setColorValue(0xff00ace6)
    .setVisible(false)
    ;

}

// ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

void draw(){
  background (255, 255, 255); // background of window (r,g,b) or (0 to 255)
  fill(74, 74, 74); // text color (r,g,b)
  textFont(font);
  text("SERVO CONTROL 3.2.3", 250, 50); //window title ("text", x coord, y xoord)
  textAlign(CENTER);
  
  // For printing from the Arduino
  if ( port.available() > 0) 
  {  // If data is available,
   val = port.readStringUntil('\n');         // read it and store it in val
  } 
  //println(val); //print it out in the console
  
}

// ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

void Speed1() { // when the Speed1 button is pressed, this method is called
  hideWarnings(); // hide warnings (refresh after another button has been pressed)
  
  port.clear();
  port.write("000001"); // tell Arduino that Speed1 has been selected
  //println("speed1 pressed");
  
}

// ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

void Speed2() { // when the Speed2 button is pressed, this method is called
  hideWarnings(); // hide warnings (refresh after another button has been pressed)
  
  port.clear();
  port.write("000002"); // tell Arduino that Speed2 has been selected
  //println("speed2 pressed");
}

// ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

void Speed3() { // when the Speed3 button is pressed, this method is called
  hideWarnings(); // hide warnings (refresh after another button has been pressed)
  
  port.clear();
  port.write("000003"); // tell Arduino that Speed3 has been selected
  //println("speed3 pressed");
}

// ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

void Reset() {
  hideWarnings(); // hide warnings (refresh after another button has been pressed)
  
  port.clear();
  
  
  port.write("000004"); // tell Arduino to reset
  //println("Reset pressed");
}

// ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

void Clear() {
  hideWarnings();
  
  port.clear();
  
  cp5.get(Textfield.class, "speedInput").clear(); // clear textfields
  cp5.get(Textfield.class, "angleInput").clear();
  
  cp5.get(Textfield.class, "speedInput").setFocus(true);
  cp5.get(Textfield.class, "angleInput").setFocus(false);
}

// ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

void Enter() {
  hideWarnings(); // hide warnings (refresh after another button has been pressed)
  cp5.get(Textfield.class, "speedInput").setFocus(true);
  cp5.get(Textfield.class, "angleInput").setFocus(false);
  
  port.clear();
  
  /*
    int dec = int(cp5.get(Textfield.class,"speedInput").getText());
    int ascii1 = dec + '0'; // convert from decimal to ascii
    port.write( ascii + ascii2);
  */
  
  inputSpeed = cp5.get(Textfield.class,"speedInput").getText();
  
  inputAngle = cp5.get(Textfield.class,"angleInput").getText();
 
  
  if (inputSpeed.length() <= 3 && inputSpeed.length() > 0) { // check if speed input contains 1 to 3 characters
    
    if (inputSpeed.matches("[0-9]+")) { // check if input contains digits only
      //println("numbers only");
      intSpeed = Integer.parseInt(inputSpeed);
      outputSpeed = nf(intSpeed, 3);
    }
    
    else {
      //println("not only numbers");
      cp5.get(Textlabel.class, "charWarning").setVisible(true);
    }
  }
  
  else { // if (inputSpeed.length() > 3) and other cases
    cp5.get(Textlabel.class, "speedWarning").setVisible(true);
  }
  
  if (inputAngle.length() <= 3 && inputAngle.length() > 0) { // check if angle input contains 1 to 3 characters
  
    if (inputAngle.matches("[0-9]+")) { // check if input contains digits only
      //println("numbers only");
      intAngle = Integer.parseInt(inputAngle);
      outputAngle = nf(intAngle, 3);
      
      println("outputSpeed: " + outputSpeed + " outputAngle: " + outputAngle);
      port.write(outputSpeed + outputAngle);
    }
    
    else {
      cp5.get(Textlabel.class, "charWarning").setVisible(true);
      //println("not only numbers");
    }
    
  }
  
  else { // if (inputAngle.length() > 3) and other cases
    cp5.get(Textlabel.class, "angleWarning").setVisible(true);
  }
  
}

// ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

void hideWarnings() {
  
  cp5.get(Textlabel.class, "speedWarning").setVisible(false);
  cp5.get(Textlabel.class, "angleWarning").setVisible(false);
  cp5.get(Textlabel.class, "charWarning").setVisible(false);
  
}

// ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

void keyPressed () {
  
  if (keyCode == ENTER || keyCode == RETURN) {
    Enter();
  }
  if (keyCode == CONTROL) {
    Reset();
  }
  
  if (keyCode == TAB) {
    cp5.get(Textfield.class, "speedInput").setFocus(false);
    cp5.get(Textfield.class, "angleInput").setFocus(true);
  }
  if (keyCode == SHIFT) {
    Clear();
  }
  
}
