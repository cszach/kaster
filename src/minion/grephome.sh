#!/bin/bash
# minion/grephome.sh
# Get the user's home directory (when sudo it's not /root) and write it to a file,
# to help Kaster determines .kasterrc, which is placed in the user's home directory
# NOT FOR MANUALLY EXECUTION

getuserhome=$(eval echo ~$USER)

# Create /tmp (temporary) directory to save products of minions
mkdir /tmp &>/dev/null

f_target="/tmp/grephome.minion.product"  # Path of file to write to
touch $f_target
echo $getuserhome > $f_target

unset f_target
unset getuserhome
