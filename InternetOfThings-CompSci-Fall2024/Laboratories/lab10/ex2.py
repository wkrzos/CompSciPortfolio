#!/usr/bin/env python3

import time
import RPi.GPIO as GPIO
from config import *  # buzzerPin, etc.
from mfrc522 import MFRC522
import board
import neopixel
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import lib.oled.SSD1331 as SSD1331

# WS2812 LED setup
NUM_PIXELS = 8
pixels = neopixel.NeoPixel(
    board.D18,  # or another pin, depending on your hardware setup
    NUM_PIXELS,
    brightness=1.0 / 32,
    auto_write=False
)

# Keep track of registered cards
registered_cards = []

def buzzer(state: bool):
    """
    Switch the buzzer on or off.
    - state=True  => ON
    - state=False => OFF

    If your buzzer is active HIGH, remove 'not'.
    If it's active LOW, keep 'not' or invert as needed.
    """
    GPIO.output(buzzerPin, not state)

def triple_feedback(uid, timestamp, delay=2.0):
    """
    Provide simultaneous feedback:
      1) NeoPixel strip turns GREEN
      2) Buzzer ON
      3) OLED shows UID & timestamp

    After `delay` seconds, turn everything OFF.
    """
    print("DEBUG: Entering triple_feedback...")

    # 1) Turn LED ON (Green)
    print("DEBUG: Turning pixels ON (green).")
    pixels.fill((0, 255, 0))
    pixels.show()

    # 2) Turn buzzer ON
    print("DEBUG: Buzzer ON.")
    buzzer(True)

    # 3) Initialize and show on OLED
    print("DEBUG: Initializing OLED.")
    disp = SSD1331.SSD1331()
    disp.Init()
    disp.clear()

    image = Image.new("RGB", (disp.width, disp.height), "BLACK")
    draw = ImageDraw.Draw(image)
    font_small = ImageFont.truetype("./lib/oled/Font.ttf", 9)

    draw.text((5, 5), uid, font=font_small, fill="WHITE")
    draw.text((5, 45), timestamp, font=font_small, fill="WHITE")
    disp.ShowImage(image, 0, 0)

    print(f"DEBUG: Sleeping for {delay} seconds.")
    time.sleep(delay)

    # Turn LED OFF
    print("DEBUG: Turning pixels OFF.")
    pixels.fill((0, 0, 0))
    pixels.show()

    # Buzzer OFF
    print("DEBUG: Buzzer OFF.")
    buzzer(False)

    # Clear OLED
    print("DEBUG: Clearing OLED.")
    disp.clear()
    print("DEBUG: triple_feedback complete.\n")

def rfid_read():
    """
    Continuously read from the MFRC522 RFID reader, respecting a cooldown
    but always providing feedback when a card is scanned.
    """
    MIFAREReader = MFRC522()
    cooldown_time = 5
    cooldown_tracker = {}

    print("Place the card close to the reader.")

    while True:
        (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
        print(f"DEBUG: status={status}, registered_cards={registered_cards}")

        if status == MIFAREReader.MI_OK:
            (status, uid) = MIFAREReader.MFRC522_Anticoll()
            print(f"DEBUG: Anticollision status={status}, uid={uid}")

            if status == MIFAREReader.MI_OK:
                card_uid = "".join([f"{byte:02X}" for byte in uid])
                current_time = time.time()

                # Always show feedback every scan
                # (If you only want feedback on successful logs, move it inside the cooldown check)
                # Create a timestamp for display
                now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                triple_feedback(card_uid, now_str, delay=2.0)

                # Only log if outside cooldown
                if (card_uid not in cooldown_tracker
                        or (current_time - cooldown_tracker[card_uid]) > cooldown_time):
                    cooldown_tracker[card_uid] = current_time
                    registered_cards.append((card_uid, now_str))
                    print(f"Card registered: UID={card_uid}, Time={now_str}")

        time.sleep(0.1)

def test():
    print("\nRFID reader test with buzzer, LED, and OLED feedback.")
    print("Place the card close to the reader (on the right side).")

    try:
        rfid_read()
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    test()
