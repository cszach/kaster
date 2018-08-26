#!/bin/sh
# Install script for Kaster Password Vault

# ***** IMPORTANT VARIABLES *****
# You may set these variables manually,
# but it's usually best to leave them as default.

kpv_version="Beta"  # Kaster version, must change for every Kaster's new release
editor=""           # Path to text editor used to edit Kaster configuration file
src_path="src"      # Kaster's source path, relative to this install script

rcp="$src_path/.kasterrc"         # Path to .kasterrc in source
kasp="$src_path/kaster.py"        # Path to kaster.py
kaster_home="/usr/lib/kaster"     # Directory containing Kaster's program files
user_home="$(eval echo ~$USER)"   # Directory containing user's Kaster files

# ********************************

if [ $(id -u) == "0" ]
then
    echo "Please run this script as normal user (i.e. not root). Aborting..."
    exit 1
fi

defc="\033[0m"; yellow="\033[1;33m"; red="\033[0;31m"  # Define colors

echo -e "Installing Kaster Password Vault $kpv_version\n"

exitcode="0"  # This script's exitcode

# *************************************
# * Get text editor to edit .kasterrc *
# *************************************

if [ -x $(command -v nano) ] && [ -z $editor ]
then
    editor="nano"
else
    if [ -z $editor ]
    then
        read -p "What text editor do you prefer? (specify full path to executable)" editor
    fi

    if ! [ -x $editor ]
    then
        >&2 echo -e "${red}ERROR${defc}: $editor is not available"
        editor=""
        exitcode="4"
    fi
fi

# ******************
# * Edit .kasterrc *
# ******************

if [ -e $rcp ]
then
    if [ -n $editor ]
    then
        echo "INFO: Opening $editor to configure Kaster"
        sleep 3
        eval "$editor $rcp"

        echo "INFO: Moving $rcp to $kaster_home"
        mv $rcp $kaster_home
    fi
elif ! [ -e $kaster_home/.kasterrc ]
then
    >&2 echo -e "${red}ERROR${defc}: Couldn't find .kasterrc, file missing or has been moved"
    exitcode="5"
else
    echo -e "${yellow}WARNING${defc}: Couldn't find .kasterrc in $rcp but found one in Kaster home ($kaster_home)"
    echo "It's possible that the .kasterrc in the home directory is of the earlier version of Kaster"
    exitcode="2"
fi

# **************************************
# * Set up $kaster_home and $user_home *
# **************************************

if [ -w $kaster_home ]
then
    mkdir -p $kaster_home
    mv src/* $kaster_home
else
    sudo mkdir -p $kaster_home
    sudo mv src/* $kaster_home
fi

if [ -r $user_home ] && [ -w $user_home ]
then
    mkdir $user_home/.kaster
else
    >&2 echo -e "${red}ERROR{$defc}: $user_home doesn't exist, or you don't have read/write access to it."
    echo -e "Please edit \$user_home variable inside the installation script ($0)."
    echo "Set it to path of directory that you have read and write access to."
fi

# ***************************
# * Finalizing installation *
# ***************************

if [ -e $kasp ]
then
    echo "INFO: Making kaster.py executable"
    chmod +x $kasp
else
    >&2 echo -e "${red}ERROR${defc}: Couldn't find kaster.py"
    exitcode="3"
fi

if [ -e undo_install.sh ]
then
    echo "INFO: Making undo_install.sh executable"
    chmod +x undo_install.sh
else
    echo "${yellow}WARNING${defc}: Couldn't find undo_install.sh"
fi

# ***********************
# * Finish installation *
# ***********************

if [ $exitcode -ge 4 ]
then
    >&2 echo -e "\nFAILED: Installation failed. Resolve errors (outputed to stderr) and try again."
fi

exit $exitcode
