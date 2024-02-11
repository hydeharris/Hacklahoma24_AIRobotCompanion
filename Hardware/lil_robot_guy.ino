#include <Servo.h>

const int arm1_pin = 9;
const int arm2_pin = 10;

Servo arm1;
Servo arm2;

const int arms_down = 45;
const int arms_up = -45;

bool speechInProgress = false;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  arm1.attach(arm1_pin);
  arm2.attach(arm2_pin);
  arm1.write(arms_down);
  arm2.write(arms_down);
}

void loop() {
   if (Serial.available() > 0) {
    char input[50]; // Array to store received data
    int i = 0;
    while (Serial.available() > 0) {
      input[i] = Serial.read(); // Read each character
      i++;
      if (i >= 49) break; // Avoid buffer overflow
    }
    input[i] = '\0'; // Null terminate the string
    
    // Search for the substring
    if (strstr(input, "speechBegin") != NULL) {
      Serial.println(input);
      speechInProgress = true; // Set speech in progress flag
    } else if (strstr(input, "speechEnd") != NULL) { // Check if the received data is "speechEnd"
      Serial.println(input);
      speechInProgress = false; // Clear speech in progress flag
      // Stop servos
      arm1.write(arms_down); // Set servos to neutral position
      arm2.write(arms_down);
    }
  }

  delay(10);
  
  if (speechInProgress == true) { // If speech is in progress
    // Move servos back and forth
    rotate_servos();
  }
}

void rotate_servos(){
    arm1.write(arms_up);
    arm2.write(arms_up);
    delay(1000);
    arm1.write(arms_down);
    arm2.write(arms_down);
    delay(1000);
}
