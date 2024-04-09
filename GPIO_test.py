# Imports
import RPi.GPIO as GPIO
import time

#Define Pin number
PIN = 18
# Set GPIO Pin numbering system
GPIO.setmode(GPIO.BOARD)
# Set GPIO Pin mode
GPIO.setup(PIN, GPIO.OUT)
GPIO.output(PIN, False)

GPIO.output(PIN, True)
print(GPIO.input(PIN))
time.sleep(1)
GPIO.output(PIN, False)
GPIO.cleanup()
#except KeyboardInterrupt:
 #   GPIO.cleanup()
  #  print('\n GPIO Clean up')
   # pass