#include <Arduino.h>
#include <LiquidCrystal_I2C.h>

#define RED_BUTTON 2
#define GREEN_BUTTON 4

LiquidCrystal_I2C lcd(0x27, 16, 2);

unsigned long start_time = 0;
unsigned long paused_time = 0;
bool display_paused = true;

void initButtons() {
    pinMode(RED_BUTTON, INPUT_PULLUP);
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
    if (digitalRead(GREEN_BUTTON) == LOW) {
        // Debounce delay
        delay(50);
        while (digitalRead(GREEN_BUTTON) == LOW);  // Wait for button release
        delay(50);
        if (display_paused) {
            // Start or resume updating display
            if (start_time == 0) {
                // First time starting
                start_time = millis();
            } else {
                // Resume, adjust start_time to account for the paused duration
                start_time += millis() - paused_time;
            }
            display_paused = false;
        } else {
            // Pause updating display
            paused_time = millis();
            display_paused = true;
        }
    }

    if (digitalRead(RED_BUTTON) == LOW) {
        // Debounce delay
        delay(50);
        while (digitalRead(RED_BUTTON) == LOW);  // Wait for button release
        delay(50);
        // Reset everything
        start_time = 0;
        paused_time = 0;
        display_paused = true;
        lcd.setCursor(0, 1);
        lcd.print("00:00:00.000");
    }

    if (!display_paused) {
        unsigned long current_time = millis();
        unsigned long elapsed_ms = current_time - start_time;
        updateDisplay(elapsed_ms);
    }
}
