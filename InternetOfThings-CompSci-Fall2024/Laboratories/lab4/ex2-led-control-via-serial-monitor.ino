#include <Arduino.h>

#define LED_RED 6
#define LED_GREEN 5
#define LED_BLUE 3

void setup() {
    pinMode(LED_RED, OUTPUT);
    pinMode(LED_GREEN, OUTPUT);
    pinMode(LED_BLUE, OUTPUT);

    analogWrite(LED_RED, 0);
    analogWrite(LED_GREEN, 0);
    analogWrite(LED_BLUE, 0);

    Serial.begin(9600);
    while (!Serial) {
    }
}

void loop() {
    if (Serial.available() > 0) {
        String command = Serial.readStringUntil('\n');
        command.trim();
        command.toLowerCase();

        // Format: "red 128", "green 255", "blue 0"
        if (command.startsWith("red ")) {
            int brightness = command.substring(4).toInt();
            brightness = constrain(brightness, 0, 255);  // Ensure value within PWM range
            analogWrite(LED_RED, brightness);
            Serial.println("Red LED set to brightness: " + String(brightness));
        } else if (command.startsWith("green ")) {
            int brightness = command.substring(6).toInt();
            brightness = constrain(brightness, 0, 255);
            analogWrite(LED_GREEN, brightness);
            Serial.println("Green LED set to brightness: " + String(brightness));
        } else if (command.startsWith("blue ")) {
            int brightness = command.substring(5).toInt();
            brightness = constrain(brightness, 0, 255);
            analogWrite(LED_BLUE, brightness);
            Serial.println("Blue LED set to brightness: " + String(brightness));
        } else {
            Serial.println("Unknown command: '" + command + "'");
        }
    }
}
