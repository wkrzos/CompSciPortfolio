#include <Arduino.h>
#include <util/atomic.h>
#include <LiquidCrystal_I2C.h>

// Define pins for RGB LED
#define RED_PIN     6   // PWM pin
#define GREEN_PIN   5   // PWM pin
#define BLUE_PIN    3   // PWM pin

// Define pins for rotary encoder and button
#define ENCODER_PIN_A   A2
#define ENCODER_PIN_B   A3
#define BUTTON_PIN      7   // Button for selection

// Define debouncing period
#define DEBOUNCE_PERIOD 50UL

// Initialize the LCD
LiquidCrystal_I2C lcd(0x27, 16, 2);

// Variables for menu navigation
const int menuLength = 4;  // Total number of menu items
String menuItems[menuLength] = {
  "1. Red LED",
  "2. Green LED",
  "3. Blue LED",
  "4. Adjust Brightness"
};
int menuIndex = 0;        // Current top item index in the menu
int cursorPosition = 0;   // 0 or 1, indicates the cursor position on the LCD

// Variables for encoder reading
volatile int encoderValue = 0;
volatile int lastEncoderValue = 0;
volatile bool encoderMoved = false;
unsigned long lastEncoderTimestamp = 0UL;

// Variables for LED states
bool redState = false;
bool greenState = false;
bool blueState = false;
int brightness = 255;  // Default brightness

// Debounce variables for button
unsigned long lastButtonPress = 0;
const unsigned long buttonDebounceDelay = 200;

// Function prototypes
void updateMenu();
void selectMenuItem();
void updateLEDs();
void adjustBrightness();

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

  // Initialize button pin
  pinMode(BUTTON_PIN, INPUT_PULLUP);

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

  // Check for button press to select menu item
  if (digitalRead(BUTTON_PIN) == LOW) {
    unsigned long currentTime = millis();
    if (currentTime - lastButtonPress > buttonDebounceDelay) {
      selectMenuItem();
      lastButtonPress = currentTime;
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
  switch (selectedIndex) {
    case 0:
      redState = !redState;
      break;
    case 1:
      greenState = !greenState;
      break;
    case 2:
      blueState = !blueState;
      break;
    case 3:
      adjustBrightness();
      break;
    default:
      break;
  }
}

void updateLEDs() {
  analogWrite(RED_PIN, redState ? brightness : 0);
  analogWrite(GREEN_PIN, greenState ? brightness : 0);
  analogWrite(BLUE_PIN, blueState ? brightness : 0);
}

void adjustBrightness() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Set Brightness:");
  lcd.setCursor(0, 1);
  lcd.print(brightness);

  int localEncoderValue = 0;
  int lastLocalEncoderValue = 0;
  bool adjusting = true;

  while (adjusting) {
    if (encoderMoved) {
      ATOMIC_BLOCK(ATOMIC_RESTORESTATE) {
        localEncoderValue = encoderValue;
        encoderMoved = false;
      }

      int movement = localEncoderValue - lastLocalEncoderValue;
      lastLocalEncoderValue = localEncoderValue;

      if (movement > 0) {
        brightness += 5;
        if (brightness > 255) brightness = 255;
      } else if (movement < 0) {
        brightness -= 5;
        if (brightness < 0) brightness = 0;
      }

      lcd.setCursor(0, 1);
      lcd.print("     ");  // Clear previous value
      lcd.setCursor(0, 1);
      lcd.print(brightness);

      updateLEDs();
    }

    // Check for button press to exit brightness adjustment
    if (digitalRead(BUTTON_PIN) == LOW) {
      unsigned long currentTime = millis();
      if (currentTime - lastButtonPress > buttonDebounceDelay) {
        lastButtonPress = currentTime;
        adjusting = false;
      }
    }
  }
  // Return to menu
  updateMenu();
}
