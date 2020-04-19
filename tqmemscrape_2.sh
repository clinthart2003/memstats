#!/bin/sh

server=$(echo $HOSTNAME | cut -d "." -f1)
FILENAME=threatq-memory-$server



echo $" " | tee -a /var/log/$FILENAME.log
echo "++++ $server  was restarted ++++" | tee -a /var/log/$FILENAME.log
echo $" " | tee -a /var/log/$FILENAME.log
NOWT=$(echo `date +%Y%m%d`)

echo $NOWT

while true; do

    # echo "DATE:$(date +"%Y-%m-%d %T")" | tee -a /var/log/$FILENAME.log
    # echo "$(top -b -c -w150 -o +%MEM | head -n 35)"  |  tee -a /var/log/$FILENAME.log
    echo $" " | tee -a /var/log/$FILENAME.log
    python /root/pymem.py $FILENAME.log
    # echo $" " | tee -a /var/log/$FILENAME.log
    # echo "$(iostat -dx)" | tee -a /var/log/$FILENAME.log
    echo $" " | tee -a /var/log/$FILENAME.log
    sleep 20

    SIZE=$(stat -c%s /var/log/$FILENAME.log)

    SYSTIME=$(date +%s)
    THEN=$(echo `date +%Y%m%d`)
    echo $THEN
    if [[ $THEN != $NOWT ]] ; then
        mv /var/log/$FILENAME.log /var/log/$FILENAME-$SYSTIME.log
        NOWT=$(echo `date +%Y%m%d`)
        echo $"Change of day " | tee -a /var/log/$FILENAME.log
        echo $NOWT;
    fi

    # if (($SIZE>10000000)) ; then
    #    mv /var/log/$FILENAME.log /var/log/$FILENAME-$SYSTIME.log ;
    # fi

    count=$(ls -l /var/log/$FILENAME-*.log | wc -l)

    if (($count>9)) ; then
        cd /var/log
        tar -cf /var/log/$FILENAME-$SYSTIME.tar $FILENAME-*.log
        gzip /var/log/$FILENAME-$SYSTIME.tar.gz /var/log/$FILENAME-$SYSTIME.tar
        rm -rf /var/log/$FILENAME-*.log
        rm -rf /var/log/*.tar ;
    fi

done