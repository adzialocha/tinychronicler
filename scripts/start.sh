#!/bin/bash
# Check for updates and start tinychronicler

BASE_DIR=/home/pi/tinychronicler
SESSION=tc

function check_command() {
        if ! [ -x "$(command -v $1)" ]; then
          echo "Error: $1 is not installed." >&2
          exit 1
        fi
}

# Make sure all required programs are installed
check_command git
check_command ping
check_command /home/pi/.poetry/bin/poetry
check_command puredata
check_command tmux

# Move into the tinychronicler folder
cd $BASE_DIR

# Check first if internet connection exists
HAS_INTERNET=$(ping -q -w1 -c1 google.com &>/dev/null && echo 1 || echo 0)

# Run update routine when internet connection is given
if [ $HAS_INTERNET -eq 1 ]; then
        echo "Internet connection exists. Start update routine!"
        echo

        # Fetch the latest version from github\
        echo "► Fetch latest version from GitHub"
        git fetch --all
        git reset --hard origin/main

        # Run pre-update script when it exists
        echo
        echo "► Run pre-update script"
        if [ -f "./scripts/pre-update.sh" ]; then
                exec ./scripts/pre-update.sh
        else
                echo "No script found, skip this step"
        fi

        # Install any dependency updates
        echo
        echo "► Update dependencies"
        LLVM_CONFIG=llvm-config-9 /home/pi/.poetry/bin/poetry install

        # Run post-update script when it exists
        echo
        echo "► Run post-update script"
        if [ -f "./scripts/post-update.sh" ]; then
                exec ./scripts/post-update.sh
        else
                echo "No script found, skip this step"
        fi
else
        echo "No internet connection detected. Skip update routine"
fi

# Start Tiny Chronicler and Pure Data in tmux session
echo
echo "► Start tinychronicler"
tmux kill-session -t $SESSION
tmux new-session -d -s $SESSION
tmux split-window -h -t $SESSION
tmux send-keys -t $SESSION:0.0 "/home/pi/.poetry/bin/poetry run python tinychronicler" Enter
tmux send-keys -t $SESSION:0.1 "puredata -inchannels 0 -nogui ./tinychronicler.pd" Enter
