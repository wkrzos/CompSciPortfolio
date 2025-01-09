import time
from PIL import Image, ImageDraw, ImageFont
import lib.oled.SSD1331 as SSD1331
import busio
import board
import adafruit_bme280.advanced as adafruit_bme280
import RPi.GPIO as GPIO

# GPIO button pin
green_button = 6  # Switch to the next view

# Views
VIEW_TEMPERATURE = 0
VIEW_HUMIDITY = 1
VIEW_PRESSURE = 2
views = [VIEW_TEMPERATURE, VIEW_HUMIDITY, VIEW_PRESSURE]
current_view = 0
last_switch_time = time.time()

def draw_temperature(draw, font_large, font_small, temperature):
    draw.rectangle((0, 0, 96, 64), fill="BLACK")
    draw.text((5, 5), "Temperature", font=font_small, fill="WHITE")
    draw.text((5, 25), f"{temperature:.1f}C", font=font_large, fill="RED")
    draw.rectangle((70, 20, 90, 40), fill="RED")

def draw_humidity(draw, font_large, font_small, humidity):
    draw.rectangle((0, 0, 96, 64), fill="BLACK")
    draw.text((5, 5), "Humidity", font=font_small, fill="WHITE")
    draw.text((5, 25), f"{humidity:.1f}%", font=font_large, fill="BLUE")
    draw.ellipse((70, 20, 90, 40), fill="BLUE")

def draw_pressure(draw, font_large, font_small, pressure):
    draw.rectangle((0, 0, 96, 64), fill="BLACK")
    draw.text((5, 5), "Pressure", font=font_small, fill="WHITE")
    draw.text((5, 25), f"{pressure:.1f}hPa", font=font_large, fill="GREEN")
    draw.rectangle((70, 20, 90, 40), outline="WHITE", fill="GREEN")

def display_environmental_data():
    global current_view, last_switch_time

    # Initialize OLED display
    disp = SSD1331.SSD1331()
    disp.Init()
    disp.clear()

    # Initialize BME280 sensor
    i2c = busio.I2C(board.SCL, board.SDA)
    bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, 0x76)

    # Setup GPIO for the button
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(green_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Load fonts
    font_large = ImageFont.truetype("./lib/oled/Font.ttf", 20)
    font_small = ImageFont.truetype("./lib/oled/Font.ttf", 13)

    # Create a blank image for drawing
    image = Image.new("RGB", (disp.width, disp.height), "BLACK")
    draw = ImageDraw.Draw(image)

    def button_callback(channel):
        global current_view, last_switch_time
        current_view = (current_view + 1) % len(views)
        last_switch_time = time.time()

    GPIO.add_event_detect(green_button, GPIO.FALLING, callback=button_callback, bouncetime=200)

    while True:
        current_time = time.time()

        # Cycle views every 10 seconds
        if current_time - last_switch_time >= 10:
            current_view = (current_view + 1) % len(views)
            last_switch_time = current_time

        # Read environmental data
        temperature = bme280.temperature
        humidity = bme280.humidity
        pressure = bme280.pressure

        # Draw the current view
        if current_view == VIEW_TEMPERATURE:
            draw_temperature(draw, font_large, font_small, temperature)
        elif current_view == VIEW_HUMIDITY:
            draw_humidity(draw, font_large, font_small, humidity)
        elif current_view == VIEW_PRESSURE:
            draw_pressure(draw, font_large, font_small, pressure)

        # Display the image on the OLED
        disp.ShowImage(image, 0, 0)
        time.sleep(0.1)

def test():
    print("\nThe OLED environmental display with cycling views test.")
    display_environmental_data()

if __name__ == "__main__":
    try:
        test()
    except KeyboardInterrupt:
        print("\nProgram terminated.")
    finally:
        GPIO.cleanup()
