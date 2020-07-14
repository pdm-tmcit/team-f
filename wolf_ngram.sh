#!/bin/bash
function head_file() {
    if [ $1 -ne 0 ]
    then
        cat | head -n $1
     else
         cat
     fi
}

head_line=0
if [ -n $1 ]
then
    head_line=$1
fi

for i in `seq 2 6`
do
    echo "[+] Start $i"
    cat zinrou.csv | head_file $head_line | awk -F, '{print $4}' | while read l
    do
            echo "$l" | ./ngram.py $i
    done | sort | uniq -c | sort -n >"ngram_output/h${head_line}_ngram$i.txt"
done
