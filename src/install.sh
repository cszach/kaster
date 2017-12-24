#!/bin/bash

if [ "$EUID" -ne 0 ]
then
    echo "You need to run this file using bash as sudo/root."
    exit 100
fi

version="Beta"  # Must change for every Kaster's update
echo "Installing Kaster password manager $version"

# Get editor
editor=""
if [ command -v nano ]
then
    editor="nano"
elif [ command -v vim ]
then
    editor="vim"
elif [ command -v vi ]
then
    editor="vi"
else
    echo "What text editor are you using? (enter the command that you can use to start the editor) "
    read editor
    if ! (( command -v "$editor" ))
    then
        echo "FATAL: Command '$editor' does not available"
        exit 407
    fi
fi

if [ -e system/.kasterrc ]
then
    echo "INFO: Opening $editor editor to edit .kasterrc (Kaster's configuration file)"
    sleep 3
    eval "$editor system/.kasterrc"

    echo "INFO: Moving system/.kasterrc to $HOME"
    mv system/.kasterrc $HOME
elif ! [ -e $HOME/.kasterrc ]
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
    echo "FATAL: Couldn't find kaster.py, kaster.py missing or you've moved the files"
    exit 400
fi

echo "Done."
exit 0
