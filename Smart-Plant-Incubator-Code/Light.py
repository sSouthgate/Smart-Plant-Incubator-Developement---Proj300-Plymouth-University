# IMPORTS
import time
from grove_light_sensor_v1_2 import GroveLightSensor
import RPi.GPIO as GPIO
from adc_sensor import AdcSensor

def light(PIN,L):
    '''
    Incubator Light Control
    
    Args:
        PIN(int): RPi GPIO Pin connected to Light circuit MOSFET
        L(int): Desired Light Level for lights to turn on
    '''

    # SETUP RPi GPIO
    #PIN = 32                    # Pin used to actovate Valve MOSFET
    GPIO.setmode(GPIO.BOARD)    # Set GPIO Pin numbering system
    GPIO.setup(PIN, GPIO.OUT)   # Set GPIO Pin mode to output
    GPIO.output(PIN, 0)         # Set GPIO to Low
    
    # Define Light Sensor Pin Number
    sensor = AdcSensor(0)
    
    while True:
        if sensor.adc_voltage < L:
            state = 'Low Light Levels, Turning On Lights'
            print('Light Level: {0}, {1}'.format(sensor.adc_voltage, state))
            GPIO.output(PIN, 1)
            time.sleep(1)
        else:
            state = 'Light Levels Nominal, Turning Off Lights'
            print('Light Level: {0}, {1}'.format(sensor.adc_voltage, state))
            GPIO.output(PIN, 0)
            time.sleep(1)

#light(32, 1.33)