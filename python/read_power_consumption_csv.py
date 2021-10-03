# coding=utf8

import sys
import calendar
import datetime
import pytz
from influxdb import InfluxDBClient

### establish a connection to the database
user = 'xxx'
password = 'xxx'
dbname = 'xxx'
host = 'xxx'
port='xxx'

client = InfluxDBClient(host, port, user, password, dbname)
client.ping()

### find the latest entry
query = 'SELECT * FROM \"power_consumption\" GROUP BY * ORDER BY DESC LIMIT 1'
latest_entries_list = client.query(query)
latest_entry = datetime.datetime(2020, 1, 1, 0, 0)
for entry in latest_entries_list:
  # 2021-08-29T19:06:30.326244Z
  entry_as_datetime = datetime.datetime.fromisoformat(entry[0]['time'][:-1]) # we cut Z
  if entry_as_datetime > latest_entry:
    latest_entry = entry_as_datetime
  
latest_entry = pytz.UTC.localize(latest_entry)
print("Latest entry in the database:")
print(latest_entry)

### open the input file
filepath = sys.argv[1]
file = open(filepath, mode='r')
lines = file.readlines()

### initialize variables
this_tz = pytz.timezone("Europe/Paris") # it could be read from the system

year = -1
month = -1
day = -1

measurements = []

for line in lines:  
  if line.count(';') == 2:
    tokens = line.split(';')
    
    if tokens[0].count('/') == 2: # it is a date
      ### update the current date
      date_reading_str = tokens[0].split('/') # dd/mm/yyyy
      day = int(date_reading_str[0])
      month = int(date_reading_str[1])
      year = int(date_reading_str[2])
            
    elif tokens[0].count(':') == 2: # it is a time of day
      ### update the current time of day
      if year == -1:
        exit("Time was read before date, something is wrong with the file, aborting.")
        
      time_reading_str = tokens[0].split(':') # hh:mm:ss
      hour = int(time_reading_str[0])
      mins = int(time_reading_str[1])
      secs = int(time_reading_str[2])
      
      naive_date = datetime.datetime(year, month, day, hour, mins, secs)
      if hour == 0 and mins == 0 and secs == 0:
        # this snippet from an input file should be self-explanatory:
        # 18/09/2021;;
        # 00:00:00;128;Reelle
        # 23:30:00;240;Reelle
        # 23:00:00;54;Reelle
        naive_date = naive_date + datetime.timedelta(days=1)

      localized_date = this_tz.localize(naive_date)
      if localized_date <= latest_entry:
        print("Reached the date which already has corresponding metrics in the database:")
        print(localized_date)
        break
      
      watt = int(tokens[1])
      
      measurements.append({
        "measurement" : "power_consumption",
        "tags": {},
        "time": localized_date.isoformat(),
        "fields": {
          "power" : watt
        }
      })
      
      utc_date = localized_date.astimezone(pytz.UTC)
      #print(utc_date)
      #print(watt)
    else:
      print('Unexpected line format: ' + line)
      


#print("Measurements:")
#print(measurements)

if len(measurements) > 0:
  print("Writing " + str(len(measurements)) + " entries to the database...")
  client.write_points(measurements)
  print("...done!")
else:
  print("No new entries to write, exiting.")

