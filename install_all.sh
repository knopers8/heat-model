#!/bin/sh

### very uncomplete now


### compile projects


### install influxdb


### install grafana


### install python dependencies

pip3 install pytz influxdb

### install linky reader

apt install npm
npm i -g linky

### make bbmeteo_server a service

cp etc/bbmeteo.service /etc/systemd/system/bbmeteo.service
systemctl daemon-reload
systemctl enable bbmeteo
systemctl start bbmeteo


### make onewire_server a service

cp etc/onewire-reader.service /etc/systemd/system/onewire-reader.service
systemctl daemon-reload
systemctl enable onewire-reader
systemctl start onewire-reader
