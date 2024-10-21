#include <Arduino.h>

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  digitalWrite(LED_BUILTIN, HIGH);
  delay(12);
  digitalWrite(LED_BUILTIN, LOW);
  delay(12);
}
// Judged by eye at delay ~= 15 the diode stops turning off, it gets dimmer and brighter
// The diode stops blinking at delay ~= 12