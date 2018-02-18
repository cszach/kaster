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

if [ -e kaster.py ]
then
    echo "INFO: Making kaster.py NOT executable."
    chmod -x kaster.py
else
    echo "FATAL: Could not find kaster.py."
    exit 400
fi

userhome=$(eval echo ~$USER)
if [ -e $userhome/.kasterrc && -d system ]
then
    echo "INFO: Moving .kasterrc in home directory back to system folder."
    mv $userhome/.kasterrc system
else
    echo "FATAL: Couldn't find .kasterrc in $userhome or system/ does not exist."
    exit 402
fi

echo "Done."
unset userhome
exit 0
