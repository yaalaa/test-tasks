import io
import time
import traceback

import regex

FN = '24_25036900.txt'
with io.open( FN, encoding = 'utf-8' ) as f:
    s = f.readline().strip()


def test( re_expr, srcs ):
    try:
        def ln( occ ): return occ.end() - occ.start()
        return ln( max( regex.finditer( re_expr, srcs, overlapped = True ), key = ln ) )
    except Exception:
        print( 'test: failed with exception' )
        traceback.print_exc()
        return -1

expr  = r'(?:(.)\1\1*\1)(?:(.)\2{2})*'
expr2 = r'(?:(.)\1\1)*' 

for ( title, re_expr, corr ) in [
    ( 'LB'  , expr  , lambda v: v - v % 3 ),
    ( 'LB2' , expr2 , None ),
]:
    for test_name, test_src in [
        #( 'A'          , 'A'      ),
        #( 'K'          , 'K'      ),
        #( 'L'          , 'L'      ),
        #( 'KLTTKL'     , 'KLTTKL' ),
        ( FN           , s        ),
    ]:
        ts_start = time.monotonic()
        res       = test( re_expr, test_src )
        if corr: res = corr( res )
        ts_end   = time.monotonic()
        print( f'{title:10} - {test_name:14} - {res:6} - {ts_end - ts_start:.3f}s' )

print( '.done.' )
