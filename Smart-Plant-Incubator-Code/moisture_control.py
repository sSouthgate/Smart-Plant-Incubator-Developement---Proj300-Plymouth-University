# IMPORTS
import time
from adc_sensor import AdcSensor
import RPi.GPIO as GPIO

def avg_moisture():
    '''
    Incubator Valve Control
    Args
        PIN(int): RPi GPIO Pin connected to Valve circuit MOSFET
        S(int) : Time that valve remains open in secondss
    '''
    # Define Moisture Sensor Pin Number
    moisture = AdcSensor(2)
    # Variable for while loop
    n = 0
    # ADC value stored in m
    m = 0

    #Loop over 60 iterations and sleep for 60 seconds in each loop - an hour worth of data
    while (n < 60) :
        
        # print('Loop nbr:',n)
        # print('m =', m)
        # print('ADC =', moisture.adc_voltage)
        m = m + moisture.adc_voltage
        n = n + 1
        time.sleep (60)
        # print('Done a sleep')
        # print('after loop \n    m =',m,'\n  ADC =', moisture.adc_voltage)

    # Get the average of the moisture value over 1 hour
    m = m / n
    # Round m to 2 decimal points for consistency with adc_voltage class.
    m = round(m, 2)
    # Return the Value stored in m
    return m


def open_valve(m, threshhold, GPIO_pin):
    '''
    After data manipulation -
    Set the valve GPIO Pin high to open the valve
    '''
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
    else: #m < 2.4:
        GPIO.output(GPIO_pin, 0)
        state = 'Soil is moist - No need to water'
        print('Moisture Level: {0}, {1}'.format(m, state))
    # else:
    #     GPIO.output(GPIO_pin, 0)
    #     state = 'PLANT IS OVERWATERED!!!!'
    #     print('Moisture Level: {0}, {1}'.format(m,state))
    

if __name__ == '__main__':
   m = avg_moisture()
   open_valve(m, 50, 18)
