#include <Arduino.h>

#define RED_BUTTON 2
#define GREEN_BUTTON 4
#define TRANSMIT_PERIOD 100UL
#define DEBOUNCE_PERIOD 50UL

unsigned long lastTransmitTime = 0;

bool debounceButton(int buttonPin) {
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

void setup() {
    // Set up serial communication at the maximum speed
    Serial.begin(115200);
    while (!Serial) {
        // Wait for serial port to connect
    }

    // Set up button pins as input with internal pull-up resistors
    pinMode(RED_BUTTON, INPUT_PULLUP);
    pinMode(GREEN_BUTTON, INPUT_PULLUP);
}

void loop() {
    // Check if enough time has passed since the last transmission
    if (millis() - lastTransmitTime >= TRANSMIT_PERIOD) {
        // Update the last transmission time
        lastTransmitTime += TRANSMIT_PERIOD;

        // Get the debounced button states
        bool redPressed = debounceButton(RED_BUTTON);
        bool greenPressed = debounceButton(GREEN_BUTTON);

        // Send button states over serial
        // "0" means button not pressed, "1" means button pressed
        Serial.print("Red: ");
        Serial.print(redPressed ? 1 : 0);  // 1 if pressed, 0 if not
        Serial.print(" Green: ");
        Serial.println(greenPressed ? 1 : 0);
    }
}