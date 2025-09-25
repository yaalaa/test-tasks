import io
import regex

#r1 = r'(?:(.)(?:\1)*(?!\1)(.)(?:\1|\2)*)'
#r1 = r'(.)(?:\1)*(?!\1)(.)(?:\1|\2)*'
r1 = r'(.)\1*(?!\1)(.)(?:\1|\2)*'


s = 'aaabbzzzz'

# fn = 'tests/24_25036902.txt'
# with io.open( fn ) as f:
#     s = f.readline()


#ms = [ m.group() for m in regex.finditer( r1, s ) if m ]
ms = [ m.group() for m in regex.finditer( r1, s, overlapped = True ) if m ]
if not ms:
    print( f'.not-found.' )
else:
    m = max( ms, key = lambda it: len( it ) )
    print( f'Found: len: {len( m )}' )
    print( f'{'-' * 16}' )
    print( f'{m}' )
    print( f'{'-' * 16}' )

