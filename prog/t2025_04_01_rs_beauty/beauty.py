# 10
# 1 2 3 3 2 4 7 6 7 8

from   __future__  import annotations
import dataclasses

# input
n = int( input().strip() )
h = [ int( s.strip() ) for s in input().split() ]
if n != len( h ):
    print( f'n differs from actual array length' )
    exit( -1 )
# print( f'Input:')
# print( f'{n=}' )
# print( f'{h=}' )

# reduce
def reduce_heights( heights ):
    cnt       = len( heights )
    if cnt <= 1: return heights
    ordered   = sorted( enumerate( heights ), key = lambda it: it[ 1 ] )
    dense     = [ 0 ] * cnt
    val       = 0
    prev      = 0
    for idx, old_val in ordered:
        if old_val > prev:
            prev = old_val
            val += 1
        dense[ idx ] = val
    return dense

# too few RAM
@dataclasses.dataclass()
class Value:
    idx    : int = 0
    horz   : int = 0
    beauty : int = 0

def calc_beauty( heights, start : Value = None ):
    cnt = len( heights )
    cur = dataclasses.replace( start ) if start else Value()
    while cur.idx < cnt:
        house = heights[ cur.idx ]
        if house > cur.horz:
            cur.beauty += 1
            cur.horz    = house
        cur.idx += 1
    return cur

def look_up( heights ) -> Value:
    cnt  = len( heights )
    best = Value()
    cur  = Value()
    while cur.idx < cnt:
        house = heights[ cur.idx ]
        if house != cur.horz + 1 and cur.beauty + ( cnt - cur.idx ) > best.beauty:
            tweaked = calc_beauty(
                heights,
                start = Value(
                    idx    = cur.idx    + 1,
                    horz   = cur.horz   + 1,
                    beauty = cur.beauty + 1,
                )
            )
            if tweaked.beauty > best.beauty: best = tweaked

        if house > cur.horz:
            cur.beauty += 1
            cur.horz    = house
        cur.idx += 1
    if cur.beauty > best.beauty : best = cur
    return best

#initial_beauty = calc_beauty( h ).beauty
# print( f'\nInitial beauty: {initial_beauty}' )

if n <= 1:
    # print( f'Beauty is enough' )
    print( f'{calc_beauty( reduce_heights( h ) ).beauty}' )
    exit( 0 )

most_beauty = look_up( h ).beauty

# print( f'Most beauty' )
print( f'{most_beauty}' )
