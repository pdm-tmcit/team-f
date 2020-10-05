import csv
import sys

rows = []
with open(sys.argv[1], 'r') as f:
    for reader in csv.reader(f):
        rows.append(reader)
for row in rows:
    print(row[3])
