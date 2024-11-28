#ifndef RGBLED_H
#define RGBLED_H

#include <Arduino.h>

// Predefined color constants
#define RED 255, 0, 0
#define GREEN 0, 255, 0
#define BLUE 0, 0, 255
#define YELLOW 255, 255, 0
#define CYAN 0, 255, 255
#define MAGENTA 255, 0, 255
#define BLACK 0, 0, 0
#define WHITE 255, 255, 255

class RGBLED {
private:
    int redPin, greenPin, bluePin; // Pin numbers for the RGB LED

public:
    // Constructor: Define the pins for the RGB LED
    RGBLED(int redPin, int greenPin, int bluePin);

    // Method to set RGB color by values (0-255)
    void setColor(int red, int green, int blue);

    // Method to set predefined colors (using RED, GREEN, etc.)
    void setColor(const char* colorName);

    // Turn off the LED
    void off();
};

#endif
