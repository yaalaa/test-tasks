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


@dataclasses.dataclass()
class Node:
    mem    : dict = None
    horz   : int  = 0
    beauty : int  = 0

    def get_mem( self, horz  ): return ( self.mem or {} ).get( horz )
    def set_mem( self, value ):
        if self.mem is None: self.mem = {}
        self.mem[ self.horz ] = value - self.beauty
    def setup  ( self, horz, beauty ):
        self.horz   = horz
        self.beauty = beauty


def calc_beauty( heights, start : Value = None, memory : list[ Node ] = None ) -> int:
    cnt = len( heights )
    cur = dataclasses.replace( start ) if start else Value()
    while cur.idx < cnt:
        if memory:
            node    = memory[ cur.idx ]
            already = node.get_mem( cur.horz )
            if already is not None:
                out = cur.beauty + already
                for mem_idx in range( start.idx if start else 0, cur.idx ):
                    memory[ mem_idx ].set_mem( out )
                return out
            node.setup( cur.horz, cur.beauty )
        house = heights[ cur.idx ]
        if house > cur.horz:
            cur.beauty += 1
            cur.horz    = house
        cur.idx += 1
    out = cur.beauty
    if memory:
        for mem_idx in range( start.idx if start else 0, cnt ):
            memory[ mem_idx ].set_mem( out )
    return out

def look_up( heights ) -> int:
    cnt    = len( heights )
    memory = [ Node() for _ in range( cnt ) ]
    best   = 0
    cur    = Value()
    while cur.idx < cnt:
        house = heights[ cur.idx ]
        if house != cur.horz + 1:
            tweaked = calc_beauty(
                heights,
                start = Value(
                    idx    = cur.idx    + 1,
                    horz   = cur.horz   + 1,
                    beauty = cur.beauty + 1,
                ),
                memory = memory,
            )
            if tweaked > best: best = tweaked

        if house > cur.horz:
            cur.beauty += 1
            cur.horz    = house
        cur.idx += 1
    if cur.beauty > best : best = cur.beauty
    return best

#initial_beauty = calc_beauty( h ).beauty
# print( f'\nInitial beauty: {initial_beauty}' )

if n <= 1:
    # print( f'Beauty is enough' )
    print( f'{calc_beauty( h )}' )
    exit( 0 )

most_beauty = look_up( h )

# print( f'Most beauty' )
print( f'{most_beauty}' )
