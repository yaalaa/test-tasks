
def water( heights ):
    total = 0
    cnt   = len( heights )
    idx   = 0
    while idx < cnt:
        v = heights[ idx ]

        while True:

            # look for height
            idx2  = idx + 1
            while idx2 < cnt:
                v2 = heights[ idx2 ]
                if v2 >= v: break
                idx2 += 1

            if idx2 <= idx + 1:
                idx = idx2
                break

            if idx2 < cnt: # found something
                total += v * ( idx2 - idx - 1 ) - sum( heights[ idx + 1 : idx2 ] )
                idx = idx2
                break

            # nothing high
            v = max( heights[ idx + 1 : ] )

    return total


a = [ 2, 5, 1, 3, 1, 2, 1, 7, 7, 6 ]


print( water( a ) )
