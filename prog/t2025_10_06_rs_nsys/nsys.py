

digits = [
    ch
    for ch in '0123456789'
] + [
    ch
    for ch in 'abcdefghijklmnopqrstuvwxyz'
]

def to_base( n, base ):
    if n == 0: return '0'
    s = ''
    q = n
    while q > 0:
        s = digits[ q % base ] + s
        q  = int( q / base )
    return s

n = 277

for p in range( 8, len( digits ) ):
    print( p )
    s = to_base( n, p )
    if s[ -2: ] == '37':
        print( f'p = {p} - {s}' )
        break
else:
    print( f'no found' )
