import regex

r1 = r'(?:(.)\1{2}(?:\1{3})*)(?:(.)\2{2})+'
r2 = r'(?:(.)\1{2})*'


s = 'CCCCAAADDD'

ms = [ m.group() for m in regex.finditer( r2, s, overlapped = True ) if m ]
if not ms:
    print( f'.not-found.' )
else:
    m = max( ms, key = lambda it: len( it ) )
    print( f'Found: len: {len( m )}' )
    print( f'{'-' * 16}' )
    print( f'{m}' )
    print( f'{'-' * 16}' )

