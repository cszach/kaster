#!/bin/bash

if [ "$EUID" -ne 0 ]
then
    echo "You need to run this file using bash as sudo/root."
    exit 100
fi

version="Beta"  # Must change for every Kaster's update
echo "Installing Kaster password manager $version"
unset version

# Get editor
editor=""
if [ -x "$(command -v nano)" ]
then
    editor="nano"
elif [ -x "$(command -v vim)" ]
then
    editor="vim"
elif [ -x "$(command -v vi)" ]
then
    editor="vi"
else
    echo "What text editor are you using? (enter the command that you can use to start the editor)"
    read editor
    if ! (( -x "$(command -v $editor)" ))
    then
        echo "FATAL: Command '$editor' does not available"
        exit 407
    fi
fi

userhome=$(eval echo ~$USER)

if [ -e system/.kasterrc ]
then
    echo "INFO: Opening $editor editor to edit .kasterrc (Kaster's configuration file)"
    sleep 3
    eval "$editor system/.kasterrc"

    echo "INFO: Moving system/.kasterrc to $userhome"
    mv system/.kasterrc $userhome
elif ! [ -e $userhome/.kasterrc ]
then
    echo "FATAL: Couldn't find .kasterrc in both current directory and home directory, file missing or has been moved"
    exit 408
else
    echo "WARNING: Couldn't find .kasterrc in current directory but found one in home directory"
    echo "It's possible that the .kasterrc in the home directory is of the earlier version of Kaster"
fi

if [ -e kaster.py ]
then
    echo "INFO: Making kaster.py executable"
    chmod +x kaster.py
else
    echo "FATAL: Couldn't find kaster.py"
    exit 400
fi

if [ -e undo_install.sh ]
then
    echo "INFO: Making undo_install.sh executable"
    chmod +x undo_install.sh
 else
    echo "WARNING: Couldn't find undo_install.sh"

echo "Done."
unset userhome
unset editor
exit 0
