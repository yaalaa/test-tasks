"""
python -m tryout.json_align
"""
from __future__ import annotations


def s2jms( s, special_quote = '\u301e' ):
    def s2js( s : str ): 
        return ''.join((
            '"',
            ( s.replace( '"', special_quote ) if special_quote else s ).replace( '\\', '\\\\' ).replace( '"', '\\"' ),
            '"',
        ))
    return '  ' + '\n+ '.join( s2js( l ) for l in s.splitlines() )


def j2s( 
    value, 
    level_indent = 4,
):
    import io
    import json
    buff = io.StringIO()
    def p    ( s ): print( s, file = buff, end = '' )
    def p_lf (   ): p( '\n' )
    def p_ind( l ): p( ' ' * ( l * level_indent ) )
    try:
        def do_value( val, level, need_indent, need_comma = False ):
            def p_ind2( l = 0 ): p_ind( level + l )
            def p_ind2i(      ): p_ind2() if need_indent else None      
            def p_c     (     ): p( ',' ) if need_comma  else None
            if isinstance( val, dict ):
                if val:
                    p_ind2i(); p( '{' ); p_lf()
                    ks   = sorted( val.keys() )
                    ks_n = len( ks )
                    pks  = [ json.dumps( k ) for k in ks ]
                    w_k  = max(( len( pk ) for pk in pks ))
                    for k_idx in range( ks_n ):
                        p_ind2( 1 ); p( f'{pks[ k_idx ]:{w_k}}' ); p( ' : ' )
                        do_value( val[ ks[ k_idx ] ], level = level + 1, need_indent = False, need_comma = k_idx < ks_n - 1 )
                    p_ind2 (); p( '}' ); p_c(); p_lf()
                else:
                    p_ind2i(); p( '{}' ); p_c(); p_lf()
            elif isinstance( val, ( list, tuple ) ):
                if val:
                    v_n = len( val )
                    p_ind2i(); p( '[' ); p_lf()
                    for v_idx in range( v_n ):
                        do_value( val[ v_idx ], level = level + 1, need_indent = True, need_comma = v_idx < v_n - 1 )
                    p_ind2 (); p( ']' ); p_c(); p_lf()
                else:
                    p_ind2i(); p( '[]' ); p_c(); p_lf()
            else:
                p_ind2i(); p( json.dumps( val ) ); p_c(); p_lf()
        do_value( value, level = 0, need_indent = True )
        return buff.getvalue()
    finally:
        buff.close


src = """
{
    "id" : "007",
    "given_name" : "James",
    "surname" : "Bond",
    "title" : "agent",
    "weapon": "Beretta"
}
"""

import json
d   = json.loads( src )
s   = j2s       ( d   )
mjs = s2jms     ( s   )
print( f'{'-' * 32}' )
print( s )
print( f'{'-' * 32}' )
print( mjs )
print( f'{'-' * 32}' )
