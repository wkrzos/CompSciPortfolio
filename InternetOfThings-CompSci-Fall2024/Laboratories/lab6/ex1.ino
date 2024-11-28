#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <OneWire.h>
#include <DallasTemperature.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);
OneWire oneWire(A1);
DallasTemperature tempSensors(&oneWire);

const int RED_PIN = 9;
const int GREEN_PIN = 10;
const int BLUE_PIN = 11;

float maxTemp = -100.0;
float minTemp = 100.0;

void setup() {
    tempSensors.begin();
    lcd.init();
    lcd.backlight();
    lcd.clear();

    pinMode(RED_PIN, OUTPUT);
    pinMode(GREEN_PIN, OUTPUT);
    pinMode(BLUE_PIN, OUTPUT);

    lcd.setCursor(0, 0);
    lcd.print("Weather Station");
    delay(2000);
    lcd.clear();
}

void loop() {
    tempSensors.requestTemperatures();
    float internalTemp = tempSensors.getTempCByIndex(0); // Internal sensor
    float externalTemp = tempSensors.getTempCByIndex(1); // External sensor

    if (externalTemp > maxTemp) maxTemp = externalTemp;
    if (externalTemp < minTemp) minTemp = externalTemp;

    lcd.setCursor(0, 0);
    lcd.print("In:");
    lcd.print(internalTemp, 1);
    lcd.print("C ");

    lcd.print("Out:");
    lcd.print(externalTemp, 1);
    lcd.print("C");

    lcd.setCursor(0, 1);
    lcd.print("Max:");
    lcd.print(maxTemp, 1);
    lcd.print("C Min:");
    lcd.print(minTemp, 1);
    lcd.print("C");

    if (externalTemp < 18.0) {
        setRGB(0, 0, 255);
    } else if (externalTemp > 25.0) {
        setRGB(255, 0, 0);
    } else {
        setRGB(0, 255, 0);
    }

    delay(1000);
}

void setRGB(int red, int green, int blue) {
    analogWrite(RED_PIN, red);
    analogWrite(GREEN_PIN, green);
    analogWrite(BLUE_PIN, blue);
}
