#!/usr/bin/env bash
set -e
set -x
set -u


START_DATE=`date -I --date='-5 days'`
END_DATE=`date -I`

/usr/local/bin/linky loadcurve --start $START_DATE --end $END_DATE --output /tmp/latest_power.json 2>&1 > /home/pi/logs/linky_read`date -Iseconds`
/usr/bin/python3 /home/pi/heat-model/python/read_power_consumption_json_stable.py /tmp/latest_power.json 2>&1 > /home/pi/logs/power_consumption_read_`date -Iseconds` 


