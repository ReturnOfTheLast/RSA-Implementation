#!/bin/bash
# At the moment this setup script is based on my own system, and as such I can not promise that it will work on yours.

c="\e[0;32m"
cl="\e[0m"

echo -e "\n${c}[*] Installing python3, virtualenv, curl and unzip${cl}" && \
sudo pacman --noconfirm -Syu python python-virtualenv curl unzip && \
echo -e "$\n${c}[*] Setting up virtualenv${cl}" && \
virtualenv venv && \
echo -e "\n${c}[*] Downloading prime numbers${cl}" && \
bash download_primenumbers.sh && \
echo -e "\n${c}[*] Finished setup${cl}" || ( echo -e "\n${c}[*] Something went wrong${cl}"; exit 1)