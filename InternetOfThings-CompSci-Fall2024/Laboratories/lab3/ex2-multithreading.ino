#include <Arduino.h>

#define LED_RED 6
#define LED_GREEN 5
#define LED_BLUE 3

#define RED_BUTTON 2
#define GREEN_BUTTON 4

void initRGB(){
    pinMode(LED_RED, OUTPUT);
    pinMode(LED_GREEN, OUTPUT);
    pinMode(LED_BLUE, OUTPUT);

    digitalWrite(LED_RED, HIGH);
    digitalWrite(LED_GREEN, LOW);
    digitalWrite(LED_BLUE, LOW);
}

void initButtons(){
    pinMode(RED_BUTTON, INPUT_PULLUP);
    pinMode(GREEN_BUTTON, INPUT_PULLUP);
}

// The three functions could be merged into one function taking the led name as a parameter. 
// However, this approach is more flexible, if we were to add more functionalities to each diode separately. 
// Moreover, one function would result in an awful number of if statements.
void setRedLed(){
    const unsigned long period = 900UL;
    static unsigned long last_change_time = 0UL;
    static int led_state = LOW;

    if (millis() - last_change_time >= period){
        if (led_state == HIGH){
            led_state = LOW;
        } else {
            led_state = HIGH;
        }

        digitalWrite(LED_RED, led_state);
        last_change_time += period;
    }
}

void setGreenLed(){
    const unsigned long period = 1000UL;
    static unsigned long last_change_time = 0UL;
    static int led_state = LOW;

    if(millis() - last_change_time >= period){
        if(led_state == HIGH){
            led_state = LOW;
        } else {
            led_state = HIGH;
        }

        digitalWrite(LED_GREEN, led_state);
        last_change_time += period;
    }
}

void setBlueLed(){
    const unsigned long period = 1100UL;
    static unsigned long last_change_time = 0UL;
    static int led_state = LOW;

    if(millis() - last_change_time >= period){
        if(led_state == HIGH){
            led_state = LOW;
        } else {
            led_state = HIGH;
        }

        digitalWrite(LED_BLUE, led_state);
        last_change_time += period;
    }
}

void setup(){
    initRGB();
    initButtons();
}

void loop(){
    setRedLed();
    setGreenLed();
    setBlueLed();
}