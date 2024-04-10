# IMPORTS
import time
from grove_moisture_sensor import GroveMoistureSensor
from grove_light_sensor_v1_2 import GroveLightSensor
import RPi.GPIO as GPIO

def open_valve(PIN,S):
    '''
    Incubator Valve Control
    Args
        PIN(int): RPi GPIO Pin connected to Valve circuit MOSFET
        S(int) : Time that valvel remains open in seconds
    '''
    
    # SETUP RPi GPIO
    GPIO.setmode(GPIO.BOARD)    # Set GPIO Pin numbering system
    GPIO.setup(PIN, GPIO.OUT)   # Set GPIO Pin mode to output
    GPIO.output(PIN, 0)         # Set GPIO to Low

    # Define Moisture Sensor Pin Number
    sensor = GroveMoistureSensor(0)
    #sensor = GroveLightSensor(2)    # For Testing
    m = sensor.moisture             # moisture value stored in m
    #m = sensor.light                # For Testing        
    if m < 300:
        GPIO.output(PIN, 1)
        state = 'Soil Dry, Opening Valve'
        print('Moisture Level: {0}, {1}'.format(m, state))
        time.sleep(S)
        GPIO.output(PIN, 0)
        print('Water Dispensed, Valve Closed')
    else:
        GPIO.output(PIN, 0)
        state = 'SOIL IS MOIST! NO NEED TO WATER!'
        print('Moisture Level: {0}, {1}'.format(m, state))

#open_valve(32, 5)