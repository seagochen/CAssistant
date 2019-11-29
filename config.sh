#!/bin/bash

# functions
exists() {
    command -v "$1" >/dev/null 2>&1
}

install_siki() {
    if python3 -c "import siki" &> /dev/null; then
        echo '---Python3 Module: SIKI installed'
    else
        pip3 install siki
    fi
}

# clear command screen first
clear

# default value
proname=project

# Read usr input and create a new folder for project
echo "This script will help you to create an empty C-tora project..."
read -t 30 -p "Your project name please: " proname
echo -e "\n"

# environment check
echo "Before creating project with name '$proname', check the environment first..."


# Test python3 is available
# and whether the dependency package has been installed
if exists python3; then
    if exists pip3; then
        install_siki
    fi
else
    echo 'You should install python3 to your system before running this script'
fi


# echo message
echo -e "\n"
echo "Environment check finished, now creating the empty project with name '$proname'"

# generate empty project dir
python3 Tora/PreparePro.py $proname