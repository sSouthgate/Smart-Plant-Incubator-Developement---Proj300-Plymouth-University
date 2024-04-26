# IMPORTS
import threading
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
water_client.loop_start()
light_client.loop_start()

# MQTT topics
moist_state_topic = "incubator/moisture/value"
light_state_topic = "incubator/light/value"
moist_th_topic = "incubator/moisture/threshold"
light_th_topic = "incubator/light/threshold"

# MQTT Subscribing client to defined topic
# mqtt.subscribe(water_client, moist_th_topic)
# mqtt.subscribe(light_client, light_th_topic)

# Default values for moisture and light threshold
moisture_default = 60
light_default = 50
# Base threshhold variables - to be modified by HA through MQTT payloads
moisture_th = moisture_default
light_th = light_default

# Thread Event Flag
kb_interupt = threading.Event()
kb_interupt.set()

def moisture_publish(x):
    '''Function to be run on a thread for publishing moisture data
    moisture data is avg moisture over x minutes.
    '''
    if kb_interupt.is_set():
        while True:
            # Get avg moisture over x minutes
            m = moisture.avg_moisture_percent(x)
            mqtt.publish(sensor_client, moist_state_topic, m)

def light_publish(x):
    
    '''Function to be run on a thread for publishing current light data every second
    '''
    if kb_interupt.is_set():
        while True:
            # publish light sensor values every second
            l = light.avg_light_percent(x)
            mqtt.publish(sensor_client, light_state_topic, l)

def moisture_routine(x):
    '''Function to be run on a thread for valve functionality
    Based on avg_moisture_percent over x minutes, deliver the required water amount
    '''
    if kb_interupt.is_set():
        while True:
            # Sub to topic at start of each loop to get threshold
            # will provite a new value each time beacause retain flag is true
            mqtt.subscribe(water_client, moist_th_topic)
            time.sleep(0.25)
            moisture_th = mqtt.get_payload(mqtt.water_q, moisture_default)
            print("Moist. Threashold = ", (moisture_th))
            m = moisture.avg_moisture_percent(x)
            moisture.valve_control(m, moisture_th, valve_GPIO)
            mqtt.unsubscribe(water_client, moist_th_topic)

def light_routine(x):
    '''Function to be run on a thread for light functionality
    Based on avg_light_percent over x minutes, turn the lights on or off
    '''
    if kb_interupt.is_set():
        while True:
            # Sub to topic at start of each loop to get threshold
            # will provite a new value each time beacause retain flag is true
            mqtt.subscribe(light_client, light_th_topic)
            time.sleep(0.25)
            light_th = mqtt.get_payload(mqtt.light_q, light_default)
            print("Light Threashold = ", (light_th))
            l = light.avg_light_percent(x)
            light.light_control(l, light_th, led_GPIO)
            mqtt.unsubscribe(light_client, light_th_topic)



def start_up():
    # Put each of these in their own threads
    t1 = threading.Thread(target=moisture_publish, args=[0.016], daemon=True)
    t2 = threading.Thread(target=light_publish, args=[0.016], daemon=True)
    t3 = threading.Thread(target=moisture_routine, args=[0.016], daemon=True)
    t4 = threading.Thread(target=light_routine, args=[0.016], daemon=True)
    
    
    # Publish avg moisture values every x minutes    
    # moisture_publish(0.016)

    # # Publish avg light values every x minutes
    # light_publish(0.016)
    
    # # Run based off of the Avg over an hour
    # moisture_routine(0.016)

    # # Run based off of the Avg over a minute
    # light_routine(0.016)

    t1.start()
    t2.start()
    t3.start()
    t4.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Closing Threads...")
        kb_interupt.clear()
        GPIO.output(led_GPIO, False)
        GPIO.output(valve_GPIO, False)
        GPIO.cleanup()
        print("\nUser stopped program...")
        print("Closing program...")

if __name__ == "__main__":
    start_up()