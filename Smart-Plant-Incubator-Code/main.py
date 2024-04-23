# IMPORTS
import time
from datetime import datetime
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

# MQTT connect the clients to the Broker
sensor_client = mqtt.connect_mqtt("pub_sensor")
water_client = mqtt.connect_mqtt("sub_water")
light_client = mqtt.connect_mqtt("sub_light")

# Start the network loop - opens in it's own thread
sensor_client.loop_start()
water_client.loop_start()
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

try:
    while True:
        m = moisture.avg_moisture_percent(0.02)
        l = light.avg_light_percent(0.02)
        mqtt.publish(sensor_client, moist_state_topic, m)
        mqtt.publish(sensor_client, light_state_topic, l)
        
except KeyboardInterrupt:
    print("\nUser stopped program...")
    print("Closing program...")