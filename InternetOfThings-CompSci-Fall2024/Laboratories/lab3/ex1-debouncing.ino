#include <Arduino.h>

#define LED_RED 6
#define LED_GREEN 5
#define LED_BLUE 3

#define RED_BUTTON 2
#define GREEN_BUTTON 4

#define DEBOUNCE_PERIOD 50UL  // Adjusted debounce period for better responsiveness
#define LED_COUNT 3

int led_pins[LED_COUNT] = { LED_RED, LED_GREEN, LED_BLUE };
int led_index = 0;

// Structure to hold debouncing state for each button
struct DebounceState {
    int debounced_button_state;
    int previous_reading;
    unsigned long last_change_time;
};

// Initialize debouncing states for each button
DebounceState green_button_state = { HIGH, HIGH, 0 };
DebounceState red_button_state = { HIGH, HIGH, 0 };

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

bool debounceButton(int buttonPin, DebounceState &state)
{
    int current_reading = digitalRead(buttonPin);

    // Check if the button state has changed
    if (current_reading != state.previous_reading) {
        state.last_change_time = millis();
    }

    // If the state has been stable for longer than the debounce period
    if (millis() - state.last_change_time > DEBOUNCE_PERIOD) {
        // If the debounced state is different from the current reading
        if (current_reading != state.debounced_button_state) {
            state.debounced_button_state = current_reading;

            // Trigger on button release (from LOW to HIGH)
            if (state.debounced_button_state == HIGH && state.previous_reading == LOW) {
                state.previous_reading = current_reading;
                return true;
            }
        }
    }

    state.previous_reading = current_reading;
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
    // Check each button individually
    if (debounceButton(GREEN_BUTTON, green_button_state) || debounceButton(RED_BUTTON, red_button_state)) {
        switchToNextLED();
    }
}
