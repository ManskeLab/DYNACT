import controlP5.*; //import ControlP5 library
import processing.serial.*;

Serial port;

ControlP5 cp5; //create ControlP5 object
PFont font;

void setup(){
  
  size (500,400); //window size, (width, height)
  
  printArray(Serial.list()); //prints all available serial ports
  
  port = new Serial(this,  Serial.list()[1], 9600); // Open the port that the Arduino board is connected to (in this case #1)
                                                    // Make sure to open the port at the same speed the Arduino is using (9600 bps)
  
  // add button to empty window
  cp5 = new ControlP5(this);
  font = createFont("HelveticaNeue-Light", 20); // custom fonts for buttons and title

  cp5.addButton("Speed1") // name of the button
    .setPosition(60, 100) // x and y coords of upper left corner of button
    .setSize(120, 80)
    .setFont(font)
    ;
    
  cp5.addButton("Speed2") // name of the button
    .setPosition(200, 100) // x and y coords of upper left corner of button
    .setSize(120, 80)
    .setFont(font)
    ;
    
  cp5.addButton("Speed3") 
    .setPosition(340, 100) // x and y coords of upper left corner of button
    .setSize(120, 80)
    .setFont(font)
    ;
  
  cp5.addButton("OFF") // "OFF" is the name of the button
    .setPosition(60, 200) // x and y coords of upper left corner of button
    .setSize(400, 80)
    .setFont(font)
    ;
}

void draw(){
  background (255, 255, 255); // background of window (r,g,b) or (0 to 225)
  fill(74, 74, 74); // text color (r,g,b)
  textFont(font);
  text("SERVO CONTROL 3.0", 70, 50); //window title ("text", x coord, y xoord)
  //printArray(PFont.list());
    
}

void Speed1() {
  port.write(1);
}

void Speed2() {
  port.write(2);
}

void Speed3() {
  port.write(3);
}

void ON(){
  port.write('n');
}

void OFF(){
  port.write('f');
}
