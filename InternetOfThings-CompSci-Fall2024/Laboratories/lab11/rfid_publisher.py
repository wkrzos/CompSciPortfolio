#!/usr/bin/env python3

import time
import RPi.GPIO as GPIO
from mfrc522 import MFRC522
from datetime import datetime
import paho.mqtt.client as mqtt

# Import config & buzzer logic
import config
from config import led1  # We'll use led1 for the visual feedback
from buzzer import buzzer

# ----- MQTT Configuration -----
BROKER_ADDRESS = "broker.hivemq.com"
BROKER_PORT = 1883
MQTT_TOPIC = "your_channel/rfid"  # same topic as in subscriber.py

client = mqtt.Client()

def connect_mqtt():
    """Connect to the MQTT broker."""
    client.connect(BROKER_ADDRESS, BROKER_PORT, 60)
    print(f"Connected to MQTT broker at {BROKER_ADDRESS}:{BROKER_PORT}")

def publish_rfid(uid, timestamp):
    """
    Publish the RFID UID and timestamp via MQTT.
    """
    payload = {
        "card_uid": uid,
        "timestamp": timestamp
    }
    import json
    client.publish(MQTT_TOPIC, json.dumps(payload))
    print(f"[MQTT] Sent data: {payload}")

def beep(duration=0.2):
    """
    Produce a short beep using the 'buzzer' function from buzzer.py.
    """
    buzzer(True)              # Turn buzzer ON
    time.sleep(duration)      # Wait
    buzzer(False)             # Turn buzzer OFF

def flash_led(led_pin, duration=0.5):
    """
    Short visual signal on the specified LED pin.
    """
    GPIO.output(led_pin, GPIO.HIGH)
    time.sleep(duration)
    GPIO.output(led_pin, GPIO.LOW)

def main():
    # Connect to MQTT
    connect_mqtt()

    reader = MFRC522()
    registered_cards = set()

    print("Please place the RFID card near the reader...")

    try:
        while True:
            (status, TagType) = reader.MFRC522_Request(reader.PICC_REQIDL)
            if status == reader.MI_OK:
                (status, uid) = reader.MFRC522_Anticoll()
                if status == reader.MI_OK:
                    card_uid = "".join([f"{byte:02X}" for byte in uid])

                    # Check if this card was already read
                    if True: #card_uid not in registered_cards
                        registered_cards.add(card_uid)

                        # Current timestamp
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        print(f"Card read: UID={card_uid}, Time={timestamp}")

                        # Publish to MQTT
                        publish_rfid(card_uid, timestamp)

                        # Audible + visual feedback
                        beep(0.2)
                        flash_led(led1, 0.3)

                        # Prevent multiple reads of the same card
                        time.sleep(1)

            # A small sleep to avoid 100% CPU usage
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nProgram stopped by user.")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
