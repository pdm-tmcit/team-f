#!/bin/bash
function get_message() {
    awk -F, '{ for(i=4;i<NF;i++)printf("%s", $i);print $NF }'
}

if ! [ -f ng.list ]
then
    echo "以下のコマンドを実行してNGリストを生成してください"
    echo "./make_output.sh | output2list.sh >ng.list"
    exit 1
fi >&2

TMPFILE="$0.tmp"

cat >"$TMPFILE"

cat ng.list | while read l
do
    cat "$TMPFILE" | grep "$l" | awk -F, '{ print $2 }'
done | sort | uniq -c | sort -n >"$TMPFILE.tmp"

maxc="$( cat "$TMPFILE.tmp" | grep -o "^[ 0-9]*" | tr "\n" "+" | sed 's/^/0/g;s/$/p/g' | dc )"

cat "$TMPFILE.tmp" | while read l
do
    name="$( echo "$l" | grep -o "[^ ]*$" )"
    count="$( echo "$l" | grep -o "^[ 0-9]*" )"
    echo "$( echo "5k100 $count*$maxc/p" | dc | sed 's/^\./0\./g' ),$name"
done
exit
rm -f "$TMPFILE*"
