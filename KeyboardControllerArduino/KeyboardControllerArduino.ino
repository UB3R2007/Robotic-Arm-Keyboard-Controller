#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

// Create the PWM driver object
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

// Define the minimum and maximum pulse lengths
#define SERVOMIN 85  // Minimum pulse length
#define SERVOMAX 510 // Maximum pulse length
#define SERVO_FREQ 50 // Analog servos run at ~50 Hz PWM

String inputString = "";  // Store incoming serial data
bool stringComplete = false;

void setup() {
  Serial.begin(9600);
  Serial.println("Begin Test");
  pwm.begin();
  pwm.setPWMFreq(SERVO_FREQ);  // Analog servos run at ~50 Hz PWM
}

void loop() {
  // If a complete string is received, process it
  if (stringComplete) {
    Serial.print("Received input string: ");
    Serial.println(inputString);  // Debug print to confirm received data

    // Ensure that the input string follows the expected format "<motor:angle>"
    if (inputString[0] == '<' && inputString[inputString.length() - 1] == '>') {
      int motor = inputString.substring(1, 2).toInt();  // Extract motor number
      int angle = inputString.substring(3, inputString.length() - 1).toInt();  // Extract angle

      Serial.print("Parsed motor: ");
      Serial.println(motor);
      Serial.print("Parsed angle: ");
      Serial.println(angle);

      // Ensure motor number is valid (between 0 and 5 for 6 DOF)
      if (motor >= 0 && motor < 6) {
        setServo(motor, angle);  // Move the servo
      } else {
        Serial.println("Invalid motor number");
      }
    } else {
      Serial.println("Invalid input format");
    }

    inputString = "";  // Clear the string after processing
    stringComplete = false;  // Reset flag
  }
}

void setServo(int servoNum, int angle) {
  // Map the position from 0-180 to SERVOMIN-SERVOMAX
  int pos = map(angle, 0, 180, SERVOMIN, SERVOMAX);
  Serial.print("Setting motor ");
  Serial.print(servoNum);
  Serial.print(" to position: ");
  Serial.println(pos);
  pwm.setPWM(servoNum, 0, pos);  // Set the servo to the calculated position
}

void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    inputString += inChar;
    if (inChar == '>') {  // Look for the end character '>'
      stringComplete = true;
    }
  }
}
