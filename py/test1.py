
class A:
    def __init__( self, n ):
        self.n = n

    @classmethod
    def make( cls, n ):
        return cls( n )

    def p( self ):
        print( self.n )


class B (A):
    def __init__( self, n ):
        super(B, self).__init__( n + 10 )


B.make(10).p()
