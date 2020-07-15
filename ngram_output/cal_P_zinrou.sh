#!/bin/bash
while read l
do
    read word
    max_c=0
    zinrou_c=0
    while read count
    do
        if echo "$count" | grep "^---" >/dev/null
        then
            break
        fi
        if echo "$count" | grep "人狼" >/dev/null
        then
            zinrou_c=$( echo "$count" | grep -o "^[0-9]*" )
        fi
        max_c=$(( $max_c + $( echo "$count" | grep -o "^[0-9]*" ) ))
    done

    P=$( dc -e "5k$zinrou_c $max_c/100*p" )
    printf "%9.5f,%s\n" $P "$word"
done
