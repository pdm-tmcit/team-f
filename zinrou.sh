cat zinrou.csv | awk -F, '{ for(i=4;i<NF;i++)printf("%s", $i);print $NF }'
