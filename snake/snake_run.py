from   __future__  import annotations
import curses
import dataclasses
import random
import time


@dataclasses.dataclass( frozen = True)
class Options:
    time_step_ms : int   = 20
    time_sleep   : float = time_step_ms / 1000
    rows         : int   = 25
    cols         : int   = 80
    speed_base   : float = 2
    line_accel   : float = 10
    ch_food              = 'X'
    ch_snake             = 'O'
    ch_space             = ' '

    def calc_cell_idx( self, row, col ): return    row * self.cols +    col
    def calc_pt_idx  ( self, pt       ): return pt.row * self.cols + pt.col
    def pt_from_idx  ( self, idx      ): return Point( row = int( idx / self.cols ), col = idx % self.cols )


@dataclasses.dataclass
class Point:
    row : int = 0
    col : int = 0


@dataclasses.dataclass
class Food:
    # kinds
    KIND_SIMPLE = 'simple'
    # common
    FOOD_MAX    = 20
    # new simple food
    SIMPLE_LIFE = 25
    SIMPLE_BORN =  5
    SIMPLE_OFS  =  2

    pt         : Point
    kind       : str
    born       : int
    expiration : int


class State:
    def __init__( self, opts :  Options, wnd ):
        self.exit       = False
        self.changed    = False
        self.key        = None
        self.time       = 0
        self.wnd        = wnd
        self.opts       = opts
        self.tail : [ Point ] = [ Point( row = int( opts.rows / 2 ), col = int( opts.cols / 2 ) ) ]
        self.dir  :   Point   = Point( row = 0, col = 1 )
        self.accel_line = 0
        self.acc        = 0
        self.food : [ Food  ] = []
        self.all        = { self.opts.calc_cell_idx( r, c ) for r in range( self.opts.rows ) for c in range( self.opts.cols ) }
        # draw snake
        self.draw_pt( self.tail[ 0 ], self.opts.ch_snake )

    def get_free_cels( self ) -> set:
        return ( self.all
                - { self.opts.calc_pt_idx(   pt ) for pt in self.tail }
                - { self.opts.calc_pt_idx( f.pt ) for f  in self.food }
                )

    def draw_pt( self, pt : Point, ch ):
        self.wnd.addch( pt.row, pt.col, ord( ch ) )

    def do( self ):
        self.do_food ()
        self.do_snake()
        if self.exit: return

        if self.key: self.exit = True

    def do_food( self ):
        # remove expired
        for f in self.food:
            if f.expiration > self.time: continue
            self.draw_pt( f.pt, self.opts.ch_space )
            self.changed = True
        self.food = [ f for f in self.food if f.expiration > self.time ]
        # simple
        if len( self.food ) < Food.FOOD_MAX and self.time % int( Food.SIMPLE_BORN / self.opts.time_sleep ) == int( Food.SIMPLE_OFS / self.opts.time_sleep ):
            free_cels = self.get_free_cels()
            if free_cels:
                food_pt = self.opts.pt_from_idx( random.choice( list( free_cels ) ) )
                self.food.append( Food(
                    pt         = food_pt,
                    kind       = Food.KIND_SIMPLE,
                    born       = self.time,
                    expiration = self.time + Food.SIMPLE_LIFE / self.opts.time_sleep,
                ) )
                self.draw_pt( food_pt, self.opts.ch_food )
                self.changed = True

    def do_snake( self ):
        # snake direction
        if   self.key == 'KEY_LEFT' : new_dir = Point( row =  0, col = -1 ); self.key = None
        elif self.key == 'KEY_RIGHT': new_dir = Point( row =  0, col =  1 ); self.key = None
        elif self.key == 'KEY_UP'   : new_dir = Point( row = -1, col =  0 ); self.key = None
        elif self.key == 'KEY_DOWN' : new_dir = Point( row =  1, col =  0 ); self.key = None
        else                        : new_dir = None
        if new_dir:
            self_collision = new_dir.row * self.dir.row + new_dir.col * self.dir.col
            if self_collision < 0:
                self.exit = True
                return
            if new_dir != self.dir: self.dir = new_dir
        # snake mode
        self.acc += min( 1, self.opts.speed_base * ( 1 + self.accel_line ) * self.opts.time_sleep )
        if self.acc >= 1:
            # new point
            prev_pt    = self.tail[ -1 ]
            new_pt     = Point( row = prev_pt.row, col = prev_pt.col )
            new_pt.row = ( new_pt.row + self.opts.rows + self.dir.row ) % self.opts.rows
            new_pt.col = ( new_pt.col + self.opts.cols + self.dir.col ) % self.opts.cols
            # self-collision
            if any(( new_pt == pt for pt in self.tail )):
                self.exit = True
                return
            # food collision
            for f_idx, f in enumerate( self.food ):
                if f.pt == new_pt: break
            else: f = None; f_idx = -1
            if f:
                self.food = self.food[ : f_idx ] + self.food[ f_idx + 1 : ]
                # speed up
                self.accel_line += self.opts.line_accel / 100
            # step forward
            self.acc  -= 1
            # draw
            if not f: self.draw_pt( self.tail[ 0 ], self.opts.ch_space )
            self.draw_pt( new_pt, self.opts.ch_snake )
            self.changed = True
            # adjust tail
            if f: self.tail += [ new_pt ]
            else: self.tail  = self.tail[ 1: ] + [ new_pt ]



if __name__ == '__main__':
    opts  = Options()
    state = None
    scr  = curses.initscr()
    try:
        curses.curs_set(0)
        wnd = scr.subwin( opts.rows, opts.cols, 0, 0 )
        wnd.nodelay( True )
        wnd.keypad ( True )
        wnd.border()
        wnd.refresh()
        state = State( opts = opts, wnd = wnd )
        while True:
            state.changed = False
            # key
            try:
                state.key = wnd.getkey()
            except Exception:
                state.key = None
            state.do()
            if state.changed: wnd.refresh()
            if state.exit   : break
            state.time += 1
            time.sleep( opts.time_sleep )
    finally:
        curses.endwin()
    print( f'\n\n{'-' * 16}\n.bye.\n{'-' * 16}' )
    if state:
        print( f'Time: {state.time * opts.time_sleep} s' )
        print( f'Tail: {len( state.tail )}' )
        if state.key:
            print( f'Key : {state.key}' )




