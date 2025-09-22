"""
екстовый файл содержит только заглавные буквы A, B, C, D, E, F и U.
Определите максимальное количество идущих подряд символов, среди которых комбинация согласная + гласная + согласная встречается ровно 2 раза.
"""
import io
import regex

fn = 'tests/24_25037852.txt'

with io.open( fn ) as f:
    data = f.readline()


# \S\s?(?:p2|p1\s?p1)\s?\S


rv         = r'[AEU]'
sv         = { 'A', 'E', 'U' }
rc         = r'[BCDF]'
rpiece1    = fr'{rc}{rv}{rc}'
rpiece2    = fr'{rc}{rv}{rc}{rv}{rc}'
rpiece     = fr'{rpiece2}|{rpiece1}'
ch_chars   = r' '
ch_piece1  = 'a'
ch_piece2  = 'b'
ch_org     = 'o'
ch_end     = 'e'
r_code     = fr'\S\s?(?:{ch_piece2}|{ch_piece1}\s?{ch_piece1})\s?\S'
def get_part_code( p ): return ch_chars if not regex.fullmatch( rpiece, p ) else ( ch_piece1 if len( p ) == 3 else ch_piece2 )
parts      = regex.split( fr'({rpiece})', data )
part_codes = ch_org + ''.join( get_part_code( part ) for part in parts ) + ch_end
def find_expr( start, just_len = False ):
    m_code    = regex.match( r_code, part_codes, pos = start )
    if not m_code: return 0 if just_len else 0
    code      = m_code.group()
    code_len  = len( code )
    if just_len:
        s_len = sum( len( parts[ idx - 1 ] ) for idx in range( start + 1, start + code_len - 1 ) )
        if code[  0 ] in { ch_piece2, ch_piece1 }: s_len += 2
        if code[ -1 ] in { ch_piece2, ch_piece1 }: s_len += 2
        return s_len
    s         = ''.join( parts[ start : start + code_len - 2 ] )
    if code[  0 ] in { ch_piece2, ch_piece1 }: s =     parts[ start            - 1 ][ -2 :   ] + s
    if code[ -1 ] in { ch_piece2, ch_piece1 }: s = s + parts[ start + code_len - 1 ][    : 2 ]
    return s

expr_lens = [ find_expr( idx, just_len = True ) for idx in range( len( parts ) ) ]
max_idx   = max( range( len( parts ) ), key = lambda idx: expr_lens[ idx ] )
max_expr  = find_expr( max_idx )

print( f'len: {len( max_expr )} (file len: {len( data )})' )
print( f'{'-' * 16}')
print( f'{max_expr}')
print( f'{''.join( ( '-' if ch in sv else ' ' ) for ch in max_expr )}' )
print( f'{'-' * 16}')

