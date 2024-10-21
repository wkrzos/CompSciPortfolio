#include <Arduino.h>

#define LED_RED 6
#define LED_GREEN 5
#define LED_BLUE 3

int redValue = 255;    // Initial color values (full brightness of red)
int greenValue = 0;
int blueValue = 0;

int fadeAmount = 1;    // Amount of change in each step
int delayTime = 10;    // Delay time between changes (lower value means faster color change)

void setup() 
{
    pinMode(LED_RED, OUTPUT);
    pinMode(LED_GREEN, OUTPUT);
    pinMode(LED_BLUE, OUTPUT);
}

void loop()
{
    // Transition from red to green (red decreases, green increases)
    for (int i = 0; i < 255; i++) {
        redValue -= fadeAmount;
        greenValue += fadeAmount;
        setColor(redValue, greenValue, blueValue);
        delay(delayTime);
    }
    
    // Transition from green to blue (green decreases, blue increases)
    for (int i = 0; i < 255; i++) {
        greenValue -= fadeAmount;
        blueValue += fadeAmount;
        setColor(redValue, greenValue, blueValue);
        delay(delayTime);
    }

    // Transition from blue to red (blue decreases, red increases)
    for (int i = 0; i < 255; i++) {
        blueValue -= fadeAmount;
        redValue += fadeAmount;
        setColor(redValue, greenValue, blueValue);
        delay(delayTime);
    }
}

void setColor(int red, int green, int blue)
{
    analogWrite(LED_RED, red);
    analogWrite(LED_GREEN, green);
    analogWrite(LED_BLUE, blue);
}