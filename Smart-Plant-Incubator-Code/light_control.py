# IMPORTS
import time
from grove_light_sensor_v1_2 import GroveLightSensor
import RPi.GPIO as GPIO
from adc_sensor import AdcSensor

light_mode_voltage = 0
light_mode_percent = 1

def avg_light_mode(x, mode):
    '''
    Avg moisture over x minutes
    mode = 0 for Voltage
    mode = 1 for %
    Return m in V
    '''
    # Define Moisture Sensor Pin Number
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
        
        # Check mode selected
        if mode == light_mode_voltage:
            l = l + light.adc_voltage
        else:
            l = l + light.adc_percent
        #Sleep to help with power managment
        time.sleep (x)

    # Get the average of the moisture value over x minutes
    if n != 0:   
        l = l / n
    
    # Round m to 2 decimal points for consistency with adc_voltage class.
    l = round(l, 2)
    # Return the Value stored in m
    return l

def avg_light(x) :
    '''
    Avg light over x minutes
    Returns l in V (see adc_voltage)
    '''
    return avg_light_mode(x, light_mode_voltage)

def avg_light_percent(x):
    '''
    Avg moisture over x minutes
    Returns m in % (see adc_percent)
    '''
    return avg_light_mode(x, light_mode_percent)

def light_control(l, threshold, GPIO_pin):
    '''
    Incubator Light Control for values in %
    
    Args:
        l(float): current light level
        threshhold(float): light level threshold for lights to turn on
        GPIO_pin(int): RPi GPIO Pin connected to Light circuit MOSFET
    '''

    # SETUP RPi GPIO
    #PIN = 32                    # Pin used to actovate Valve MOSFET
    # GPIO.setmode(GPIO.BOARD)    # Set GPIO Pin numbering system
    # GPIO.setup(GPIO_pin, GPIO.OUT)   # Set GPIO Pin mode to output
    # GPIO.output(GPIO_pin, 0)         # Set GPIO to Low
    
    # Define Light Sensor Pin Number
    sensor = AdcSensor(0)
    
    if l < threshold:
        state = 'Low Light Levels, Turning On Lights'
        print('Light Level: {0}, {1}'.format(l, state))
        GPIO.output(GPIO_pin, 1)
        time.sleep(1)
    else:
        state = 'Light Levels Nominal, Turning Off Lights'
        print('Light Level: {0}, {1}'.format(l, state))
        GPIO.output(GPIO_pin, 0)
        time.sleep(1)

# def light_routine(threshold, x, GPIO_pin):
#     '''Function to be run on a thread for light functionality
#     Based on avg_light_percent over x minutes, turn the lights on or off
#     '''
#     l = avg_light_percent(x)
#     light_control(l, threshold, GPIO_pin)

if __name__ == '__main__':
   while True:
    light = AdcSensor(2)
    l = light.adc_percent
    print(l)
    time.sleep(1)
