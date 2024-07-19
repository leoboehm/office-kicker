import RPi.GPIO as GPIO
import time
import requests

# GPIO setup
PIR_PIN = 11
LED_PIN = 12

GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT)

# server url
SERVER_URL = 'https://58457-3000.4.codesphere.com/motion'


def detect_motion():
    while True:
        # check for motion
        if GPIO.input(PIR_PIN):
            # turn on LED
            GPIO.output(LED_PIN, GPIO.HIGH)
            try:
                # send motion state
                requests.get(SERVER_URL)
            except Exception as e:
                print(f"Failed to send data: {e}")
        else:
            # turn off LED
            GPIO.output(LED_PIN, GPIO.LOW)
        
        # update every second
        time.sleep(1)


if __name__ == "__main__":
    try:
        detect_motion()
    except KeyboardInterrupt:
        print("Quit")
        GPIO.cleanup()
