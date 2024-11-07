#include <Arduino.h>

#define POTENTIOMETER_PIN A0
#define ADC_MAX_VALUE 1023
#define VOLTAGE_REFERENCE 5.0

void setup() {
    Serial.begin(9600);
    while (!Serial) { }
}

void loop() {
    int adcValue = analogRead(POTENTIOMETER_PIN);

    float voltage = (adcValue / (float)ADC_MAX_VALUE) * VOLTAGE_REFERENCE;

    Serial.print("ADC Value: ");
    Serial.print(adcValue);
    Serial.print("  Voltage: ");
    Serial.println(voltage, 2);

    delay(100);  // The author is aware of this delay() usage.
}
