# Imports
import RPi.GPIO as GPIO
import time

# Set GPIO Pin numbering system
GPIO.setmode(GPIO.BOARD)
# Set GPIO Pin mode
GPIO.setup(18, GPIO.OUT)

while True:
    GPIO.output(18, True)
    time.sleep(1)
#except KeyboardInterrupt:
 #   GPIO.cleanup()
  #  print('\n GPIO Clean up')
   # pass