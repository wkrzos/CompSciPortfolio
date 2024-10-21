#include <Arduino.h>
#include <LiquidCrystal_I2C.h>

#define RED_BUTTON 2
#define GREEN_BUTTON 4
#define DEBOUNCE_PERIOD 100UL

LiquidCrystal_I2C lcd(0x27, 16, 2);

unsigned long start_time = 0;
unsigned long elapsed_time = 0;
bool is_running = false;

unsigned long last_green_press_time = 0;
unsigned long last_red_press_time = 0;
bool last_green_button_state = HIGH;
bool last_red_button_state = HIGH;

void initButtons() {
    pinMode(RED_BUTTON, INPUT_PULLUP);
    pinMode(GREEN_BUTTON, INPUT_PULLUP);
}

void setup() {
    lcd.init();
    lcd.backlight();
    initButtons();

    lcd.setCursor(0, 0);
    lcd.print("Stoper:");
    lcd.setCursor(0, 1);
    lcd.print("00:00");
}

void updateDisplay(unsigned long time_in_seconds) {
    unsigned long minutes = time_in_seconds / 60;
    unsigned long seconds = time_in_seconds % 60;

    lcd.setCursor(0, 1);
    lcd.print((minutes < 10 ? "0" : "") + String(minutes) + ":");
    lcd.print((seconds < 10 ? "0" : "") + String(seconds));
}

bool debounceButton(int buttonPin, unsigned long& last_press_time, bool& last_button_state) {
    bool current_state = digitalRead(buttonPin);

    if (current_state != last_button_state) {
        last_press_time = millis();
    }

    if (millis() - last_press_time > DEBOUNCE_PERIOD) {
        if (current_state == LOW && last_button_state == HIGH) {
            last_button_state = current_state;
            return true;
        }
    }

    last_button_state = current_state;
    return false;
}

void loop() {
    if (debounceButton(GREEN_BUTTON, last_green_press_time, last_green_button_state)) {
        if (!is_running) {
            start_time = millis() - elapsed_time;
            is_running = true;
        } else {
            elapsed_time = millis() - start_time;
            is_running = false;
        }
    }

    if (debounceButton(RED_BUTTON, last_red_press_time, last_red_button_state)) {
        elapsed_time = 0;
        is_running = false;
        updateDisplay(0);
    }

    if (is_running) {
        unsigned long current_time = millis() - start_time;
        unsigned long time_in_seconds = current_time / 1000;
        updateDisplay(time_in_seconds);
    }
}
