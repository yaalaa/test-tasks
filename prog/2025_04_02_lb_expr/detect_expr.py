import io
import regex

fn = 'tests/24-10.txt'

with io.open( fn ) as f:
    data = f.readline()

#print( f'Input data len: {len( data )}' )

num_regex    = r'(?:[1-9]\d*)?[02468]'
op_regex     = f'[*+]'
lookup_regex = f'(?<!\d)(?:{num_regex})(?:(?:{op_regex})(?:{num_regex}))*(?!\d)'
print( f'{lookup_regex}' )
found = max( ( m.group() for m in regex.finditer( lookup_regex, '+' + data + '+' ) ), key = lambda v: len( v ))

if not found:
    print( f'Not found' )
else:
    print(( f'Found len: {len( found )}' ))
    print(( f'Text\n{'-' * 16}\n{found}\n{'-' * 16}\n' ))

