// Disclaimer: The author has asked ChatGPT to generate the comments in this code. The code logic is original.

#include <Arduino.h>
#include <LiquidCrystal_I2C.h>

#define RED_PIN     6
#define GREEN_PIN   5
#define BLUE_PIN    3

#define ENCODER_PIN_A   2   // Interrupt pin
#define ENCODER_PIN_B   4
#define BUTTON_PIN      7   // Button for selection

LiquidCrystal_I2C lcd(0x27, 16, 2);

// Variables for menu navigation
const int menuLength = 4;  // Total number of menu items
String menuItems[menuLength] = {
  "1. Red LED",
  "2. Green LED",
  "3. Blue LED",
  "4. Adjust Brightness"
};
int menuIndex = 0;    // Current top item index in the menu
int cursorPosition = 0; // 0 or 1, indicates the cursor position on the LCD

// Variables for encoder
volatile int encoderPos = 0;  // Position from encoder interrupts
int lastReportedPos = 0;      // Keep track of last reported position
boolean rotating = false;     // Debounce management

// Variables for LED states
bool redState = false;
bool greenState = false;
bool blueState = false;
int brightness = 255;  // Default brightness

// Debounce variables for button
unsigned long lastButtonPress = 0;
const unsigned long debounceDelay = 200;

// Function prototypes
void updateMenu();
void encoderISR();
void selectMenuItem();
void updateLEDs();

void setup() {
  // Initialize serial communication (optional)
  Serial.begin(9600);

  // Initialize RGB LED pins
  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(BLUE_PIN, OUTPUT);

  // Initialize encoder pins
  pinMode(ENCODER_PIN_A, INPUT_PULLUP);
  pinMode(ENCODER_PIN_B, INPUT_PULLUP);

  // Initialize button pin
  pinMode(BUTTON_PIN, INPUT_PULLUP);

  // Attach interrupts for the encoder
  attachInterrupt(digitalPinToInterrupt(ENCODER_PIN_A), encoderISR, CHANGE);

  // Initialize LCD
  lcd.init();
  lcd.backlight();

  // Display the initial menu
  updateMenu();
}

void loop() {
  // Check if the encoder position has changed
  if (rotating) {
    rotating = false;
    // Update menu based on encoder position
    if (encoderPos > lastReportedPos) {
      // Scrolled down
      cursorPosition++;
      if (cursorPosition > 1) {
        cursorPosition = 1;
        menuIndex++;
        if (menuIndex > menuLength - 2) {
          menuIndex = menuLength - 2;
        }
      }
    } else if (encoderPos < lastReportedPos) {
      // Scrolled up
      cursorPosition--;
      if (cursorPosition < 0) {
        cursorPosition = 0;
        menuIndex--;
        if (menuIndex < 0) {
          menuIndex = 0;
        }
      }
    }
    lastReportedPos = encoderPos;
    updateMenu();
  }

  // Check for button press to select menu item
  if (digitalRead(BUTTON_PIN) == LOW) {
    unsigned long currentTime = millis();
    if (currentTime - lastButtonPress > debounceDelay) {
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

void encoderISR() {
  static unsigned long lastInterruptTime = 0;
  unsigned long interruptTime = millis();
  // Debounce encoder
  if (interruptTime - lastInterruptTime > 5) {
    int MSB = digitalRead(ENCODER_PIN_A);
    int LSB = digitalRead(ENCODER_PIN_B);

    int encoded = (MSB << 1) | LSB;
    if (encoded == 0b11 || encoded == 0b00) {
      encoderPos++;
    } else {
      encoderPos--;
    }
    rotating = true;
  }
  lastInterruptTime = interruptTime;
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

  while (true) {
    if (rotating) {
      rotating = false;
      if (encoderPos > lastReportedPos) {
        brightness += 5;
        if (brightness > 255) brightness = 255;
      } else if (encoderPos < lastReportedPos) {
        brightness -= 5;
        if (brightness < 0) brightness = 0;
      }
      lastReportedPos = encoderPos;
      lcd.setCursor(0, 1);
      lcd.print("     ");  // Clear previous value
      lcd.setCursor(0, 1);
      lcd.print(brightness);
      updateLEDs();
    }

    // Check for button press to exit brightness adjustment
    if (digitalRead(BUTTON_PIN) == LOW) {
      unsigned long currentTime = millis();
      if (currentTime - lastButtonPress > debounceDelay) {
        lastButtonPress = currentTime;
        break;
      }
    }
  }
  // Return to menu
  updateMenu();
}
