from adc import ADC
import time

class AdcSensor:
    '''
    Grove Moisture Sensor class

    Args:
        pin(int): number of analog pin/channel the sensor connected.
    '''
    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC()

    @property
    def adc_sensor(self):
        '''
        Get the moisture strength value/voltage

        Returns:
            (int): voltage, in mV
        '''
        value = self.adc.read_raw(self.channel)
        return value

Grove = AdcSensor




def main():
    from helper import SlotHelper
    sh = SlotHelper(SlotHelper.ADC)
    pin = sh.argv2pin()

    sensor = AdcSensor(pin)

    print('Reading voltage...')
    while True:
        s = sensor.adc_sensor
        s = (3300 / 4095) * s
        s = round(s / 1000,2)
        print('ADC value: {0}V'.format(s))
        time.sleep(1)

if __name__ == '__main__':
    main()