import time
import RPi.GPIO as GPIO
from mfrc522 import MFRC522
from datetime import datetime

import paho.mqtt.client as mqtt

# ----- GPIO Configuration -----
GPIO.setmode(GPIO.BCM)

BUZZER_PIN = 18
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# Optionally, use PWM for a passive buzzer.
# If you have an active buzzer, simply toggle GPIO HIGH/LOW.
buzzer_pwm = GPIO.PWM(BUZZER_PIN, 2000)  # ~2 kHz frequency
buzzer_pwm.stop()

# LED (or any visual indicator) on GPIO pin 23
LED_PIN = 23
GPIO.setup(LED_PIN, GPIO.OUT)

# ----- Helper Functions -----
def beep(duration=0.2):
    """
    Produce a short beep.
    If the buzzer is passive, use PWM; if active, use HIGH/LOW.
    """
    # --- Passive buzzer (PWM) ---
    buzzer_pwm.start(50)     # 50% duty cycle
    time.sleep(duration)
    buzzer_pwm.stop()

    # --- Active buzzer example (comment out the PWM if using this) ---
    # GPIO.output(BUZZER_PIN, GPIO.HIGH)
    # time.sleep(duration)
    # GPIO.output(BUZZER_PIN, GPIO.LOW)

def flash_led(duration=0.5):
    """
    Short visual signal on the LED.
    """
    GPIO.output(LED_PIN, GPIO.HIGH)
    time.sleep(duration)
    GPIO.output(LED_PIN, GPIO.LOW)

# ----- MQTT Configuration -----
BROKER_ADDRESS = "broker.hivemq.com"
BROKER_PORT = 1883
MQTT_TOPIC = "your_channel/rfid"  # example MQTT topic

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
    # Send as a JSON string
    import json
    client.publish(MQTT_TOPIC, json.dumps(payload))
    print(f"[MQTT] Sent data: {payload}")

def main():
    """
    Main loop: read RFID cards and publish data over MQTT.
    """
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

                    # Check if the card was already read (avoid duplicates if the card stays in place)
                    if card_uid not in registered_cards:
                        registered_cards.add(card_uid)

                        # Get current timestamp
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        print(f"Card read: UID={card_uid}, Time={timestamp}")

                        # Publish to MQTT
                        publish_rfid(card_uid, timestamp)

                        # Audible + visual feedback
                        beep(0.2)
                        flash_led(0.3)

                        # Small delay to prevent multiple reads of the same card
                        time.sleep(1)

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nProgram stopped by user.")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
