# IMPORTS
import time
from grove_light_sensor_v1_2 import GroveLightSensor
import RPi.GPIO as GPIO
from adc_sensor import AdcSensor

def avg_light(x):
    '''
    Avg moisture over x minutes
    Returns m in V
    '''
    # Define light Sensor Pin Number
    light = AdcSensor(0)
    # Number of loops in average functions
    n = 0
    # ADC value stored in m
    l = 0
    #Define time variables
    t0 = time.time()    #current time
    t1 = 0              #set to 0

    # Loop for x minutues and sleep x seconds in each loop
    while (t1 < (t0 + (x *60))) :
        #Count the amount of loops to make an average
        n = n + 1
        t1 = time.time()    #current time
        l = l + light.adc_voltage
        #Sleep to help with power managment
        time.sleep (x)

    # Get the average of the moisture value over x minutes
    l = l / n
    # Round m to 2 decimal points for consistency with adc_voltage class.
    l = round(l, 2)
    # Return the Value stored in m
    return l


def avg_light_percent(x):
    '''
    Avg moisture over x minutes
    Returns m in % (see adc_percent)
    '''
    # Define light Sensor Pin Number
    light = AdcSensor(0)
    # Number of loops in average functions
    n = 0
    # ADC value stored in m
    l = 0
    #Define time variables
    t0 = time.time()    #current time
    t1 = 0              #set to 0

    # Loop for x minutues and sleep x seconds in each loop
    while (t1 < (t0 + (x *60))) :
        #Count the amount of loops to make an average
        n = n + 1
        t1 = time.time()    #current time
        l = l + light.adc_percent
        print(l)
        #Sleep to help with power managment
        time.sleep (x)

    # Get the average of the moisture value over x minutes
    l = l / n
    # Round m to 2 decimal points for consistency with adc_voltage class.
    l = round(l, 2)
    # Return the Value stored in m
    return l


def light_control(l, threshold, GPIO_pin):
    '''
    Incubator Light Control
    
    Args:
        PIN(int): RPi GPIO Pin connected to Light circuit MOSFET
        L(int): Desired Light Level for lights to turn on
    '''

    # SETUP RPi GPIO
    #PIN = 32                    # Pin used to actovate Valve MOSFET
    GPIO.setmode(GPIO.BOARD)    # Set GPIO Pin numbering system
    GPIO.setup(GPIO_pin, GPIO.OUT)   # Set GPIO Pin mode to output
    GPIO.output(GPIO_pin, 0)         # Set GPIO to Low
    
    # Define Light Sensor Pin Number
    sensor = AdcSensor(0)
    
    if l < threshold:
        state = 'Low Light Levels, Turning On Lights'
        print('Light Level: {0}, {1}'.format(sensor.adc_voltage, state))
        GPIO.output(GPIO_pin, 1)
        time.sleep(1)
    else:
        state = 'Light Levels Nominal, Turning Off Lights'
        print('Light Level: {0}, {1}'.format(sensor.adc_voltage, state))
        GPIO.output(GPIO_pin, 0)
        time.sleep(1)

# def light_routine(threshold, x, GPIO_pin):
#     '''Function to be run on a thread for light functionality
#     Based on avg_light_percent over x minutes, turn the lights on or off
#     '''
#     l = avg_light_percent(x)
#     light_control(l, threshold, GPIO_pin)

if __name__ == '__main__':
   l = avg_light_percent(1)
   print(l)
   light_control(l, 50, 32)
