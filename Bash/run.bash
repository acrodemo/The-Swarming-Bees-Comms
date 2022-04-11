#!/bin/bash
FILE=""
DIR="/home/$USER/Documents/Code/SwarmingBees2/The-Swarming-Bees-Comms/Bash/SEND_FILES"


while true
    do
        if [ -z "$(ls -A $DIR)" ]
            then
                echo "Empty"
            else
                python3 /home/$USER/Documents/Code/SwarmingBees2/The-Swarming-Bees-Comms/Client/main.py
            fi
    done
