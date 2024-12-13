import time
import os
import board
import neopixel
import RPi.GPIO as GPIO
import w1thermsensor
import busio
import adafruit_bme280.advanced as adafruit_bme280
import sys

# GPIO button pins
red_button = 22  # Switch to thermometer mode
green_button = 23  # Switch to hygrometer mode

# Initialize WS2812 LED strip
NUM_PIXELS = 8
pixels = neopixel.NeoPixel(board.D18, NUM_PIXELS, brightness=1.0/32, auto_write=False)

# Sensor initialization
ds18b20_sensor = w1thermsensor.W1ThermSensor()
i2c = busio.I2C(board.SCL, board.SDA)
bme280_sensor = adafruit_bme280.Adafruit_BME280_I2C(i2c, 0x76)

# Modes
mode = "thermometer"
last_switch_time = time.time()
temp_offset = 20  # Default starting point for thermometer

def update_thermometer():
    global temp_offset
    temperature = ds18b20_sensor.get_temperature()
    pixels.fill((0, 0, 0))  # Turn off all LEDs
    
    # Map temperature to LEDs
    for i in range(NUM_PIXELS):
        if temp_offset + i <= temperature:
            if i < 3:
                pixels[i] = (0, 0, 255)  # Blue
            elif i < 5:
                pixels[i] = (0, 255, 0)  # Green
            else:
                pixels[i] = (255, 0, 0)  # Red
    pixels.show()
    print(f"Thermometer Mode: Temperature = {temperature:.1f}°C")

def update_hygrometer():
    humidity = bme280_sensor.humidity
    pixels.fill((0, 0, 0))  # Turn off all LEDs

    # Map humidity to LEDs
    for i in range(NUM_PIXELS):
        if 10 + i * 10 <= humidity:
            if i < 3:
                pixels[i] = (255, 0, 0)  # Red
            elif i < 6:
                pixels[i] = (0, 255, 0)  # Green
            else:
                pixels[i] = (0, 0, 255)  # Blue
    pixels.show()
    print(f"Hygrometer Mode: Humidity = {humidity:.1f}%")

def button_callback(channel):
    global mode, last_switch_time
    if channel == red_button:
        mode = "thermometer"
    elif channel == green_button:
        mode = "hygrometer"
    last_switch_time = time.time()  # Reset the switch timer
    print(f"Switched to {mode} mode.")

def console_adjustment():
    global temp_offset
    while True:
        command = input("Enter 'up' to increase or 'down' to decrease the temperature range, or 'exit' to quit console: ")
        if command.lower() == 'up':
            temp_offset += 1
            print(f"Temperature range offset increased. New offset: {temp_offset}")
        elif command.lower() == 'down':
            temp_offset -= 1
            print(f"Temperature range offset decreased. New offset: {temp_offset}")
        elif command.lower() == 'exit':
            print("Exiting console adjustment.")
            break
        else:
            print("Invalid command. Please enter 'up', 'down', or 'exit'.")

if __name__ == "__main__":
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(red_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(green_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(red_button, GPIO.FALLING, callback=button_callback, bouncetime=200)
        GPIO.add_event_detect(green_button, GPIO.FALLING, callback=button_callback, bouncetime=200)

        print("Program started. Use buttons to switch modes or open the console for adjustments.")

        while True:
            current_time = time.time()
            if current_time - last_switch_time >= 10:
                # Automatically switch modes every 10 seconds
                mode = "hygrometer" if mode == "thermometer" else "thermometer"
                last_switch_time = current_time
                print(f"Automatically switched to {mode} mode.")

            if mode == "thermometer":
                update_thermometer()
            elif mode == "hygrometer":
                update_hygrometer()

            # Non-blocking console adjustment check
            if os.name == 'posix':
                import select
                if select.select([sys.stdin], [], [], 0)[0]:
                    console_adjustment()
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nProgram terminated.")

    finally:
        pixels.fill((0, 0, 0))
        pixels.show()
        GPIO.cleanup()
