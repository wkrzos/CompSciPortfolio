#include "RGBLED.h"

// Constructor: Initialize the RGB LED pins
RGBLED::RGBLED(int rPin, int gPin, int bPin) {
    redPin = rPin;
    greenPin = gPin;
    bluePin = bPin;
    pinMode(redPin, OUTPUT);
    pinMode(greenPin, OUTPUT);
    pinMode(bluePin, OUTPUT);
    off(); // Turn off the LED initially
}

// Set RGB color by values
void RGBLED::setColor(int red, int green, int blue) {
    analogWrite(redPin, red);
    analogWrite(greenPin, green);
    analogWrite(bluePin, blue);
}

// Set predefined colors
void RGBLED::setColor(const char* colorName) {
    if (strcmp(colorName, "RED") == 0) setColor(RED);
    else if (strcmp(colorName, "GREEN") == 0) setColor(GREEN);
    else if (strcmp(colorName, "BLUE") == 0) setColor(BLUE);
    else if (strcmp(colorName, "YELLOW") == 0) setColor(YELLOW);
    else if (strcmp(colorName, "CYAN") == 0) setColor(CYAN);
    else if (strcmp(colorName, "MAGENTA") == 0) setColor(MAGENTA);
    else if (strcmp(colorName, "BLACK") == 0) off();
    else if (strcmp(colorName, "WHITE") == 0) setColor(WHITE);
}

// Turn off the LED
void RGBLED::off() {
    analogWrite(redPin, 0);
    analogWrite(greenPin, 0);
    analogWrite(bluePin, 0);
}
