#include <Arduino.h>
#include <util/atomic.h>
#include <LiquidCrystal_I2C.h>

// Define pins for RGB LED
#define RED_PIN     6   // PWM pin
#define GREEN_PIN   5   // PWM pin
#define BLUE_PIN    3   // PWM pin

// Define pins for rotary encoder and buttons
#define ENCODER_PIN_A   A2
#define ENCODER_PIN_B   A3
#define BUTTON_GREEN_PIN  7   // Green button for selection
#define BUTTON_RED_PIN    8   // Red button to exit adjustment

// Define debouncing period
#define DEBOUNCE_PERIOD 50UL

// Initialize the LCD
LiquidCrystal_I2C lcd(0x27, 16, 2);

// Variables for menu navigation
const int menuLength = 3;  // Total number of menu items
String menuItems[menuLength] = {
  "1. Red LED",
  "2. Green LED",
  "3. Blue LED"
};
int menuIndex = 0;        // Current top item index in the menu
int cursorPosition = 0;   // 0 or 1, indicates the cursor position on the LCD

// Variables for encoder reading
volatile int encoderValue = 0;
volatile int lastEncoderValue = 0;
volatile bool encoderMoved = false;
unsigned long lastEncoderTimestamp = 0UL;

// Variables for LED brightness
int redBrightness = 0;     // Initialize brightness to 0
int greenBrightness = 0;
int blueBrightness = 0;

// Debounce variables for buttons
unsigned long lastGreenButtonPress = 0;
unsigned long lastRedButtonPress = 0;
const unsigned long buttonDebounceDelay = 200;

// Adjustment mode flag
bool inAdjustmentMode = false;

// Function prototypes
void updateMenu();
void selectMenuItem();
void updateLEDs();
void adjustBrightness(String color);

