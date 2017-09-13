#!/bin/bash
ifconfig enp8s0 85.121.149.44 netmask 255.255.255.0
route add default gw 25.0.0.1 enp8s0
echo "nameserver 8.8.8.8" >> /etc/resolv.conf
