
class A:
    def do_something( self, param ):
        print( f'A.do_something: {param=}' )


class B( A ):
    def do_something(self, param):
        print( f'B.do_something: {param=}' )
        return super().do_something(param)

class Mixin:
    def do_something(self, param):
        print( f'Mixin.do_something: {param=}' )
        return super().do_something(param)

class C( A, Mixin ):
    pass

class D( Mixin, A ):
    pass


print( f'{'-' * 16} A {'-' * 16}' )
A().do_something( 'a' )
print( f'{'-' * 16} B {'-' * 16}' )
B().do_something( 'b' )
print( f'{'-' * 16} C {'-' * 16}' )
C().do_something( 'c' )
print( f'{'-' * 16} D {'-' * 16}' )
D().do_something( 'd' )
print( f'{'-' * 16}---{'-' * 16}' )