// ISR for encoder pin changes
ISR(PCINT1_vect) {
  static int lastEncoded = 0;
  int MSB = digitalRead(ENCODER_PIN_A); // MSB = most significant bit
  int LSB = digitalRead(ENCODER_PIN_B); // LSB = least significant bit

  int encoded = (MSB << 1) | LSB;       // Combine the two bits
  int sum = (lastEncoded << 2) | encoded; // Combine previous and current

  if (millis() - lastEncoderTimestamp > DEBOUNCE_PERIOD) {
    if (sum == 0b1101 || sum == 0b0100 || sum == 0b0010 || sum == 0b1011) {
      encoderValue++;
      encoderMoved = true;
    }
    if (sum == 0b1110 || sum == 0b0111 || sum == 0b0001 || sum == 0b1000) {
      encoderValue--;
      encoderMoved = true;
    }
    lastEncoderTimestamp = millis();
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

  // Initialize button pins
  pinMode(BUTTON_GREEN_PIN, INPUT_PULLUP);
  pinMode(BUTTON_RED_PIN, INPUT_PULLUP);

  // Initialize LCD
  lcd.init();
  lcd.backlight();

  // Display the initial menu
  updateMenu();

  // Enable pin change interrupt for encoder pins
  PCICR |= (1 << PCIE1);   // Enable Pin Change Interrupt Control Register for PCIE1 (A0-A5)
  PCMSK1 |= (1 << PCINT10) | (1 << PCINT11); // Enable PCINT10 (A2) and PCINT11 (A3)
}

void loop() {
  // Check if the encoder has moved
  if (encoderMoved) {
    if (!inAdjustmentMode) {
      int movement;
      ATOMIC_BLOCK(ATOMIC_RESTORESTATE) {
        movement = encoderValue - lastEncoderValue;
        lastEncoderValue = encoderValue;
        encoderMoved = false;
      }

      if (movement > 0) {
        // Rotated clockwise
        cursorPosition++;
        if (cursorPosition > 1) {
          cursorPosition = 1;
          menuIndex++;
          if (menuIndex > menuLength - 2) {
            menuIndex = menuLength - 2;
          }
        }
      } else if (movement < 0) {
        // Rotated counter-clockwise
        cursorPosition--;
        if (cursorPosition < 0) {
          cursorPosition = 0;
          menuIndex--;
          if (menuIndex < 0) {
            menuIndex = 0;
          }
        }
      }
      updateMenu();
    }
  }

  // Check for green button press to select menu item
  if (digitalRead(BUTTON_GREEN_PIN) == LOW) {
    unsigned long currentTime = millis();
    if (currentTime - lastGreenButtonPress > buttonDebounceDelay) {
      selectMenuItem();
      lastGreenButtonPress = currentTime;
    }
  }

  // Update LED states
  updateLEDs();
}

void updateMenu() {
  lcd.clear();
  // Display two menu items starting from menuIndex
  lcd.setCursor(0, 0);
  lcd.print(menuItems[menuIndex]);
  lcd.setCursor(0, 1);
  lcd.print(menuItems[menuIndex + 1]);

  // Display cursor indicator
  lcd.setCursor(15, cursorPosition);
  lcd.print("<");
}

void selectMenuItem() {
  int selectedIndex = menuIndex + cursorPosition;
  inAdjustmentMode = true; // Enter adjustment mode
  switch (selectedIndex) {
    case 0:
      adjustBrightness("Red");
      break;
    case 1:
      adjustBrightness("Green");
      break;
    case 2:
      adjustBrightness("Blue");
      break;
    default:
      break;
  }
}

void updateLEDs() {
  analogWrite(RED_PIN, redBrightness);
  analogWrite(GREEN_PIN, greenBrightness);
  analogWrite(BLUE_PIN, blueBrightness);
}

void adjustBrightness(String color) {
  int *brightnessPtr;  // Pointer to the brightness variable
  int brightnessValue; // Current brightness value
  String menuItem;     // Menu item string

  if (color == "Red") {
    brightnessPtr = &redBrightness;
    brightnessValue = redBrightness;
    menuItem = menuItems[0]; // "1. Red LED"
  } else if (color == "Green") {
    brightnessPtr = &greenBrightness;
    brightnessValue = greenBrightness;
    menuItem = menuItems[1]; // "2. Green LED"
  } else if (color == "Blue") {
    brightnessPtr = &blueBrightness;
    brightnessValue = blueBrightness;
    menuItem = menuItems[2]; // "3. Blue LED"
  } else {
    // Invalid color
    inAdjustmentMode = false;
    return;
  }

  // Display the menu item and the current brightness
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(menuItem);
  lcd.print(" ");
  lcd.print(brightnessValue);

  // Reset encoder values
  ATOMIC_BLOCK(ATOMIC_RESTORESTATE) {
    lastEncoderValue = encoderValue;
  }

  bool adjusting = true;

  // Adjust brightness
  while (adjusting) {
    if (encoderMoved) {
      int movement;
      ATOMIC_BLOCK(ATOMIC_RESTORESTATE) {
        movement = encoderValue - lastEncoderValue;
        lastEncoderValue = encoderValue;
        encoderMoved = false;
      }

      if (movement != 0) {
        brightnessValue += movement * 5;  // Adjust brightness in steps of 5
        if (brightnessValue > 255) brightnessValue = 255;
        if (brightnessValue < 0) brightnessValue = 0;

        *brightnessPtr = brightnessValue;  // Update the brightness variable

        // Update the displayed value
        lcd.setCursor(menuItem.length() + 1, 0);
        lcd.print("     ");  // Clear previous value
        lcd.setCursor(menuItem.length() + 1, 0);
        lcd.print(brightnessValue);

        updateLEDs();
      }
    }

    // Check for red button press to exit brightness adjustment
    if (digitalRead(BUTTON_RED_PIN) == LOW) {
      unsigned long currentTime = millis();
      if (currentTime - lastRedButtonPress > buttonDebounceDelay) {
        lastRedButtonPress = currentTime;
        adjusting = false;
      }
    }
  }

  inAdjustmentMode = false; // Exit adjustment mode

  // Return to menu
  updateMenu();
}
