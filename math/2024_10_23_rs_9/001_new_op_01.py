
def new_op( a, b ): return a * b - a % b

def calc_seq( seq ):
    if not  seq       : return 0
    if len( seq ) == 1: return seq[ 0 ]
    acc = seq[ 0 ]
    for cur in seq[ 1: ]:
        acc = new_op( acc, cur )
    return acc

def gen_reposition( acc, left ):
    if not left:
        yield acc
        return
    if len( left ) == 1:
        yield acc + left
        return
    for idx in range( len( left ) ):
        yield from gen_reposition( acc + left[ idx : idx + 1 ], left[ : idx] + left[ idx + 1 : ] )



data = list( range( 1, 7 ) )

print( f'Input  : {data}' )

# get maximum
max_v = 0
max_r = []
cnt   = 0
for r_idx, r in enumerate( gen_reposition( [], data ) ):
    #print( f'{r_idx:5}: {r} : {calc_seq( r )}')
    cnt  += 1
    cur_v = calc_seq( r )
    if cur_v <= max_v: continue
    max_v = cur_v
    max_r = r
print( f'Best   : {max_r} - {max_v}' )

