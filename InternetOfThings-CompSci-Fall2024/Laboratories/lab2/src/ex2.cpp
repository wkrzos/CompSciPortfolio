#include <Arduino.h>

#define LED_GREEN 5
#define RED_BUTTON 2
#define GREEN_BUTTON 4

int brightness = 0;
int fadeAmount = 1;

void initRGB() 
{
    pinMode(LED_GREEN, OUTPUT);
    analogWrite(LED_GREEN, brightness);
}

void initButtons()
{
    pinMode(RED_BUTTON, INPUT_PULLUP);
    pinMode(GREEN_BUTTON, INPUT_PULLUP);
}

void setup()
{
    initRGB();
    initButtons();
}

void loop()
{
    // Increase brightness by holding green button
    if (digitalRead(RED_BUTTON) == LOW) {
        brightness += fadeAmount;
        if (brightness > 255) {
            brightness = 255;
        }
        analogWrite(LED_GREEN, brightness);
        delay(50);
    }

    // Lower brightness by holding red button
    if (digitalRead(GREEN_BUTTON) == LOW) {
        brightness -= fadeAmount;
        if (brightness < 0) {
            brightness = 0;
        }
        analogWrite(LED_GREEN, brightness);
        delay(50);
    }
}