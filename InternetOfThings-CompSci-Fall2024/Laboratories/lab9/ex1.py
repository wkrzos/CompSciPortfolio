import RPi.GPIO as GPIO
import time

led1 = 13
encoderA = 17
encoderB = 27

def change_brightness(channel):
    global duty_cycle, last_state
    current_state = GPIO.input(encoderA)
    if current_state != last_state:
        if GPIO.input(encoderB) != current_state:
            duty_cycle = min(100, duty_cycle + 2.5)
        else:
            duty_cycle = max(0, duty_cycle - 2.5)

        diode1.ChangeDutyCycle(duty_cycle)
        print(f"Brightness: {duty_cycle}%")

    last_state = current_state


if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(led1, GPIO.OUT)
    GPIO.setup(encoderA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(encoderB, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    try:
        diode1 = GPIO.PWM(led1, 100)
        duty_cycle = 0
        diode1.start(duty_cycle)

        last_state = GPIO.input(encoderA)

        GPIO.add_event_detect(encoderA, GPIO.BOTH, callback=change_brightness)

        print("Program started. Turn the encoder to adjust brightness.")
        while True:
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nProgram terminated.")

    finally:
        diode1.stop()
        GPIO.cleanup()
