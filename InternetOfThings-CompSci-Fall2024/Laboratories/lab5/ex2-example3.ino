#include <Arduino.h>
#include <LiquidCrystal_I2C.h>

#define RED_PIN     6
#define GREEN_PIN   5
#define BLUE_PIN    3
#define ENCODER_PIN_A   A2
#define ENCODER_PIN_B   A3
#define GREEN_BUTTON    4
#define RED_BUTTON      7

LiquidCrystal_I2C lcd(0x27, 16, 2);

int brightnessValues[3] = {255, 255, 255}; // Brightness values for red, blue, and green
int menuIndex = 0;                         // Current menu selection
bool adjustingBrightness = false;          // Indicates brightness adjustment mode
volatile int encoderValue = 0;
volatile bool encoderMoved = false;

// Encoder interrupt service routine
ISR(PCINT1_vect) {
    static int lastEncoded = 0;
    int MSB = digitalRead(ENCODER_PIN_A);
    int LSB = digitalRead(ENCODER_PIN_B);

    int encoded = (MSB << 1) | LSB;
    int sum = (lastEncoded << 2) | encoded;

    if (sum == 0b1101 || sum == 0b0100 || sum == 0b0010 || sum == 0b1011) {
        encoderValue++;
        encoderMoved = true;
    }
    if (sum == 0b1110 || sum == 0b0111 || sum == 0b0001 || sum == 0b1000) {
        encoderValue--;
        encoderMoved = true;
    }

    lastEncoded = encoded;
}

void setup() {
    // Initialize RGB LED pins
    pinMode(RED_PIN, OUTPUT);
    pinMode(GREEN_PIN, OUTPUT);
    pinMode(BLUE_PIN, OUTPUT);

    // Initialize encoder pins
    pinMode(ENCODER_PIN_A, INPUT_PULLUP);
    pinMode(ENCODER_PIN_B, INPUT_PULLUP);

    // Initialize buttons
    pinMode(GREEN_BUTTON, INPUT_PULLUP);
    pinMode(RED_BUTTON, INPUT_PULLUP);

    // Initialize LCD
    lcd.init();
    lcd.backlight();

    // Display the initial menu
    updateMenu();

    // Enable encoder interrupts
    PCICR |= (1 << PCIE1);
    PCMSK1 |= (1 << PCINT10) | (1 << PCINT11);
}

void loop() {
    // Handle menu navigation with encoder
    if (encoderMoved && !adjustingBrightness) {
        encoderMoved = false;
        menuIndex += (encoderValue > 0) ? 1 : -1;
        encoderValue = 0;
        if (menuIndex < 0) menuIndex = 0;
        if (menuIndex > 2) menuIndex = 2;
        updateMenu();
    }

    // Handle green button press to enter/exit brightness adjustment
    if (digitalRead(GREEN_BUTTON) == LOW) {
        delay(200); // Debounce
        if (!adjustingBrightness) {
            adjustingBrightness = true;
            updateMenuWithBrightness();
        }
    }

    // Handle red button press to exit brightness adjustment
    if (digitalRead(RED_BUTTON) == LOW) {
        delay(200); // Debounce
        if (adjustingBrightness) {
            adjustingBrightness = false;
            updateMenu();
        }
    }

    // Adjust brightness with encoder while in adjustment mode
    if (adjustingBrightness && encoderMoved) {
        encoderMoved = false;
        int movement = encoderValue;
        encoderValue = 0;
        brightnessValues[menuIndex] += (movement > 0) ? 5 : -5;
        if (brightnessValues[menuIndex] > 255) brightnessValues[menuIndex] = 255;
        if (brightnessValues[menuIndex] < 0) brightnessValues[menuIndex] = 0;
        updateMenuWithBrightness();
    }

    // Update LED brightness
    analogWrite(RED_PIN, brightnessValues[0]);
    analogWrite(BLUE_PIN, brightnessValues[1]);
    analogWrite(GREEN_PIN, brightnessValues[2]);
}

void updateMenu() {
    lcd.clear();
    for (int i = 0; i < 3; i++) {
        lcd.setCursor(0, i);
        lcd.print(String(i + 1) + ". ");
        lcd.print((i == 0) ? "red" : (i == 1) ? "blue" : "green");
        if (i == menuIndex) {
            lcd.setCursor(14, i);
            lcd.print("<");
        }
    }
}

void updateMenuWithBrightness() {
    lcd.clear();
    for (int i = 0; i < 3; i++) {
        lcd.setCursor(0, i);
        lcd.print(String(i + 1) + ". ");
        lcd.print((i == 0) ? "red" : (i == 1) ? "blue" : "green");
        if (i == menuIndex) {
            lcd.setCursor(6, i);
            lcd.print(" ");
            lcd.print(brightnessValues[i]);
        }
    }
}
