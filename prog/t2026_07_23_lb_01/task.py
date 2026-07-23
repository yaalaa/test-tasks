import io
import traceback

import regex

FN = '24.txt'
with io.open( FN, encoding = 'utf-8' ) as f:
    s = f.readline().strip()


def test( re_expr, overlap ):
    try:
        def ln( occ ): return occ.end() - occ.start()
        return ln( max( regex.finditer( re_expr, s, overlapped = overlap ), key = ln ) )
    except Exception:
        print( 'test: failed with exception' )
        traceback.print_exc()
        return -1

number = r'[1-9]+'
expr   = fr'{number}(?:[+*]{number}){{0,49}}'
expr2  = fr'{number}(?:[+*]{number})*'

for ( title, re_expr ) in [
    ( 'LB' , expr  ),
    # ( 'LB*', expr2 ),
]:
    for ovr in ( False, True ):
        print( f'{title:10} - ovr: {f'{ovr}':5} - {test( re_expr, ovr ):6}' )
        # print( f'{'-' * 32}\n{re_expr}\n{'-' * 32}' )

print( '.done.' )
