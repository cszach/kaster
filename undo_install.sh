#!/bin/bash
# If you ran install.sh, you can run this file
# to revert install.sh's actions.
# Helpful when you are testing Kaster.
# It won't undo your changes to the source files.
# If you changed .kasterrc, this script won't
# help if you are expecting it to renew .kasterrc.

if [ $EUID -ne "0" ]
then
    echo "You need to execute this as sudo/root."
    exit 100
fi

if [ -e src/kaster.py ]
then
    echo "INFO: Making kaster.py NOT executable."
    chmod -x src/kaster.py
else
    echo "FATAL: Could not find kaster.py."
    exit 400
fi

userhome=$(eval echo ~$USER)
if [ -e $userhome/.kasterrc ] && [ -d src/system ]
then
    echo "INFO: Moving .kasterrc in home directory back to src/system/."
    mv $userhome/.kasterrc src/system
else
    echo "FATAL: Couldn't find .kasterrc in $userhome or src/system/ does not exist."
    exit 402
fi

echo "Done."
unset userhome
exit 0
