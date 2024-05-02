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
print(GPIO.input(Light), GPIO.input(Valve))
GPIO.output(Light, False)
GPIO.output(Valve, False)

time.sleep(3)

GPIO.output(Light, True)
GPIO.output(Valve, True)
print(GPIO.input(Light), GPIO.input(Valve))
time.sleep(0.25)
GPIO.output(Light, False)
GPIO.output(Valve, False)
GPIO.cleanup()
#except KeyboardInterrupt:
 #   GPIO.cleanup()
  #  print('\n GPIO Clean up')
   # pass