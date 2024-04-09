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
from grove_light_sensor_v1_2 import GroveLightSensor
import RPi.GPIO as GPIO
# Set current date and time
current_date_time = datetime.now()

# VARIABLES
t0 = time.time()                            # Current time in s
T = current_date_time.strftime('%H:%M:%S')  # Current Time in Hours:Minutes:Seconds

# SETUP RPi GPIO
PIN = 32                    # Define RPi GPIO PIN
GPIO.setmode(GPIO.BOARD)    # Set GPIO Pin numbering system
GPIO.setup(PIN, GPIO.OUT)   # Set GPIO Pin mode to output
GPIO.output(PIN, 0)         # Set GPIO to Low

# connect to analog pin 2(slot A2)
sensorPin = 2
# Define what grove sensor will be used
sensor = GroveLightSensor(sensorPin) # using light sensor while developing code is easier to test

# Set the file path and the headers for the CSV file
file_path = '../Smart-Plant-Incubator-Code/test.csv'
headers = ["Moisture Level", "Time in s", "Time of Day", "Date"]

# Check if the file exists
if os.path.exists(file_path):
    print("File already present, adding to current file")
if not os.path.exists(file_path):
    print("File not present, creating file...")
    # If the file doesn't exist, create it and write the headers to it
    with open(file_path, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(headers)
    print("File created")

print('EXPERIMENT START:',T)
GPIO.output(PIN, 1)
try:   
    while True: #sensor.light > 10:
            # Set Variables at each start of the loop
            current_date_time = datetime.now()              # Add current Date & Time into a variable
            T = current_date_time.strftime('%H:%M:%S')      # Define T as current Time
            D = current_date_time.strftime('%d/%m')         # Define D as current Date in day/month
            t1 = time.time()                                # Define t1 as current time in seconds
            t1 = t1 - t0                                    # Substract t1(current time in s) from t0(Start time in s of program)
            
            # Print info to terminal for inspection
            print('Time Elapsed:', round(t1),'s')
            print('Light value: {0}'.format(sensor.light))
            
            # Start writing data stream to data file.
            with open('test.csv', 'a', newline='') as file:
                writer = csv.writer(file)                       
                writer.writerow([sensor.light,round(t1),T,D])   # Sensor Value, Time Elapsed(in s), Current Time, Current Date
                time.sleep(1)

# When Ctrl+C is input do this:
except KeyboardInterrupt:
    print('\nTest Terminated by User, Closing Program...')

GPIO.output(PIN, 0) # Set GPIO pin low
GPIO.cleanup
print('PROGRAM END')
