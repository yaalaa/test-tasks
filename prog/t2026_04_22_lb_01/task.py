import io

sep     = 'BC'
sep_max = 180
fn      = '24-14.txt'
with io.open( fn, mode = 'r', encoding = 'utf-8' ) as f:
    d = f.read()

parts       = [ len( s ) for s in d.split( sep ) ]
sep_len     = len( sep )
parts_total = sum( parts )
check_len   = parts_total + ( len( parts ) -1 ) * sep_len

print( f'File len  : {len( d )}')
print( f'Part cnt  : {len( parts )}')
print( f'Part total: {parts_total}')
print( f'Check len : {check_len}')

if len( parts ) - 1 <= sep_max:
    print( f'Answer: whole file' )
    exit( -1 )

best_start = -1
best_len   = -1

for idx in range( len( parts ) - sep_max -1 ):
    cur_len = sum( parts[ idx : idx + sep_max + 1 ] ) + sep_max * sep_len
    if idx > 0                     : cur_len += 1
    if idx + sep_max < len( parts ): cur_len += 1
    if cur_len > best_len:
        best_len   = cur_len
        best_start = idx

print( f'Answer: {best_len}' )

