if [ $(id -u) != "0" ]
then
    echo "Please run this script as root. Aborting..."
    exit 1
fi

defc="\033[0m"; yellow="\033[1;33m"; red="\033[1;31m";  # Define colors

echo "INFO: Moving everything in Kaster's home ($kaster_home)"
echo "      back to Kaster's source directory ($src_path)"

if [ -d $kaster_home ] && [ -d $src_path ]
then
    rm $kaster_home/.kasterrc
    chmod u-x $kasp
    mv $kaster_home/* $src_path
    rmdir $kaster_home
else
    if ! [ -d $kaster_home ]
    then
        >&2 echo -e "${red}ERROR${defc}: Couldn't find Kaster's home ($kaster_home)"
    fi

    if ! [ -d $src_path ]
    then
        >&2 echo -e "${red}ERROR${defc}: Couldn't find Kaster's source path ($src_path)"
    fi
fi

if [ -L /usr/bin/kaster ]
then
    rm /usr/bin/kaster
else
    echo -e "${yellow}WARNING${defc}: Couldn't find /usr/bin/kaster"
fi

if [ -d $user_home/.kaster ]
then
    read -p "Remove $user_home/.kaster ? (DON'T if you've saved passwords) [y|n] " rmhp
    rmhp=$(echo -n $rmhp | tr [:upper:] [:lower:])

    if [[ $rmhp == "y" ]] || [[ $rmhp == "yes" ]]
    then
        rm -r $user_home/.kaster
    fi
else
    echo -e "${red}ERROR${defc}: Couldn't find $user_home/.kaster"
fi

if [ -f $user_home/.kasterrc ]
then
    read -p "Remove personal settings ($user_home/.kasterrc) ? [y|n] " rmhp
    rmhp=$(echo -n $rmhp | tr [:upper:] [:lower:])

    if [[ $rmhp == "y" ]] || [[ $rmhp == "yes" ]]
    then
        rm $user_home/.kasterrc
    fi
else
    echo -e "${red}ERROR${defc}: Couldn't find custom .kasterrc"
fi
