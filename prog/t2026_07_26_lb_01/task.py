import io
import time
import traceback

import regex

FN = 'f_37131.txt'
with io.open( FN, encoding = 'utf-8' ) as f:
    s = f.readline().strip()


def test( re_expr ):
    try:
        def ln( occ ): return occ.end() - occ.start()
        return ln( max( regex.finditer( re_expr, s, overlapped = True ), key = ln ) )
    except Exception:
        print( 'test: failed with exception' )
        traceback.print_exc()
        return -1

expr  = r'(?:.(?:(?<!K)L|[^KL]|(?<!L)K)*)'
expr2 = r'.(?:.(?!LK|KL))+' 

for ( title, re_expr ) in [
    ( 'LB'  , expr  ),
    ( 'LB2' , expr2 ),
]:
    ts_start = time.monotonic()
    res       = test( re_expr )
    ts_end   = time.monotonic()
    print( f'{title:10} - {res:6} - {ts_end - ts_start:.3f}s' )

print( '.done.' )
