#!/bin/bash
# This sets up a development enviroment

c="\e[0;32m"
cl="\e[0m"

echo -e "\n${c}[*] Installing git${cl}" && \
sudo pacman --noconfirm -Syu git && \
echo -e "\n${c}[*] Installing yay${cl}" && \
git clone https://aur.archlinux.org/yay.git && \
cd yay && makepkg --noconfirm -si && cd .. && rm -rf yay && \
echo -e "\n${c}[*] Installing vscode${cl}" && \
yay --noanswerclean --noanswerdiff -noansweredit --noanswerupgrade -Syu visual-studio-code-bin && \
echo -e "\n${c}[*] Running archlinux-setup.sh${cl}\n" && \
bash ./setup/archlinux-setup.sh | sed 's|\[\*\]|  \[\+\]|g' && \
echo -e "\n${c}[*] Opening project in vscode${cl}"
code -a . && \
echo -e "\n${c}[*] Finished development setup${cl}" || echo -e "\n${c}[*] Something went wrong${cl}"