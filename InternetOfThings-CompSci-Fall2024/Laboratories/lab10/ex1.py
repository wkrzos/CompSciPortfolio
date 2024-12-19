import time
from PIL import Image, ImageDraw, ImageFont
import lib.oled.SSD1331 as SSD1331
import busio
import board
import adafruit_bme280.advanced as adafruit_bme280

def oled_environment_display():
    # Initialize OLED display
    disp = SSD1331.SSD1331()
    disp.Init()
    disp.clear()

    # Initialize BME280 sensor
    i2c = busio.I2C(board.SCL, board.SDA)
    bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, 0x76)

    # Create blank image for drawing
    image = Image.new("RGB", (disp.width, disp.height), "BLACK")
    draw = ImageDraw.Draw(image)

    # Load fonts
    font_large = ImageFont.truetype("./lib/oled/Font.ttf", 20)
    font_small = ImageFont.truetype("./lib/oled/Font.ttf", 13)

    while True:
        # Read environmental parameters
        temperature = bme280.temperature
        humidity = bme280.humidity
        pressure = bme280.pressure

        # Clear previous drawing
        draw.rectangle((0, 0, disp.width, disp.height), fill="BLACK")

        # Draw temperature with icon
        draw.text((5, 5), "Temp:", font=font_small, fill="WHITE")
        draw.text((60, 5), f"{temperature:.1f}C", font=font_small, fill="WHITE")
        draw.rectangle((10, 25, 30, 45), fill="RED")  # Simple thermometer icon

        # Draw humidity with icon
        draw.text((5, 50), "Hum:", font=font_small, fill="WHITE")
        draw.text((60, 50), f"{humidity:.1f}%", font=font_small, fill="WHITE")
        draw.ellipse((10, 70, 30, 90), fill="BLUE")  # Simple water droplet icon

        # Draw pressure with icon
        draw.text((5, 95), "Pres:", font=font_small, fill="WHITE")
        draw.text((60, 95), f"{pressure:.1f}hPa", font=font_small, fill="WHITE")
        draw.rectangle((10, 115, 30, 135), outline="WHITE", fill="WHITE")  # Simple barometer icon

        # Display image on OLED
        disp.ShowImage(image, 0, 0)
        time.sleep(1)

def test():
    print("\nThe OLED environmental display test.")
    oled_environment_display()

if __name__ == "__main__":
    test()
