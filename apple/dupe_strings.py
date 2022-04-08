import io
import re
import os
import sys

input_fn = sys.argv[1]
if not input_fn:
    print('Error: no input file')
    exit(1)

print( f'Input: {input_fn}')

if not os.path.isfile(input_fn):
    print(f'Error: does not exist - {input_fn}')
    exit(1)

with io.open(input_fn, mode = 'r' ) as f:
    lines = f.readlines()

data = {}
for idx, line in enumerate(lines):
    l = line.strip()
    if not l                : continue # empty
    if not l.startswith('"'): continue # comment or something wierd
    m = re.fullmatch(r'"(?P<key>[^"]+)"\s*=\s*"(?P<val>.*)"\s*;', l)
    if not m                : continue # bad one
    key = m.group('key')
    val = m.group('val')
    if not key              : continue # still bad
    if key in data: # dupe
        key_pad = ' ' * max( 0, 32 - len( key ) )
        print(f'Dupe: "{key}"{key_pad} line {idx: 5} dupes line {data[key]["idx"]: 5}')
        continue
    data[key] = {
        'idx' : idx,
        'val' : val
    }

