#include <Arduino.h>
#include <LiquidCrystal_I2C.h>

#define GREEN_BUTTON 4

LiquidCrystal_I2C lcd(0x27, 16, 2);

unsigned long start_time = 0;      // Start time of the stopwatch
unsigned long paused_time = 0;    // Time to freeze on LCD
bool display_paused = false;      // Tracks if the display is paused

void initButtons() {
    pinMode(GREEN_BUTTON, INPUT_PULLUP);
}

void setup() {
    lcd.init();
    lcd.backlight();
    initButtons();

    lcd.setCursor(0, 0);
    lcd.print("Stopwatch:");
    lcd.setCursor(0, 1);
    lcd.print("00:00:00.000");

    start_time = millis();  // Start the timer immediately
}

void updateDisplay(unsigned long elapsed_ms) {
    unsigned long total_seconds = elapsed_ms / 1000;
    unsigned long milliseconds = elapsed_ms % 1000;
    unsigned long hours = total_seconds / 3600;
    unsigned long minutes = (total_seconds % 3600) / 60;
    unsigned long seconds = total_seconds % 60;

    lcd.setCursor(0, 1);
    lcd.print((hours < 10 ? "0" : "") + String(hours) + ":");
    lcd.print((minutes < 10 ? "0" : "") + String(minutes) + ":");
    lcd.print((seconds < 10 ? "0" : "") + String(seconds) + ".");
    if (milliseconds < 10) {
        lcd.print("00" + String(milliseconds));
    } else if (milliseconds < 100) {
        lcd.print("0" + String(milliseconds));
    } else {
        lcd.print(String(milliseconds));
    }
}

void loop() {
    static unsigned long last_button_press = 0;
    unsigned long current_time = millis();

    // Handle green button press
    if (digitalRead(GREEN_BUTTON) == LOW) {
        if (current_time - last_button_press > 200) {  // Debounce
            last_button_press = current_time;

            if (display_paused) {
                // Resume live display
                display_paused = false;
            } else {
                // Pause display, keep stopwatch running
                paused_time = current_time - start_time;
                display_paused = true;
            }
        }
    }

    if (!display_paused) {
        // Live display: Show continuously updated time
        unsigned long elapsed_time = current_time - start_time;
        updateDisplay(elapsed_time);
    } else {
        // Paused display: Show the frozen time
        updateDisplay(paused_time);
    }
}
