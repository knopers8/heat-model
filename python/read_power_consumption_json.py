# coding=utf8

import sys
import calendar
import datetime
import pytz
import json
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
with open(filepath, 'r') as file:
  data=file.read()

data_json = json.loads(data)


### initialize variables
this_tz = pytz.timezone("Europe/Paris") # it could be read from the system

year = -1
month = -1
day = -1

measurements = []

for datum in data_json['data']:
  naive_date = datetime.datetime.fromisoformat(datum['date'])

  localized_date = this_tz.localize(naive_date)
  if localized_date <= latest_entry:
    print("That date which already has corresponding metrics in the database, omitting:")
    print(localized_date)
    continue

  watt = datum['value']

  measurements.append({
    "measurement" : "power_consumption",
    "tags": {},
    "time": localized_date.isoformat(),
      "fields": {
      "power" : watt
    }
  })

#print("Measurements:")
#print(measurements)

if len(measurements) > 0:
  print("Writing " + str(len(measurements)) + " entries to the database...")
  client.write_points(measurements)
  print("...done!")
  #print("nop")
else:
  print("No new entries to write, exiting.")
