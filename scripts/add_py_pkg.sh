#!/bin/bash

set -e

txtred='\e[1;31m' # Red
txtgrn='\e[1;32m' # Green
txtylw='\e[1;33m' # Yellow
txtwht='\e[1;37m' # White
nocolr='\e[0m'     # No Color

# Check if an argument was provided
if [ $# -eq 0 ]; then
  echo -e "${txtred}No arguments provided. Exiting...${nocolr}"
  echo -e "${txtylw}Usage: make add m=package_name${nocolr}"
  exit 1
fi

# Install package using pip
echo -e "${txtgrn}Installing package using pip...${txtwht}"
pip install $1

# Prompt user to add package to requirements file
echo -e "${txtylw}Do you want to add $1 package to a requirements file? (y/n)${nocolr}"
read response

if [[ $response =~ ^[Yy]$ ]]
then
    # Prompt user to choose requirements file
    echo -e "${txtylw}Which requirements file do you want to add $1 to? (1/2)${nocolr}"
    echo "1. requirements.txt"
    echo "2. requirements-dev.txt"
    echo "3. requirements-test.txt"
    read file_choice

    if [[ $file_choice == 1 ]]
    then
        # Add package to requirements.txt
        echo "$1" >> requirements.txt
        echo "Package added to requirements.txt"
    elif [[ $file_choice == 2 ]]
    then
        # Add package to requirements-dev.txt
        echo "$1" >> requirements-dev.txt
        echo -e "${txtgrn}Package added to requirements-dev.txt${nocolr}"
    elif [[ $file_choice == 3 ]]
    then
        echo "$1" >> requirements-test.txt
        echo -e "${txtgrn}Package added to requirements-test.txt${nocolr}"
    else
        echo -e "${txtred}Invalid choice${nocolr}"
    fi
else
    echo -e "${txtylw}Package $1 not added to requirements file${nocolr}"
fi
