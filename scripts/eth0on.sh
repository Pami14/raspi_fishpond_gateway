#!/bin/bash

sleep 20 

ifconfig | grep eth0

while [ $? == 1 ]
	do 
	sudo ifconfig eth0 up
	sleep 5
	ifconfig | grep eth0
done

sudo systemctl stop eth0on.service


