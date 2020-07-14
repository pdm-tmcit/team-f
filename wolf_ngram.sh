#!/bin/bash
# もしargv[0]が0以上だったら、headする
function head_file() {
    [ $1 -ne 0 ] && head -n $1 || cat
}

head_line=$( [ -n $1 ] && echo "0" || echo $1 )

for i in `seq 2 6`
do
    echo "[+] Start $i"
    cat zinrou.csv | head_file $head_line | awk -F, '{print $4}' | while read l
    do
            echo "$l" | ./ngram.py $i
    done | sort | uniq -c | sort -n >"ngram_output/h${head_line}_ngram$i.txt"
done
