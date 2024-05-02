from adc import ADC
import time

class AdcSensor:
    '''
    AdcSensor class - reads the raw ADC value and minipulates it to give Voltage (in V).
    Based on known input voltage - in this case 3.3V

    Args:
        pin(int): number of analog pin/channel the sensor connected.
    '''
    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC()

    @property
    def adc_voltage(self):
        '''
        Read the ADC value - 
        Divide the input Voltage(3.3V) by the maximum ADC Value (4095) times the ADC. Then devide by 1k.
        Returns:
            (int): voltage, in V
        '''
        value = self.adc.read_raw(self.channel)
        value = (3300 / 4095) * value
        value = round(value/1000, 2)
        return value
    
    @property
    def adc_percent(self):
        '''
        Read the ADC value - 
        Divide the value by the maximum *OBSERVED* ADC Value (3235) times 100.
        Returns:
            (int): voltage%
        '''
        value = self.adc.read_raw(self.channel)
        value = (value / 3235) * 100
        value = round(value, 2)
        return value
    
    @property
    def real_adc_percent(self):
        '''
        Read the ADC value - 
        Divide the value by the maximum ADC Value (4095) times 100.
        Returns:
            (int): voltage%
        '''
        value = self.adc.read_raw(self.channel)
        value = (value / 4095) * 100
        value = round(value, 2)
        return value

    @property
    def adc_raw(self):

        value = self.adc.read_raw(self.channel)
        return value


#Grove = AdcSensor

def run():
    from helper import SlotHelper
    sh = SlotHelper(SlotHelper.ADC)
    pin = sh.argv2pin()
    #pin = 0    # This is for debugging - comment out the above line

    sensor = AdcSensor(pin)

    print('Reading voltage...')
    while True:
        print('ADC raw: {0}'.format(sensor.adc_raw))
        print('ADC value: {0}V'.format(sensor.adc_voltage))
        print('ADC value: {0}%'.format(sensor.adc_percent))
        time.sleep(1)

if __name__ == '__main__':
    run()