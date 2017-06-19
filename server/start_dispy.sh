#!/bin/bash

# All original code: Crown Copyright 2016, 2017 

# start dispy on the chosen interface, usually it's wlan0
# we need to wait until the interface has has a chance to connect
sleep 30

_IP=$(hostname -I)
/usr/local/bin/dispynode.py -i "$_IP" --daemon 

