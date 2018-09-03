#!/bin/sh
# Install script for Kaster Password Vault

# ***** IMPORTANT VARIABLES *****

# You may set these variables manually,
# but it's usually best to leave them as default.

kpv_version="Beta"  # Kaster version, must change for every Kaster's new release
src_path="src"      # Kaster's source path, relative to this install script

kaster_home="/usr/lib/kaster"  # Directory containing Kaster's program files
kasp="$kaster_home/kaster.py"  # Path to kaster.py in $kaster_home
user_home=$HOME                # Directory containing user's Kaster files
date_format="%d/%m/%Y"         # Date format for use in Kaster
time_format="%H:%M:%S"         # Time format for use in Kaster

export src_path
export kaster_home

# Default values. DO NOT CHANGE THESE UNLESS YOU KNOW WHAT YOU ARE DOING.

export def_kaster_home="/usr/lib/kaster"  # Default value for $kaster_home
export def_user_home=$HOME                # Default value for $user_home
export def_df="%d/%m/%Y"                  # Default value for $date_format
export def_tf="%H:%M:%S"                  # Default value for $time_format

# ********************************

if [ $(id -u) == "0" ]
then
    echo "Please run this script as normal user (i.e. not root). Aborting..."
    exit 1
fi

export defc="\033[0m"       # No color
export yellow="\033[1;33m"  # Yellow
export red="\033[1;31m"     # Red

echo -e "Installing Kaster Password Vault $kpv_version\n"

exitcode="0"  # This script's exitcode

export fcheck="0"

# ***********************
# * Set up $kaster_home *
# ***********************

if [ -f .mk_kpv_home.sh ]
then
    echo "INFO: Creating Kaster's home at $kaster_home"

    if [ -w $kaster_home ]
    then
        sh .mk_kpv_home.sh
    else
        eval "sudo -E /bin/sh -c \"sh .mk_kpv_home.sh\""
    fi

    exitcode=$?
else
    >&2 echo -e "${red}ERROR${defc}: Couldn't find .mk_kpv_home.sh"
    exitcode="3"
fi

# ****************************************
# * Generate .kasterrc in $user_home and *
# * Create .kaster/ folder in $user_home *
# ****************************************

if [ -r $user_home ] && [ -w $user_home ]
then
    echo "INFO: Creating .kasterrc in $user_home"

    rcp="$user_home/.kasterrc"
    touch $rcp

    if [ $kaster_home != $def_kaster_home ]
    then
        echo "program_file_dir = \"$kaster_home\"" >> $rcp
    fi

    if [ $user_home != $def_user_home ]
    then
        echo "user_file_dir = \"$user_home\"" >> $rcp
    fi

    if [ $date_format != $def_df ]
    then
        echo "date_format = \"$date_format\"" >> $rcp
    fi

    if [ $time_format != $def_tf ]
    then
        echo "time_format = \"$time_format\"" >> $rcp
    fi

    echo "INFO: Creating user-specific Kaster folder in $user_home"
    mkdir $user_home/.kaster
else
    >&2 echo -e "${red}ERROR${defc}: $user_home doesn't exist, or you don't have read/write access to it."
    echo -e "Please edit \$user_home variable inside the installation script ($0)."
    echo "Set it to path of directory that you have read and write access to."
    echo "It is best to set it to your home directory ($HOME)"
    exitcode="4"
fi

# ***************************
# * Finalizing installation *
# ***************************

if [ -e $kasp ]
then
    echo "INFO: Making kaster.py executable"
    chmod +x $kasp
    echo "INFO: Creating a symlink to $kasp in /usr/bin/"
    sudo ln -s $kasp /usr/bin/kaster &> /dev/null
else
    >&2 echo -e "${red}ERROR${defc}: Couldn't find kaster.py"
    exitcode="5"
fi

if [ -f uninstall.sh ]
then
    echo "INFO: Completing uninstall script (./uninstall.sh)"

    echo -e "#!/bin/sh\n#\n\
# This script can be used to (partly) uninstall Kaster. It moves everything\n\
# inside Kaster's home (usually /usr/lib/kaster) back to the source folder.\n\
# Then if you want to completely remove Kaster, you have to manually delete\n\
# the source folder and other relevant files (such as LICENSE or README.rst).\n\n\
src_path=\"$src_path\"\nkaster_home=\"$kaster_home\"\nuser_home=\"$user_home\"\n"\
> uninstall.new.sh

    cat uninstall.sh >> uninstall.new.sh
    mv uninstall.new.sh uninstall.sh
else
    echo -e "${yellow}WARNING${defc}: Couldn't find uninstall script"
fi

# ********************************
# * Report & Finish installation *
# ********************************

if [ $exitcode -ne 0 ]
then
    >&2 echo -e "\n${red}FAILED${defc}: Installation failed."
    echo "Resolve errors (outputed to stderr) and try again."
else
    echo -e "\n\033[1;32mKaster is successfully installed.${defc}"
fi

exit $exitcode
