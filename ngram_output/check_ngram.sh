#!/bin/bash
if ! [ -f "$1" ]
then
    echo "Usage: $0 <ngram.txt>" >&2
    exit 1
fi

cat "$1" | tail -n 30 | while read l
do
    word="$( echo "$l" | awk -F' ' '{ print $2 }' )"
    python -c "print('-'*40)"
    echo "$word"
    find ../village_talklist -type f -name "*.csv" | \
        xargs grep "$word" | \
        awk -F, '{ print $3 }' | \
        sort | uniq -c | sort -n
    python -c "print('-'*40)"
done
