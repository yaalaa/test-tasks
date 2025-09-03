
#a = [ 2, 8, 4 ]
a = [ -5, 8, 9, -4, -3 ]

n = len( a )

s2 = sum( v * v for v in a )

p = 0
t = 0
for i in range( n - 1, 0, -1 ):
  t += a[ i + 1 - 1 ]
  p += a[ i - 1 ] * t


s = s2 * ( n - 1 ) - 2 * p


print( a )
print( s )

