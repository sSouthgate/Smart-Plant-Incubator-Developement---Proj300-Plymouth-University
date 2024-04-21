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
import mqtt_pub

# Grove Imports
#from grove_light_sensor_v1_2 import GroveLightSensor
#from grove_moisture_sensor import GroveMoistureSensor

# Set current date and time
current_date_time = datetime.now()

# VARIABLES
t0 = time.time()                            # Current time in s
T = current_date_time.strftime('%H:%M:%S')  # Current Time in Hours:Minutes:Seconds
x = 1                                       # Time Valve will be open

# SETUP RPi GPIO
PIN = 32                    # Define RPi GPIO PIN
GPIO.setmode(GPIO.BOARD)    # Set GPIO Pin numbering system
GPIO.setup(PIN, GPIO.OUT)   # Set GPIO Pin mode to output
GPIO.output(PIN, 0)         # Set GPIO to Low

# Connect sensors to appropriate slots on hat
light_Pin = 0
moisture_Pin = 2
# Define what grove sensor will be used
moisture = AdcSensor(moisture_Pin)
light = AdcSensor(light_Pin)

# MQTT connect the publisher to the Broker
client = mqtt_pub.connect_mqtt()
#Start the network loop - opens in it's own thread
client.loop_start()

# Set the file path and the headers for the CSV file
file_path = '/home/auzon/Documents/Smart-Plant-Incubator-Code/sensor_log.csv'
headers = ["Moisture Level", "Light Levels", "Time in s", "Time of Day", "Date"]

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
#GPIO.output(PIN, 1)                                     # Set Pin High
#time.sleep(x)                                           # Sleep for 1s
#GPIO.output(PIN, 0)                                     # Set Pin to Low

# Write to the CSV to identify new test
with open(file_path, 'a', newline='') as file:
                csv_writer = csv.writer(file)                       
                csv_writer.writerow(['NEW TEST'])


try:   
    while True: #sensor.light > 10:
            # Set Variables at each start of the loop
            current_date_time = datetime.now()              # Add current Date & Time into a variable
            T = current_date_time.strftime('%H:%M:%S')      # Define T as current Time
            D = current_date_time.strftime('%d/%m')         # Define D as current Date in day/month
            t1 = time.time()                                # Define t1 as current time in seconds
            t1 = t1 - t0                                    # Substract t1(current time in s) from t0(Start time in s of program)
            
            m = moisture.adc_sensor
            #m = (3300 / 4095) * m
            #m = round(m / 1000,2)

            # Print info to terminal for inspection
            print('Time Elapsed: {0}s'.format(round(t1)))
            print('Moisture value: {0}V'.format(m))
            print('Light value: {0}V'.format(light.adc_sensor))
            mqtt_pub.publish(client, "incubator/light", light.adc_sensor)
            mqtt_pub.publish(client, "incubator/moisture", moisture.adc_sensor)
            
            # Start writing data stream to data file.
            with open(file_path, 'a', newline='') as file:
                writer = csv.writer(file)                       
                writer.writerow([m,light.adc_sensor,round(t1),T,D])   # Sensor Value, Time Elapsed(in s), Current Time, Current Date
                time.sleep(1)

# When Ctrl+C is input do this:
except KeyboardInterrupt:
    print('\nTest Terminated by User, Closing Program...')

# MQTT stop network loop
client.loop_stop()

# Reset GPIO pins
GPIO.output(PIN, 0) # Set GPIO pin low
GPIO.cleanup        # GPIO Clean Up (rests all pins to a neutral state)

# Write to file that program ended
with open(file_path, 'a', newline='') as file:
                csv_writer = csv.writer(file)                       
                csv_writer.writerow(['END OF TEST'])

print('PROGRAM END')