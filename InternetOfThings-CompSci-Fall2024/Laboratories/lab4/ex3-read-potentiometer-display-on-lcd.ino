#include <Arduino.h>
#include <LiquidCrystal_I2C.h>

#define POTENTIOMETER A0
#define ADC_MAX_VALUE 1023
#define VOLTAGE_REFERENCE 5.0

LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup() {
    lcd.init();
    lcd.backlight();

    lcd.setCursor(0, 0);
    lcd.print("ADC: ");
    lcd.setCursor(8, 0);
    lcd.print("V: ");
}

void loop() {
    int adcValue = analogRead(POTENTIOMETER);

    float voltage = (adcValue / (float)ADC_MAX_VALUE) * VOLTAGE_REFERENCE;

    // Display the ADC value
    lcd.setCursor(4, 0);
    lcd.print(adcValue);
    lcd.print("   ");

    // Display the calculated voltage
    lcd.setCursor(10, 0);
    lcd.print(voltage, 2);
    lcd.print("V ");

    // Check if ADC value reaches extremes and display stability message
    lcd.setCursor(0, 1);
    if (adcValue == 0) {
        lcd.print("Min value stable    ");
    } else if (adcValue == ADC_MAX_VALUE) {
        lcd.print("Max value stable    ");
    } else {
        lcd.print("                    ");
    }

    delay(500);  // The author is aware of this delay usage. Since no other tasks need to be performed, milis won't be used.
}
