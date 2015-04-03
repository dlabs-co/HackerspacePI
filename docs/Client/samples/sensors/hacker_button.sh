#!/bin/bash

gpio mode 8 input

oldstate=2

while [ 1 ]; do
    state=$( gpio read 8 );
    [[ $state != $oldstate ]] && {
        oldstate=$state;
        [[ $state == 1 ]] && { $status="open"; } && { $status="closed"; }
        bash ../update_status.sh "hacker_button" $status $(date +%y-%m-%d %H:%M) 
    }
    sleep 1s;
done
