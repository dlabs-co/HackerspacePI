#!/bin/bash
while [ 1 ]; do
    read id_card

    status="open"
    last_id=$(cat ~/.last_id_read)
    echo $id_card > ~/.last_id_read

    [[ $id_card == $last_id ]] && {
        status="closed"
        echo "" > ~/.last_id_read
    }

    bash ../update_status.sh $id_card $status "$(date "+%y-%m-%d %H:%M")" 
done
