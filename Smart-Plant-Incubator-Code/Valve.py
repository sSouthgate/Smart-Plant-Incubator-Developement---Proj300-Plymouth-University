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
    
    # SETUP RPi GPIO
    # GPIO.setmode(GPIO.BOARD)    # Set GPIO Pin numbering system
    # GPIO.setup(PIN, GPIO.OUT)   # Set GPIO Pin mode to output
    # GPIO.output(PIN, 0)         # Set GPIO to Low

    # Define Moisture Sensor Pin Number
    moisture = AdcSensor(2)
    
    # Variable for while loop
    n = 0
    # ADC value stored in m
    m = 0

    #Loop over 60 iterations and sleep for 6 seconds in each loop - an hour worth of data
    while (n < 60) :
        
        print('Loop nbr:',n)
        print('m =', m)
        print('ADC =', moisture.adc_sensor)
        m = m + moisture.adc_sensor
        n = n + 1
        time.sleep (60)
        print('Done a sleep')
        print('after loop \n    m =',m,'\n  ADC =', moisture.adc_sensor)

    # Get the average of the moisture value over 1 hour
    m = m / n
    # Round m to 2 decimal points for consistency with adc_sensor class.
    m = round(m, 2)
    
 # If loop logic dependent on moisture level set PIN high or low
    if m < 1.6:
        #GPIO.output(PIN, 1)
        state = 'Soil Dry, Opening Valve'
        print('Moisture Level: {0}.\n{1}'.format(m, state))
        time.sleep(1)
        #GPIO.output(PIN, 0)
        print('Water Dispensed, Valve Closed')
    elif m < 2.0:
        #GPIO.output(PIN, 0)
        state = 'Soil is moist - No need to water'
        print('Moisture Level: {0}, {1}'.format(m, state))
    else:
        #GPIO.output(PIN, 0)
        state = 'PLANT IS OVERWATERED!!!!'
        print('Moisture Level: {0}, {1}'.format(m,state))

    
    # Return the Value stored in m
    return m
#valve(32, 5)

if __name__ == '__main__':
   avg_moisture()