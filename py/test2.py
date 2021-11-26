
def water( heights ):
    total    = 0
    cnt      = len( heights )
    idx      = 0
    while idx < cnt:
        v = heights[ idx ]

        while True:

            # skip same elements
            idx2  = idx + 1
            while idx2 < cnt:
                v2 = heights[ idx2 ]
                if v2 != v: break
                idx2 += 1
            if idx2 >= cnt: # at end
                idx = cnt
                break

            # look for height
            idx3  = idx2
            while idx3 < cnt:
                v3 = heights[ idx3 ]
                if v3 >= v: break
                idx3 += 1

            if idx3 < cnt: # found something
                total += v * ( idx3 - idx2 ) - sum( heights[ idx2 : idx3 ] )
                idx = idx3
                break

            # nothing high
            v = max( heights[ idx2 : ] )

    return total


a = [ 2, 5, 1, 3, 1, 2, 1, 7, 7, 6 ]


print( water( a ) )
