#include <Arduino.h>
#include <LiquidCrystal_I2C.h>

#define RED_PIN 6
#define BLUE_PIN 3

#define ENCODER_PIN_A A2
#define ENCODER_PIN_B A3

LiquidCrystal_I2C lcd(0x27, 16, 2);

int encoderValue = 0;
int lastEncoded = 0;
int lastEncoderValue = 0;
int lastMSB = 0;
int lastLSB = 0;

unsigned long lastEncoderReadTime = 0;
const unsigned long encoderReadInterval = 5;

void setup() {
  pinMode(RED_PIN, OUTPUT);
  pinMode(BLUE_PIN, OUTPUT);

  pinMode(ENCODER_PIN_A, INPUT_PULLUP);
  pinMode(ENCODER_PIN_B, INPUT_PULLUP);

  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("Encoder Value:");
  lcd.setCursor(0, 1);
  lcd.print(encoderValue);
}

void loop() {
  // Debounce encoder reading
  if (millis() - lastEncoderReadTime >= encoderReadInterval) {
    int MSB = digitalRead(ENCODER_PIN_A); // MSB = most significant bit
    int LSB = digitalRead(ENCODER_PIN_B); // LSB = least significant bit

    int encoded = (MSB << 1) | LSB;       // Combine the two bits
    int sum = (lastEncoded << 2) | encoded; // Combine previous and current

    // Determine rotation direction and adjust encoderValue
    if (sum == 0b1101 || sum == 0b0100 || sum == 0b0010 || sum == 0b1011) {
      encoderValue++;
    }
    if (sum == 0b1110 || sum == 0b0111 || sum == 0b0001 || sum == 0b1000) {
      encoderValue--;
    }

    if (encoderValue < 0) encoderValue = 0;
    if (encoderValue > 255) encoderValue = 255;

    // Update the LCD display
    lcd.setCursor(0, 1);
    lcd.print("                ");
    lcd.setCursor(0, 1);
    lcd.print(encoderValue);

    // Update the LED color
    analogWrite(RED_PIN, encoderValue);
    analogWrite(BLUE_PIN, 255 - encoderValue);

    // Prepare for next reading
    lastEncoded = encoded;
    lastEncoderReadTime = millis();
  }
}
