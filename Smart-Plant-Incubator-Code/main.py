# IMPORTS
import time
from adc_sensor import AdcSensor
import RPi.GPIO as GPIO
import mqtt_pub_sub as mqtt
import moisture_control as moisture
import light_control as light

# SETUP RPi GPIO
led_GPIO = 32                # RPi pin for the LED MOSFET
valve_GPIO = 36              # RPi pin for the Valve MOSFET
GPIO.setmode(GPIO.BOARD)    # Set GPIO Pin numbering system
GPIO.setup([led_GPIO, valve_GPIO], GPIO.OUT)   # Set GPIO Pin mode to output
GPIO.output([led_GPIO, valve_GPIO], 0)         # Set GPIO to Low

# Set Sensor Pins
light_sensor = AdcSensor(0)
moisture_sensor = AdcSensor(2)

# MQTT connect the clients to the Broker
sensor_client = mqtt.connect_mqtt("pub_sensor")
water_client = mqtt.connect_mqtt("sub_water")
light_client = mqtt.connect_mqtt("sub_light")

# Start the network loop - opens in it's own thread
sensor_client.loop_start()
#water_client.loop_start()
light_client.loop_start()

# MQTT topics
moist_state_topic = "incubator/moisture/value"
light_state_topic = "incubator/light/value"
moist_th_topic = "incubator/moisture/threshold"
light_th_topic = "incubator/light/threshold"

# MQTT Subscribing client to defined topic
mqtt.subscribe(water_client, moist_th_topic)
mqtt.subscribe(light_client, light_th_topic)

# Base threshhold variables - to be modified by HA through MQTT payloads
moisture_th = 60
light_th = 50

def moisture_publish(x):
    '''Function to be run on a thread for publishing moisture data
    moisture data is avg moisture over x minutes.
    '''
    # Get avg moisture over x minutes
    m = moisture.avg_moisture_percent(x)
    mqtt.publish(sensor_client, moist_state_topic, m)

def light_publish():
    '''Function to be run on a thread for publishing current light data every second
    '''
    # publish light sensor values every second
    l = light_sensor.adc_percent
    mqtt.publish(sensor_client, light_state_topic, l)
    time.sleep(1)

def moisture_routine(x):
    '''Function to be run on a thread for valve functionality
    Based on avg_moisture_percent over x minutes, deliver the required water amount
    '''
    mqtt.subscribe(water_client, moist_th_topic)
    #moisture_th = mqtt.get_payload(mqtt.water_q)
    #print("WATER TH:", (moisture_th))
    # if moisture_th == None:
    #     moisture_th = 60
    m = moisture.avg_moisture_percent(x)
    moisture.valve_control(m, moisture_th, valve_GPIO)
    mqtt.unsubscribe(water_client, moist_th_topic)

def light_routine():
    '''Function to be run on a thread for light functionality
    Based on avg_light_percent over x minutes, turn the lights on or off
    '''
    mqtt.subscribe(light_client, light_th_topic)
    light_th = mqtt.get_light_payload()
    print("LIGHT TH:", (light_th))
    if light_th == None:
        light_th = 50
    l = light_sensor.adc_percent
    light.light_control(l, light_th, led_GPIO)
    mqtt.unsubscribe(light_client, light_th_topic)



def main():
    # Put each of these in their own threads
    
    # Publish avg moisture values every minute
    moisture_publish(0.016)
    # Publish light values
    light_publish()
    # Avg over an hour
    moisture_routine(0.016)
    # Avg over a second
    light_routine()


try:
    while True:
        
        main()

except KeyboardInterrupt:
    print("\nUser stopped program...")
    print("Closing program...")