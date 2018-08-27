#!/bin/sh
# Install script for Kaster Password Vault

# ***** IMPORTANT VARIABLES *****

# You may set these variables manually,
# but it's usually best to leave them as default.

kpv_version="Beta"  # Kaster version, must change for every Kaster's new release
editor=""           # Path to text editor used to edit Kaster configuration file
src_path="src"      # Kaster's source path, relative to this install script

kasp="$src_path/kaster.py"       # Path to kaster.py
kaster_home="/usr/lib/kaster"    # Directory containing Kaster's program files
user_home="$(eval echo ~$USER)"  # Directory containing user's Kaster files
date_format = "%d/%m/%Y"         # Date format for use in Kaster
time_format = "%H:%M:%S"         # Time format for use in Kaster

export src_path
export kaster_home

# Default values. DO NOT CHANGE THESE UNLESS YOU KNOW WHAT YOU ARE DOING.

export def_kaster_home="/usr/lib/kaster"    # Default value for $kaster_home
export def_user_home="$(eval echo ~$USER)"  # Default value for $user_home
export def_df="%d/%m/%Y"                    # Default value for $date_format
export def_tf="%H:%M:%S"                    # Default value for $time_format

# ********************************

if [ $(id -u) == "0" ]
then
    echo "Please run this script as normal user (i.e. not root). Aborting..."
    exit 1
fi

defc="\033[0m"; yellow="\033[1;33m"; red="\033[0;31m"  # Define colors

echo -e "Installing Kaster Password Vault $kpv_version\n"

exitcode="0"  # This script's exitcode

# **************************************
# * Set up $kaster_home and $user_home *
# **************************************

export fcheck="0"

if [ -f .mk_kpv_home.sh ]
then
    if [ -w $kaster_home ]
    then
        sh .mk_kpv_home.sh
    else
        sudo sh .mk_kpv_home.sh
    fi
else
    >&2 echo -e "${red}ERROR${defc}: Couldn't find .mk_kpv_home.sh"
    exitcode="6"
fi

# ************************************
# * Generate .kasterrc in $user_home *
# ************************************

if [ -r $user_home ] && [ -w $user_home ]
then
    rcp="$user_home/.kasterrc"
    touch $rcp

    if [ $kaster_home != $def_kaster_home ]
    then
        echo "program_file_dir = \"$kaster_home\"" >> $rcp
    fi

    if [ $user_home != $def_user_home ]
    then
        echo "user_file_dir = \"$def_user_home\"" >> $rcp
    fi

    if [ $date_format != $def_df ]
    then
        echo "date_format = \"$def_df\"" >> $rcp
    fi

    if [ $time_format != $def_tf ]
    then
        echo "time_format = \"$def_tf\"" >> $rcp
    fi
else
    >&2 echo -e "${red}ERROR{$defc}: $user_home doesn't exist, or you don't have read/write access to it."
    echo -e "Please edit \$user_home variable inside the installation script ($0)."
    echo "Set it to path of directory that you have read and write access to."
    exitcode="7"
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

# ********************************
# * Report & Finish installation *
# ********************************

if [ $exitcode -gt 3 ]
then
    >&2 echo -e "\n{$red}FAILED{$defc}: Installation failed."
    echo "Resolve errors (outputed to stderr) and try again."
fi

exit $exitcode
