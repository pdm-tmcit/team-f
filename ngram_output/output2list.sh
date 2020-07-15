#!/bin/bash
cat output.txt | awk -F, '{ print $2 }' | while read word
do
    if ! ( cat output.txt | grep -v ",$word$" | grep "$word" >/dev/null )
    then
        echo "$word"
    fi
done
