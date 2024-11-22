#include <Arduino.h>

#define LED_RED 6
#define LED_GREEN 5
#define LED_BLUE 3

#define RED_BUTTON 2
#define GREEN_BUTTON 4

#define LED_COUNT 3

int led_pins[LED_COUNT] = { LED_RED, LED_GREEN, LED_BLUE };
int led_index = 0;

void initRGB()
{
    pinMode(LED_RED, OUTPUT);
    pinMode(LED_GREEN, OUTPUT);
    pinMode(LED_BLUE, OUTPUT);
    
    digitalWrite(LED_RED, HIGH);
    digitalWrite(LED_GREEN, LOW);
    digitalWrite(LED_BLUE, LOW);
}

void initButtons()
{
    pinMode(RED_BUTTON, INPUT_PULLUP);
    pinMode(GREEN_BUTTON, INPUT_PULLUP);
}

void switchToNextLED()
{
    // Turn off the current LED
    digitalWrite(led_pins[led_index], LOW);
    
    // Move to the next LED in the cycle
    led_index = (led_index + 1) % LED_COUNT;
    
    // Turn on the next LED
    digitalWrite(led_pins[led_index], HIGH);
}

void setup()
{
    initRGB();
    initButtons();
}

void loop()
{
    // Check for button release (button goes from LOW to HIGH)
    if (digitalRead(GREEN_BUTTON) == HIGH && digitalRead(RED_BUTTON) == HIGH) {
        static bool green_pressed = false;
        static bool red_pressed = false;

        if (digitalRead(GREEN_BUTTON) == LOW) {
            green_pressed = true;
        } else if (green_pressed && digitalRead(GREEN_BUTTON) == HIGH) {
            green_pressed = false;
            switchToNextLED();
        }

        if (digitalRead(RED_BUTTON) == LOW) {
            red_pressed = true;
        } else if (red_pressed && digitalRead(RED_BUTTON) == HIGH) {
            red_pressed = false;
            switchToNextLED();
        }
    }
}
