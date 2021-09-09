#!/bin/sh

### very uncomplete now


### compile projects


### install influxdb


### install grafana


### make bbmeteo_server a service

cp etc/bbmeteo.service /etc/systemd/system/bbmeteo.service
systemctl daemon-reload
systemctl enable bbmeteo
systemctl start bbmeteo
