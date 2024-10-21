#include <Arduino.h>

#include <Arduino.h>

#define LED_RED 6
#define LED_GREEN 5
#define LED_BLUE 3

#define RED_BUTTON 2
#define GREEN_BUTTON 4

bool ledState = false;
int currentColor = LED_RED;

void initRGB() 
{
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
  
  pinMode(LED_RED, OUTPUT);
  digitalWrite(LED_RED, LOW);
  
  pinMode(LED_GREEN, OUTPUT);
  digitalWrite(LED_GREEN, LOW);
  
  pinMode(LED_BLUE, OUTPUT);
  digitalWrite(LED_BLUE, LOW);
}

void initButtons()
{
  pinMode(RED_BUTTON, INPUT_PULLUP);
  pinMode(GREEN_BUTTON, INPUT_PULLUP);
}

void toggleLED() {
  ledState = !ledState;
  if (ledState) {
      digitalWrite(currentColor, HIGH);
  } else {
      digitalWrite(LED_RED, LOW);
      digitalWrite(LED_GREEN, LOW);
      digitalWrite(LED_BLUE, LOW);
  }
}

void changeColor() {
  if (ledState) {
    digitalWrite(currentColor, LOW);
  }

  // Change the color
  if (currentColor == LED_RED) {
      currentColor = LED_GREEN;
  } else if (currentColor == LED_GREEN) {
      currentColor = LED_BLUE;
  } else {
      currentColor = LED_RED;
  }

  if (ledState) {
    digitalWrite(currentColor, HIGH);
  }
}

void setup()
{
  initRGB();
  initButtons();
}

void loop()
{
    if (digitalRead(GREEN_BUTTON) == LOW) {
        delay(200);  // Debouncing
        toggleLED();
    }
    
    if (digitalRead(RED_BUTTON) == LOW) {
        delay(200);  // Debouncing
        changeColor();
    }
}