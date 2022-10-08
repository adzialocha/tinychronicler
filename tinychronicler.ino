#include <RGBmatrixPanel.h>

#define CLK 11
#define OE   9
#define LAT 10
#define A   A0
#define B   A1
#define C   A2
#define D   A3

RGBmatrixPanel matrix(A, B, C, D, CLK, LAT, OE, false);
uint16_t COLOR_BACKGROUND = matrix.Color888(255, 0, 90, true);
uint16_t COLOR_FOREGROUND = matrix.Color888(0, 255, 165, true);

void setup() {
  // Initialise serial communication between RaspberryPI and Arduino
  Serial.begin(19200);

  // Initialise 32x32 RGB LED matrix
  matrix.begin();
}

void loop() {
  if (Serial.available() == 0) {
    return;
  }

  int data = Serial.read() - '0';

  switch (data) {
    case 0:
      reset();
      break;
    case 1:
      printBackground();
      break;
    case 2:
      printLeftEye();
      break;
    case 3:
      printRightEye();
      break;
    case 4:
      printLeftEye();
      printRightEye();
      break;
    case 5:
      printMouth();
      break;
    case 6:
      resetEyes();
      break;
    case 7:
      resetMouth();
      break;
    default:
      break;
  }
}

void printBackground() {
  matrix.fillScreen(COLOR_BACKGROUND);
}

void resetEyes() {
  matrix.fillCircle(8, 8, 3, COLOR_BACKGROUND);
  matrix.fillCircle(23, 8, 3, COLOR_BACKGROUND);
}

void printLeftEye() {
  matrix.fillCircle(8, 8, 3, COLOR_FOREGROUND);
}

void printRightEye() {
  matrix.fillCircle(23, 8, 3, COLOR_FOREGROUND);
}

void resetMouth() {
  matrix.fillCircle(15, 19, 5, COLOR_BACKGROUND);
}

void printMouth() {
  matrix.fillCircle(15, 19, 5, COLOR_FOREGROUND);
}

void reset() {
  matrix.fillScreen(matrix.Color888(0, 0, 0));
}
