#!/bin/bash
# grephome.sh
# Get the user's home directory (when sudo it's not /root) and write it to a file,
# to help Kaster determines .kasterrc, which is placed in the user's home directory

getuserhome=$(eval echo ~$USER)

# Create /tmp (temporary) directory to save products of minions
if ! [ -d /tmp ]
then
    mkdir /tmp
fi

f_target="/tmp/grephome.minion.product"  # Path of file to write to
touch $f_target
echo $getuserhome > $f_target

unset f_target
unset getuserhome
