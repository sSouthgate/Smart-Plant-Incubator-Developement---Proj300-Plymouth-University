''' 
This program aims to be used to perform the experiments required to find the relating equation between soil moistuire, it's delta over time and amount of water distributed.
    By opening and closing the solenoid valve for a set interval we can find out how much water is distributed in x amount of seconds.
    This in turn will allow us to calculate the change in moisture overtime when a know amount of water is dispensed.
    We wil be recording the data and exporting it through a generated .csv file.
    This file will allow us to plot a graph of the moisture change overtime with a fixed amount water distributed.
    We will then be able to find the relation between time, water, and moisture, 
    alowing us to know how much water is needed to be distributed over how much time to achieve the disired moisture level.
'''
# IMPORTS
import csv
import os
import time
from datetime import datetime
from adc_sensor import AdcSensor
import RPi.GPIO as GPIO
import mqtt_pub_sub as mqtt
import moisture_control as moisture

# Grove Imports
#from grove_light_sensor_v1_2 import GroveLightSensor
#from grove_moisture_sensor import GroveMoistureSensor

# Set current date and time
current_date_time = datetime.now()

# VARIABLES
t0 = time.time()                            # Current time in s
T = current_date_time.strftime('%H:%M:%S')  # Current Time in Hours:Minutes:Seconds
x = 1                                       # random interger if required

# SETUP RPi GPIO
GPIO_pin = 36                    # Define RPi GPIO GPIO_pin
GPIO.setmode(GPIO.BOARD)    # Set GPIO GPIO_pin numbering system
GPIO.setup(GPIO_pin, GPIO.OUT)   # Set GPIO GPIO_pin mode to output
GPIO.output(GPIO_pin, 0)         # Set GPIO to Low

# Connect sensors to appropriate slots on hat
light_pin = 0
moisture_pin = 2
# Define what grove sensor will be used
moisture_sensor = AdcSensor(moisture_pin)
#light = AdcSensor(light_GPIO_pin)

# MQTT connect the client to the Broker
# sensor_client = mqtt.connect_mqtt("pub_sensor")
# water_client = mqtt.connect_mqtt("sub_water")
# light_client = mqtt.connect_mqtt("sub_light")
# Start the network loop - opens in it's own thread
# sensor_client.loop_start()
# water_client.loop_start()
# light_client.loop_start()
# MQTT topics to publish to
# moisture_topic = "incubator/moisture/value"
# light_topic = "incubator/light/value"

# Set the file path and the headers for the CSV file
file_path = '/home/auzon/Documents/Smart-Plant-Incubator-Code/sensor_log.csv'
headers = ["Moisture Level", "Raw ADC", "Time in s", "Time of Day", "Date"]


# Check if the file exists
if os.path.exists(file_path):
    print("Sensor log file already present, adding to current file")
if not os.path.exists(file_path):
    print("Sensor log file not present, creating file...")
    # If the file doesn't exist, create it and write the headers to it
    with open(file_path, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(headers)
    print("File created")

print('EXPERIMENT START:',T)

# Open and Close Valve
#GPIO.output(GPIO_pin, 1)                                     # Set GPIO_pin High
#time.sleep(x)                                           # Sleep for 1s
#GPIO.output(GPIO_pin, 0)                                     # Set GPIO_pin to Low

# Write to the CSV to identify new test
with open(file_path, 'a', newline='') as file:
                csv_writer = csv.writer(file)                       
                csv_writer.writerow(['NEW TEST'])

n = 1

try:   
    while True: #sensor.light > 10:
            # Set Variables at each start of the loop
            current_date_time = datetime.now()              # Add current Date & Time into a variable
            T = current_date_time.strftime('%H:%M:%S')      # Define T as current Time
            D = current_date_time.strftime('%d/%m')         # Define D as current Date in day/month
            t1 = time.time()                                # Define t1 as current time in seconds
            t1 = t1 - t0                                    # Substract t1(current time in s) from t0(Start time in s of program)
            t1 = round(t1)
                   
            # Load data into variables so that data is consistent across platforms
            m = moisture_sensor.adc_percent
            #l = light.adc_percent
            m1 = round((m / 100) * 3235)

            # Print info to terminal for inspection
            print('Time Elapsed: {0}s'.format(round(t1)))
            print(t1/3600)
            print('Moisture value: {0}%'.format(m))
            print('ADC raw value: {0}'.format(m1))
            #print('Light value: {0}%'.format(l))
            # mqtt.publish(sensor_client, moisture_topic, m)
            # mqtt.publish(sensor_client, light_topic, l)
            
            # Start writing data stream to data file.
            with open(file_path, 'a', newline='') as file:
                writer = csv.writer(file)                       
                writer.writerow([m,m1,round(t1),T,D])   # Sensor Value, Time Elapsed(in s), Current Time, Current Date
            
            if t1 == (n * 3600):
                   GPIO.output(GPIO_pin, 1)
                   time.sleep(1)
                   GPIO.output(GPIO_pin, 0)
                   n = n + 1
            else: 
                time.sleep(1)

# When Ctrl+C is input do this:
except KeyboardInterrupt:
    print('\nTest Terminated by User, Closing Program...')

#sensor_client.loop_stop()
# water_client.loop_stop()
# light_client.loop_stop()

# Reset GPIO GPIO_pins
GPIO.output(GPIO_pin, 0) # Set GPIO GPIO_pin low
GPIO.cleanup        # GPIO Clean Up (rests all GPIO_pins to a neutral state)

# Write to file that program ended
with open(file_path, 'a', newline='') as file:
                csv_writer = csv.writer(file)                       
                csv_writer.writerow(['END OF TEST'])

print('PROGRAM END')