import time
import RPi.GPIO as GPIO
from config import *  # pylint: disable=unused-wildcard-import
from mfrc522 import MFRC522
import board
import neopixel
from datetime import datetime

# GPIO pin for buzzer
buzzer_pin = 18

# WS2812 LED setup
NUM_PIXELS = 8
pixels = neopixel.NeoPixel(board.D18, NUM_PIXELS, brightness=1.0/32, auto_write=False)

def play_buzzer():
    GPIO.output(buzzer_pin, GPIO.HIGH)
    time.sleep(0.2)
    GPIO.output(buzzer_pin, GPIO.LOW)

def visual_feedback():
    pixels.fill((0, 255, 0))  # Green light
    pixels.show()
    time.sleep(0.5)
    pixels.fill((0, 0, 0))  # Turn off LEDs
    pixels.show()

def rfid_read():
    MIFAREReader = MFRC522()
    registered_cards = set()  # Keep track of already registered UIDs

    print("Place the card close to the reader.")

    while True:
        (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        if status == MIFAREReader.MI_OK:
            (status, uid) = MIFAREReader.MFRC522_Anticoll()

            if status == MIFAREReader.MI_OK:
                # Combine UID to a single number for easier identification
                card_uid = "".join([f"{byte:02X}" for byte in uid])

                if card_uid not in registered_cards:
                    registered_cards.add(card_uid)  # Register the card
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    # Log the card UID and timestamp
                    print(f"Card registered: UID={card_uid}, Time={timestamp}")

                    # Trigger feedback
                    play_buzzer()
                    visual_feedback()

                    # Simulate delay to avoid multiple registrations
                    time.sleep(1)

def test():
    print("\nThe RFID reader test with buzzer and LED feedback.")
    print("Place the card close to the reader (on the right side of the set).")

    # Setup GPIO for buzzer
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(buzzer_pin, GPIO.OUT)

    try:
        rfid_read()
    except KeyboardInterrupt:
        print("\nProgram terminated.")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    test()
