# IMPORTS
import time
from adc_sensor import AdcSensor
import RPi.GPIO as GPIO

moist_mode_voltage = 0
moist_mode_percent = 1

def avg_moisture_mode(x, mode):
    '''
    Avg moisture over x minutes
    mode = 0 for Voltage
    mode = 1 for %
    Return m in V
    '''
    # Define Moisture Sensor Pin Number
    moisture = AdcSensor(2)
    # Number of loops in average functions
    n = 0
    # ADC value stored in m
    m = 0
    #Define time variables
    t0 = time.time()    #current time
    t1 = 0              #set to 0

    # Loop for x minutues and sleep x seconds in each loop
    while (t1 < (t0 + (x *60))) :
        #Count the amount of loops to make an average
        n = n + 1
        t1 = time.time()    #current time
        
        # Check mode selected
        if mode == moist_mode_voltage:
            m = m + moisture.adc_voltage
        else:
            m = m + moisture.adc_percent
        #Sleep to help with power managment
        time.sleep (x)

    # Get the average of the moisture value over x minutes
    if n != 0:   
        m = m / n
    
    # Round m to 2 decimal points for consistency with adc_voltage class.
    m = round(m, 2)
    # Return the Value stored in m
    return m

def avg_moisture(x) :
    return avg_moisture_mode(x, moist_mode_voltage)


def avg_moisture_percent(x):
    '''
    Avg moisture over x minutes
    Returns m in % (see adc_percent)
    '''
    return avg_moisture_mode(x, moist_mode_percent)

    '''
    DEPRECATED
    '''

    # # Define Moisture Sensor Pin Number
    # moisture = AdcSensor(2)
    # # Number of loops in average functions
    # n = 0
    # # ADC value stored in m
    # m = 0
    # #Define time variables
    # t0 = time.time()    #current time
    # t1 = 0              #set to 0

    # # Loop for x minutues and sleep x seconds in each loop
    # while (t1 < (t0 + (x *60))) :
    #     #Count the amount of loops to make an average
    #     n = n + 1
    #     t1 = time.time()    #current time
    #     m = m + moisture.adc_percent
    #     #print(m)
    #     #Sleep to help with power managment
    #     time.sleep (x)

    # # Get the average of the moisture value over x minutes
    # if n != 0:   
    #     m = m / n
    
    # # Round m to 2 decimal points for consistency with adc_voltage class.
    # m = round(m, 2)
    # # Return the Value stored in m
    # return m


def valve_control(m, threshhold, GPIO_pin):
    '''
    After data manipulation -
    Set the valve GPIO Pin high to open the valve for the required time
    '''

    # SETUP RPi GPIO
    GPIO.setmode(GPIO.BOARD)    # Set GPIO Pin numbering system
    GPIO.setup(GPIO_pin, GPIO.OUT)   # Set GPIO Pin mode to output

    if m < threshhold:
        GPIO.output(GPIO_pin, 1)
        state = 'Soil Dry, Opening Valve'
        print('Moisture Level: {0}.\n{1}'.format(m, state))

        ################################################
       #APPLY CHANGE IN MOISTURE OVER TIME EQUATION HERE#
        ################################################ 
        
        time.sleep(1)
        GPIO.output(GPIO_pin, 0)
        print('Water Dispensed, Valve Closed')
    else:
        GPIO.output(GPIO_pin, 0)
        state = 'Soil is moist - No need to water'
        print('Moisture Level: {0}.\n{1}'.format(m, state))
    
# def moisture_routine(threshold, x, GPIO_pin):
#     '''Function to be run on a thread for valve functionality
#     Based on avg_moisture_percent over x minutes, deliver the required water amount
#     '''
#     m = avg_moisture_percent(x)
#     valve_control(m, threshold, GPIO_pin)


if __name__ == '__main__':
   m = avg_moisture_percent(1)
   print(m)
   #valve_control(m, 50, 36)
