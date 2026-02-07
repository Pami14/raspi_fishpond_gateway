#!/bin/bash

sleep 10
sudo ifconfig eth0 down
sudo openvpn /home/pi/XXX.ovpn

