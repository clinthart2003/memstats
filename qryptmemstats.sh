#!/bin/sh

server=$(echo $HOSTNAME | cut -d "." -f1)
FILENAME=qrypt-memory-$server

echo $" " | tee -a /var/log/qrypter_commander/$FILENAME.log
echo "++++ $server  was restarted ++++" | tee -a /var/log/qrypter_commander/$FILENAME.log
echo $" " | tee -a /var/log/qrypter_commander/$FILENAME.log
NOWT=$(echo `date +%Y%m%d`)

echo $NOWT

while true; do

    # Add date stamp and metrics to logs in /var/log dir
         #TOP stats and snapshot timestamp
    echo "DATE:$(date +"%Y-%m-%d %T")" | tee -a /var/log/qrypter_commander/$FILENAME.log
    echo "$(top -b -w150 -o +%MEM | head -n 75)"  |  tee -a /var/log/qrypter_commander/$FILENAME.log
         #Collect HDD metrics
    echo $" " | tee -a /var/log/qrypter_commander/$FILENAME.log
    echo "$(iostat -dx)" | tee -a /var/log/qrypter_commander/$FILENAME.log
    echo $" " | tee -a /var/log/qrypter_commander/$FILENAME.log
    sleep 60

    # Clip file at change of day
    SYSTIME=$(date +%s)
    THEN=$(echo `date +%Y%m%d`)
    echo $THEN
    if [[ $THEN != $NOWT ]] ; then
        mv /var/log/qrypter_commander/$FILENAME.log /var/log/qrypter_commander/$FILENAME-$SYSTIME.log
        mv /var/log/qrypter_commander/$FILENAME-jvm.log /var/log/qrypter_commander/$FILENAME-jvm-$SYSTIME.log
        NOWT=$(echo `date +%Y%m%d`)
        echo $"Change of day " | tee -a /var/log/qrypter_commander/$FILENAME.log
        echo $NOWT;
    fi

    count=$(ls -l /var/log/qrypter_commander/$FILENAME-*.log | wc -l)

    # Rollup and archive logs when there are 10, then zip it up.
    if (($count>19)) ; then
        cd /var/log
        tar -cf /var/log/qrypter_commander/$FILENAME-$SYSTIME.tar $FILENAME-*.log
        gzip /var/log/qrypter_commander/$FILENAME-$SYSTIME.tar.gz /var/log/qrypter_commander/$FILENAME-$SYSTIME.tar
        rm -rf /var/log/qrypter_commander/$FILENAME-*.log
        rm -rf /var/log/qrypter_commander/*.tar ;
    fi

        count=$(ls -l /var/log/qrypter_commander/$FILENAME-*.log | wc -l)

done