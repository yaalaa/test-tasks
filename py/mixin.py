
class A:
    def do_something( self, param ):
        print( f'A.do_something: {param=}' )
    def do_more( self, param1, param2 ):
        print( f'A.do_more: {param1=} - {param2=}' )
        self.do_something( param2 )


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
a = A()
a.do_something( 'a' )
a.do_more( 'A2', 'A2' )
print( f'{'-' * 16} B {'-' * 16}' )
b = B()
b.do_something( 'b' )
b.do_more( 'B2', 'B2' )
print( f'{'-' * 16} C {'-' * 16}' )
c = C()
c.do_something( 'c' )
c.do_more( 'C2', 'C2' )
print( f'{'-' * 16} D {'-' * 16}' )
d = D()
d.do_something( 'd' )
d.do_more( 'D2', 'D2' )
print( f'{'-' * 16}---{'-' * 16}' )
