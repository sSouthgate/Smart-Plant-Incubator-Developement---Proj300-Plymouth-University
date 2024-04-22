# IMPORTS
import csv
import os
import time
from datetime import datetime
from adc_sensor import AdcSensor
import RPi.GPIO as GPIO
import mqtt_pub

# SETUP RPi GPIO
led_pin = 32                # RPi pin for the LED MOSFET
valve_pin = 36              # RPi pin for the Valve MOSFET
GPIO.setmode(GPIO.BOARD)    # Set GPIO Pin numbering system
GPIO.setup(led_pin, valve_pin, GPIO.OUT)   # Set GPIO Pin mode to output
GPIO.output(led_pin, valve_pin, 0)         # Set GPIO to Low

# Connect sensors to appropriate slots on hat
light_pin = 0
moisture_pin = 2
# Define what grove sensor will be used
moisture = AdcSensor(moisture_pin)
light = AdcSensor(light_pin)

# MQTT connect the publisher to the Broker
client = mqtt_pub.connect_mqtt()
#Start the network loop - opens in it's own thread
client.loop_start()
# MQTT topics to publish to
moisture_topic = "incubator/moisture"
light_topic = "incubator/light"