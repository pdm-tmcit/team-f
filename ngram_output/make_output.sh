#!/bin/bash
ls | grep "h.*ngram[0-9]*\.txt$" | while read l
do
    if [ -f "$l.checked" ]
    then
        cat "$l.checked"
    else
        ./check_ngram.sh "$l" >"$l.checked"
        cat "$l.checked"
    fi | ./cal_P_zinrou.sh
done | sort -n >output.txt
