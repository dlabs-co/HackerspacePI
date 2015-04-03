#!/bin/bash

gpio mode 3 input

oldstate=2

while [ 1 ]; do
    state=$( gpio read 3 );
    [[ $state != $oldstate ]] && {
        oldstate=$state;
        [[ $state == 1 ]] && { $status="open"; } && { $status="closed"; }
        bash ../update_status.sh "movement_sensor" $status "$(date "+%y-%m-%d %H:%M")" 
    }
    sleep 1s;
done
