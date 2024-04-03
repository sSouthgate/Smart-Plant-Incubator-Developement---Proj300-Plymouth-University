''' 
This program aims to be used to perform the experiments required to find the relating equation between soil moistuire, it's delta over time and amount of water distributed.
    By opening and closing the solenoid valve for a set interval we can find out how much water is distributed in x amount of seconds.
    This in turn will allow us to calculate the change in moisture overtime when a know amount of water is dispensed.
    We wil be recording the data and exporting it through a generated .csv file.
    This file will allow us to plot a graph of the moisture change overtime with a fixed amount water distributed.
    We will then be able to find the relation between time, water, and moisture, 
    this will allow us to know how much water is needed to be distributed over how much time to achieve the disired moisture level.
'''
# Imports
import csv
import os
from datetime import datetime
# Variables
m = 50 #dummy value for moisture
t = 5 #dummy value for time
current_date_time = datetime.now()
T = current_date_time.strftime('%H:%M:%S')
D = current_date_time.strftime("%d/%m")
x = 0 #test value

# Set the file path and the headers for the CSV file
file_path = '../test.csv'
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

print("Writting to CSV File...")

while x < 6:
    with open('test.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        field = ["Moisture Level", "Time in s", "Time of day"]

        #writer.writerow(field)
        writer.writerow([m,t,T,D])
    x += 1

print("Writting finished")