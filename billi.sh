#!/bin/bash

# Detect Linux Distribution
detect_distro() {
    if [[ "$OSTYPE" == linux-android* ]]; then
        distro="termux"
    fi

    if [ -z "$distro" ]; then
        distro=$(ls /etc | awk 'match($0, "(.+?)[-_](?:release|version)", groups) {if(groups[1] != "os") {print groups[1]}}')
    fi

    if [ -z "$distro" ]; then
        if [ -f "/etc/os-release" ]; then
            distro="$(source /etc/os-release && echo $ID)"
        elif [ "$OSTYPE" == "darwin" ]; then
            distro="darwin"
        else 
            distro="invalid"
        fi
    fi
}

# Pause Function
pause() {
    read -n1 -r -p "Press any key to continue..." key
}

# Banner Function
banner() {
    clear
    echo -e "\e[1;31m"
    if ! [ -x "$(command -v figlet)" ]; then
        echo 'Introducing Billi'
    else
        figlet Billi
    fi
}

# Initialize Environment Variables
init_environ(){
    declare -A backends; backends=(
        ["arch"]="pacman -S --noconfirm"
        ["debian"]="apt-get -y install"
        ["ubuntu"]="apt -y install"
        ["termux"]="apt -y install"
        ["fedora"]="yum -y install"
        ["redhat"]="yum -y install"
        ["SuSE"]="zypper -n install"
        ["sles"]="zypper -n install"
        ["darwin"]="brew install"
        ["alpine"]="apk add"
    )

    INSTALL="${backends[$distro]}"

    if [ "$distro" == "termux" ]; then
        PYTHON="python"
        SUDO=""
    else
        PYTHON="python3"
        SUDO="sudo"
    fi
    PIP="$PYTHON -m pip"
}

# Install Dependencies
install_deps(){
    packages=(openssl git $PYTHON $PYTHON-pip figlet)
    if [ -n "$INSTALL" ]; then
        for package in ${packages[@]}; do
            $SUDO $INSTALL $package
        done
        $PIP install -r requirements.txt
    else
        echo "We could not install dependencies."
        echo "Please make sure you have git, python3, pip3 and requirements installed."
        echo "Then you can execute bomber.py ."
        exit
    fi
}

# Main Script Logic
banner
pause
detect_distro
init_environ
if [ -f .update ]; then
    echo "All Requirements Found...."
else
    echo 'Installing Requirements....'
    echo .
    echo .
    install_deps
    echo This Script Was Made By Bandar > .update
    echo 'Requirements Installed....'
    pause
fi

# Menu with SMS Bombing Option
while :
do
    banner
    echo ""
    echo "[1] Start SMS Bomber"
    echo "[2] To Exit"
    read ch
    clear
    if [ $ch -eq 1 ]; then
        $PYTHON bomber.py --sms
        exit
    elif [ $ch -eq 2 ]; then
        banner
        exit
    else
        echo -e "\e[4;32m Invalid Input !!! \e[0m"
        pause
    fi
done
