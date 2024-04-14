import time
from grove.grove_moisture_sensor import GroveMoistureSensor

from helper import SlotHelper
sh = SlotHelper(SlotHelper.ADC)
pin = sh.argv2pin()

# connect to alalog pin 2(slot A2)
PIN = 2

sensor = GroveMoistureSensor(pin)

print('Detecting moisture...')
while True:
    m = sensor.moisture
    if 0 <= m and m < 300:
        result = 'Dry'
    elif 300 <= m and m < 600:
        result = 'Moist'
    else:
        result = 'Wet'
    print('Moisture value: {0}, {1}'.format(m, result))
    time.sleep(1)