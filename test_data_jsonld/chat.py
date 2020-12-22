import os, re, json, sys

if len(sys.argv) < 3:
    print('Usage:', sys.argv[0], '<TEMPLATE FILE> <MESSAGE>', file=sys.stderr)
    exit(1)

with open(sys.argv[1], 'r') as f:
    model = json.loads(f.read())

model['text']['@value'] = sys.argv[2]

print(model)
