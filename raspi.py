import RPi.GPIO as GPIO
import time
import requests

# GPIO setup
PIR_PIN = 11  # TODO: adapt to actual sensor pin
LED_PIN = 13  # TODO: adapt to actual LED pin

GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT)

# server url
FLASK_SERVER_URL = 'https://58457-3000.4.codesphere.com/motion'


def detect_motion():
    while True:
        
        # check for motion
        if GPIO.input(PIR_PIN):
            # turn on LED
            GPIO.output(LED_PIN, GPIO.HIGH)
            try:
                # set motion state to true
                requests.post(FLASK_SERVER_URL, json={'motion': True})
            except Exception as e:
                print(f"Failed to send data: {e}")

        else:
            # turn off LED
            GPIO.output(LED_PIN, GPIO.LOW)
            try:
                # set motion state to false
                requests.post(FLASK_SERVER_URL, json={'motion': False}) 
            except Exception as e:
                print(f"Failed to send data: {e}")
        
        # update every 10 secs
        time.sleep(10)


if __name__ == "__main__":
    try:
        detect_motion()
    except KeyboardInterrupt:
        print("Quit")
        GPIO.cleanup()
