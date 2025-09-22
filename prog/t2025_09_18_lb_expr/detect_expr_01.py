import regex

rnum  = r'(?:0|[1-9][0-9]*)'
rmul  = fr'{rnum}(?:\*{rnum})*'
rmul2 = fr'(?:{rmul}\*)?0(?:\*{rmul})?'
rsum  = fr'{rmul2}(?:\+{rmul2})*'

print( rsum )

