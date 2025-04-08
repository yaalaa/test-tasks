import regex


rx = r'(?:(.)\1{2})+'

# test 1
s1 = 'BBCDDDEEEFGGGEEEDDDDK'
f1 = max( regex.finditer( rx, s1 ), key = lambda m: len( m.group() ))
print( f'{len( f1.group()): 3} - {f1.group()} - {s1}' )

