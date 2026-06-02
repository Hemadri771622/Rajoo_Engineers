#!/bin/bash

LOGFILE="/home/ric/update.log"

echo "===================================" >> $LOGFILE
echo "System boot detected: $(date)" >> $LOGFILE

cd /home/ric/Rajoo_Engineers || exit

echo "Fetching latest code..." >> $LOGFILE
git fetch origin RIC >> $LOGFILE 2>&1

LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/RIC)

if [ "$LOCAL" != "$REMOTE" ]; then

    echo "New update found" >> $LOGFILE

    echo "Stopping backend..." >> $LOGFILE
    sudo systemctl stop rajoo.service

    sleep 3

    echo "Pulling latest code..." >> $LOGFILE
    git pull origin RIC >> $LOGFILE 2>&1

    sleep 3

    echo "Starting backend..." >> $LOGFILE
    sudo systemctl start rajoo.service

    echo "Backend updated successfully" >> $LOGFILE

else

    echo "Already up to date" >> $LOGFILE

    echo "Starting backend..." >> $LOGFILE
    sudo systemctl start rajoo.service

fi

echo "Boot update process completed" >> $LOGFILE
echo "" >> $LOGFILE
