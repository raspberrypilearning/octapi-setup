#!/bin/bash

# All original code: Crown Copyright 2016, 2017 

# show usage, requires parameters such as "reboot" or "shutdown"
if [ -z "$1" ]; then
    echo "usage: $0 reboot/shutdown/date/unicorn/scp"
    exit
fi

if [ "$1" = "reboot" ]; then
    echo "rebooting cluster"
    ACTION="sudo reboot"
elif [ "$1" = "shutdown" ]; then
    echo "shutting down cluster"
    ACTION="sudo shutdown -HP now"
elif [ "$1" = "unicorn" ]; then
    echo running specified unicorn HAT script
    ACTION="/home/pi/start_unicorn.sh $2"
elif [ "$1" = "date" ]; then
    echo setting the date
    NOW=$(date +"%d %b %Y %H:%M")
    ACTION="sudo date -s '$NOW'"
elif [ "$1" = "scp" ]; then
    echo secure copy to servers
fi

# generate the IP list or use the existing one
if [ -e "ip_list" ]; then
    echo "using existing ip_list as follows..."
    cat ip_list
else
    # discover all IPs on this network
    echo "obtaining IPs on this network and generating new ip_list..." 
    nmap -sP 192.168.1.* | grep 'report for' | awk -F' ' '{print $5}' > /home/pi/ip_list
fi

# for each active IP that is not the router or the client
for i in $(cat ip_list); do
    if [ $i = "192.168.1.1" ]; then
        echo "ignoring router $i"
    elif [ $i = $(hostname -I)]; then
        echo "ignoring client node $i"
    else 
        # assumes an rsa key has been distributed to each node
        echo "contacting $i"
        if [ "$1" = "scp" ]; then
	    scp $2 pi@$i:$3   # $2 is source filename, $3 is full destination
        else
            ssh -f $i $ACTION &
        fi
    fi
done
