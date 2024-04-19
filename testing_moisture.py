import time
from test_adc_read import GroveTest

from helper import SlotHelper
sh = SlotHelper(SlotHelper.ADC)
pin = sh.argv2pin()

# connect to alalog pin 2(slot A2)
PIN = 2

sensor = GroveTest(pin)

print('Detecting moisture...')
while True:
    n = float
    m = sensor.moisture
    n = (3300 / 4095) * m
    n = round(n / 1000,2 )
    #if 0 <= m and m < 300:
    #    result = 'Dry'
    #elif 300 <= m and m < 600:
    #    result = 'Moist'
    #else:
    #    result = 'Wet'
    print('Moisture value: {0}'.format(n))
    time.sleep(1)