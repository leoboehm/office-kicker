import RPi.GPIO as GPIO
import time
import requests

# GPIO setup
PIR_PIN = 11    # TODO: adjust to actual sensor pin
LED_PIN = 13    # TODO: adjust to actual LED pin
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT)

SERVER_URL = 'https://58457-3000.4.codesphere.com/motion'

def detect_motion():
    while True:
        if GPIO.input(PIR_PIN):
            # turn on LED
            GPIO.output(LED_PIN, GPIO.HIGH)
            try:
                requests.post(SERVER_URL, json={'motion': True})    # post or get?
            except Exception as e:
                print(f"Failed to send data: {e}")
        else:
            # turn off LED
            GPIO.output(LED_PIN, GPIO.LOW)

        time.sleep(1)

if __name__ == "__main__":
    try:
        detect_motion()
    except KeyboardInterrupt:
        GPIO.cleanup()