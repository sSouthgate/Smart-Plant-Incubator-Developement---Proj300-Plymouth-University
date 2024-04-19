# Imports
import RPi.GPIO as GPIO
import time

#Define Pin number
Light = 32
Valve = 36
# Set GPIO Pin numbering system
GPIO.setmode(GPIO.BOARD)
# Set GPIO Pin mode
GPIO.setup(Light, GPIO.OUT)
GPIO.setup(Valve, GPIO.OUT)
GPIO.output(Light, False)
GPIO.output(Valve, False)

GPIO.output(Light, True)
GPIO.output(Valve, True)
print(GPIO.input(Light), GPIO.input(Valve))
time.sleep(1)
GPIO.output(Light, False)
GPIO.output(Valve, False)
GPIO.cleanup()
#except KeyboardInterrupt:
 #   GPIO.cleanup()
  #  print('\n GPIO Clean up')
   # pass