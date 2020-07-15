#!/bin/bash
# もしargv[0]が0以上だったら、headする
function head_file() {
    [ $1 -ne 0 ] && head -n $1 || cat
}

function make_zinroucsv() {
    find village_talklist -type f -name "*.csv" | xargs grep ",人狼,"
}

function get_message() {
    awk -F, '{ for(i=4;i<NF;i++)printf("%s", $i);print $NF }'
}

# ファイル作成
if ! [ -d village_talklist ]
then
    echo "village_talklistのディレクトリが見つからない"
    echo "https://drive.google.com/drive/folders/1cCUrKPtL-xQAd_y9OBnvRrv-vfXXjkA_からダウンロードしてきて"
    exit 1
fi >&2

[ -d ngram_output ] || mkdir ngram_output
[ -f zinrou.csv ]   || make_zinroucsv

head_line=$( [ -n $1 ] && echo "0" || echo $1 )
for i in `seq 2 6`
do
    echo "[+] Start $i"
    cat zinrou.csv | head_file $head_line | get_message | while read l
    do
            echo "$l" | ./ngram.py $i
    done | sort | uniq -c | sort -n >"ngram_output/h${head_line}_ngram$i.txt"
done
