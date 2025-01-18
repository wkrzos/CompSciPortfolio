import json
import time
import paho.mqtt.client as mqtt

# Optional: if you need access to GPIO or config pins in the subscriber:
# import config

# ----- MQTT Configuration -----
BROKER_ADDRESS = "broker.hivemq.com"
BROKER_PORT = 1883
MQTT_TOPIC = "your_channel/rfid"  # same topic as in publisher.py

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Successfully connected to MQTT broker, return code =", rc)
        client.subscribe(MQTT_TOPIC)
        print(f"Subscribed to topic: {MQTT_TOPIC}")
    else:
        print(f"Connection error, return code = {rc}")

def on_message(client, userdata, msg):
    """
    Callback function for incoming messages.
    Here we parse JSON and optionally save to a file, database, or console.
    """
    try:
        payload_str = msg.payload.decode("utf-8")
        data = json.loads(payload_str)

        card_uid = data.get("card_uid")
        timestamp = data.get("timestamp")

        print(f"[RECEIVED] Card UID: {card_uid}, Timestamp: {timestamp}")

        # Example: log to a local file
        with open("rfid_usage.log", "a", encoding="utf-8") as f:
            f.write(f"{timestamp}, UID={card_uid}\n")

    except Exception as e:
        print(f"Error processing the message: {e}")

def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    print(f"Connecting to MQTT broker at {BROKER_ADDRESS}:{BROKER_PORT}...")
    client.connect(BROKER_ADDRESS, BROKER_PORT, 60)

    # Start the loop to continuously check for incoming messages
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("\nSubscriber program stopped by user.")

if __name__ == "__main__":
    main()
