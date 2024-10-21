#include <Arduino.h>

#define LED_RED 6
#define LED_GREEN 5
#define LED_BLUE 3

#define RED_BUTTON 2
#define GREEN_BUTTON 4

#define DEBOUNCE_PERIOD 100UL
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

bool debounceButton(int buttonPin)
{
    static int debounced_button_state = HIGH;
    static int previous_reading = HIGH;
    static unsigned long last_change_time = 0UL;

    int current_reading = digitalRead(buttonPin);
    if (previous_reading != current_reading) {
        last_change_time = millis();
    }

    if (millis() - last_change_time > DEBOUNCE_PERIOD) {
        if (current_reading != debounced_button_state) {
            debounced_button_state = current_reading;
            if (debounced_button_state == LOW) {
                return true;
            }
        }
    }

    previous_reading = current_reading;
    return false;
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
    if (debounceButton(GREEN_BUTTON) || debounceButton(RED_BUTTON)) {
        switchToNextLED();
    }
}