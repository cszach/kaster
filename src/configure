#!/bin/bash
if [ "$EUID" -ne 0 ]
then 
    echo "Run this file using bash as root."
    exit 1
fi

# Create directory for program's files
if [ ! -d /usr/share/kaster ]
then
    echo "Creating /usr/share/kaster"
    mkdir /usr/share/kaster
fi

# Create log file
if ! [[ -e /usr/share/kaster/log.dat ]];
then
    echo "Creating file /usr/share/kaster/log.dat"
    touch /usr/share/kaster/log.dat
    DATETIME=$(date "+%H:%M:%S %d/%m/%Y")
    echo "Log file created on $DATETIME" > /usr/share/kaster/log.dat
fi

if [[ -e kaster.py ]];
then
    echo "Making kaster.py executable"
    chmod +x kaster.py
else
    echo "Error: kaster.py not found"
    exit 3
fi

echo "Done"

