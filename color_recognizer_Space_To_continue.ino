/*********
  Rui Santos
  Complete project details at http://randomnerdtutorials.com  
*********/

// TCS230 or TCS3200 pins wiring to Arduino
#define S0 4
#define S1 5
#define S2 6
#define S3 7
#define sensorOut 8
#include <Keyboard.h>


// Stores frequency read by the photodiodes
int redFrequency = 0;
int greenFrequency = 0;
int blueFrequency = 0;
bool debug = false;
// Stores the red. green and blue colors

int redColor = 0;
int greenColor = 0;
int blueColor = 0;

int inc = 50;
int maxTotalCount = 20;
int timer = millis();
int next = timer + inc;
bool readyToRead = false;

int count = maxTotalCount;

int countBlue = 0;
int countRed = 0;
int countGreen = 0;
int countYellow = 0;

int maxCount = 0;
String maxColor = "U";
String currSeq = "";

void setup() {
  // Setting the outputs
  pinMode(S0, OUTPUT);
  pinMode(S1, OUTPUT);
  pinMode(S2, OUTPUT);
  pinMode(S3, OUTPUT);
  
  // Setting the sensorOut as an input
  pinMode(sensorOut, INPUT);
  
  // Setting frequency scaling to 20%
  digitalWrite(S0,HIGH);
  digitalWrite(S1,LOW);
  
  Serial.begin(9600);
  // initialize control over the keyboard:
  //Keyboard.begin();
}

void loop() {

  bool readyToRead = false;
  int timer = millis();
  
  // Setting RED (R) filtered photodiodes to be read
  digitalWrite(S2,LOW);
  digitalWrite(S3,LOW);
  
  // Reading the output frequency
  redFrequency = pulseIn(sensorOut, LOW);
  // Remaping the value of the RED (R) frequency from 0 to 255
  // You must replace with your own values. Here's an example: 
  // redColor = map(redFrequency, 70, 120, 255,0);
  //redColor = map(redFrequency, XX, XX, 255,0);
  
  // Printing the RED (R) value
  //Serial.print("R = ");
  //Serial.print(redColor);
  //delay(inc);
  
  // Setting GREEN (G) filtered photodiodes to be read
  digitalWrite(S2,HIGH);
  digitalWrite(S3,HIGH);
  
  // Reading the output frequency
  greenFrequency = pulseIn(sensorOut, LOW);
  // Remaping the value of the GREEN (G) frequency from 0 to 255
  // You must replace with your own values. Here's an example: 
  // greenColor = map(greenFrequency, 100, 199, 255, 0);
  //greenColor = map(greenFrequency, XX, XX, 255, 0);
  
  // Printing the GREEN (G) value  
  //Serial.print(" G = ");
  //Serial.print(greenColor);
  //delay(inc);
 
  // Setting BLUE (B) filtered photodiodes to be read
  digitalWrite(S2,LOW);
  digitalWrite(S3,HIGH);
  
  // Reading the output frequency
  blueFrequency = pulseIn(sensorOut, LOW);
  // Remaping the value of the BLUE (B) frequency from 0 to 255
  // You must replace with your own values. Here's an example: 
  // blueColor = map(blueFrequency, 38, 84, 255, 0);
  //blueColor = map(blueFrequency, XX, XX, 255, 0);
  
  // Printing the BLUE (B) value 
  //Serial.print(" B = ");
  //Serial.print(blueColor);
  //delay(inc);

  // Checks the current detected color and prints
  // a message in the serial monitor
  
  

  if (count >= maxTotalCount) {

    //Serial.println("The Block Color was " + maxColor);
    Serial.println(maxColor);
    currSeq = currSeq + maxColor;
    //Serial.println(currSeq);
    //clear input so extra spaces in buffer don't cause it to start
    while(Serial.available() > 0) { Serial.read(); }
    
    //Serial.println("Insert Next Block and press SPACE to continue");
    //wait for input
    while (Serial.available() == 0) {}
    
    char key = Serial.read();
    //if (key == 'c') {
      //count = 0;
      //currSeq = "";
    //}
    
    if ( key == ' ') {
        count = 0;
        //Serial.println("I got the message");
        
    }
    else{
      //Serial.println("I'm sorry I didn't catch that");
      //Serial.print("<");
      //Serial.print(key);
      //Serial.print(">");
    }
    countBlue = 0;
    countRed = 0;
    countGreen = 0;
    countYellow = 0;
    maxColor = "U";
    maxCount = 0;
    next = millis();
    //Serial.println(timer);
    //Serial.println(next);
    //Serial.println("Insert Next Block and press SPACE to continue");
    //Serial.println("Looking For Colors"); 
  }
  else if (timer >= next) {
    next = timer + inc;
    count++;
    //Serial.println(timer);
    //Serial.println(next);
    //Serial.println("ready");
    readyToRead = true;
    
    
  }
  if (readyToRead && redFrequency > 70 &&  greenFrequency < 100 && greenFrequency > 50 && blueFrequency >= 26) {
    if (debug) {
      Serial.println("Green");
    }
    countGreen++;

    if (countGreen > maxCount) {
      maxCount = countGreen;
      maxColor = "A";
    }
  }

  else if (readyToRead && redFrequency > 70 &&  greenFrequency < 90 && greenFrequency > 50 && blueFrequency <26) {
    if (debug) {
      Serial.println("Blue");
    }
    countBlue++;
    if (countBlue > maxCount) {
      maxCount = countBlue;
      maxColor = "T";
    }
  }

  else if (readyToRead && redFrequency < 40 &&  greenFrequency > 95 && blueFrequency < 26) {
    if (debug) {
      Serial.println("Red");
    }
    countRed++;
    if (countRed > maxCount) {
      maxCount = countRed;
      maxColor = "C";
    }
  } 

  else if (readyToRead && redFrequency < 26 &&  greenFrequency < 40 && blueFrequency < 20) {
    if (debug) {
      Serial.println("Yellow");
    }
    countYellow++;
    if (countYellow > maxCount) {
      maxCount = countYellow;
      maxColor = "G";
    }
  }

  else if (readyToRead) {
    if (debug) {
    Serial.print("Color Not Found, ");
    Serial.print("R = ");
    Serial.print(redFrequency);
    Serial.print(", G = ");
    Serial.print(greenFrequency);
    Serial.print(", B = ");
    Serial.println(blueFrequency);
    }
  }
 

 
  /*
  if(redColor > greenColor && redColor > blueColor){
      Serial.println(" - RED detected!");
  }
  if(greenColor > redColor && greenColor > blueColor){
    Serial.println(" - GREEN detected!");
  }
  if(blueColor > redColor && blueColor > greenColor){
    Serial.println(" - BLUE detected!");
  }*/
}
