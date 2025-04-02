//
// g++ ./beauty.cpp -o ./beauty
// ./beauty <./tests/test_01.txt
// ./beauty <./tests/test_02.txt
//

#include <stdio.h>

struct Value {
    int horz   = 0;
    int beauty = 0;
};

struct MemLink {
    MemLink *next  = NULL;
    Value    value;
};

struct Node {
    int      height = 0;
    int      horz   = 0;
    Value    fix;
    MemLink *mem = NULL;

    int get_mem( int horz ) {
        MemLink *m = this->mem;
        for ( ; m && m->value.horz != horz; m = m->next ) {
        }
        return m ? m->value.beauty : -1;
    }

    void set_mem( int value ) {
        MemLink *newMem = new MemLink;
        newMem->next  = mem;
        newMem->value = fix;
        newMem->value.beauty = value - newMem->value.beauty;
        mem           = newMem;
    }

    void setup( const Value &value ) {
        fix = value;
    }

    static void set_mem_range( Node *nodes, int start_idx, int end_idx, int beauty ) {
        for ( int idx = start_idx; idx < end_idx; idx++ ) {
            nodes[ idx ].set_mem( beauty );
        }
    }
};

int calc_beauty( Node *nodes, int node_cnt, int start_idx = 0, const Value *start_value = NULL ) {
    int   idx = start_idx;
    Value cur = start_value ? *start_value : Value();
    for ( ; idx < node_cnt; idx++ ) {
        Node &node    = nodes[ idx ];
        int   already = node.get_mem( cur.horz );
        if ( already >= 0 ) {
            int out = cur.beauty + already;
            Node::set_mem_range( nodes, start_idx, idx, out );
            return out;
        }
        node.setup( cur );
        if ( node.height > cur.horz ) {
            cur.beauty++;
            cur.horz = node.height;
        }
    }
    Node::set_mem_range( nodes, start_idx, node_cnt, cur.beauty );
    return cur.beauty;
}

int look_up( Node *nodes, int node_cnt ) {
    int   best = 0;
    Value cur;
    for ( int idx = 0; idx < node_cnt; idx++ ) {
        Node &node = nodes[ idx ];
        node.horz = cur.horz;

        do {
            if ( node.height == cur.horz + 1 ) {
                break;
            }
            if ( idx >= 2 && node.height <= nodes[ idx - 2 ].horz && nodes[ idx - 1 ].height <= nodes[ idx - 2 ].horz ) {
                break;
            }
            if ( idx < node_cnt - 1 && cur.horz < node.height && node.height < nodes[ idx + 1 ].height ) {
                break;
            }
            Value start_val = cur;
            start_val.horz  ++;
            start_val.beauty++;
            int   tweaked   = calc_beauty(
                nodes,
                node_cnt,
                idx + 1,
                &start_val
            );
            if ( tweaked > best ) {
                best = tweaked;
            }
        } while ( false );

        if ( node.height > cur.horz ) {
            cur.beauty++;
            cur.horz = node.height;
        }
    }
    if ( cur.beauty > best ) {
        best = cur.beauty;
    }
    return best;
}

int main( int argc, const char **argv ) {
    int n = 0;
    scanf( "%d", &n );
    int *h = new int[ n ];
    for ( int idx = 0; idx < n; idx++ ) {
        scanf( "%d", &h[ idx ] );
    }

     // printf( "n = %d\n", n );
     // for ( int idx = 0; idx < n; idx++ ) {
     //     printf( idx ? " %d" : "%d", h[ idx ] );
     // }
     // printf( "\n" );

    // initialize structures
    Node *nodes = new Node[ n ];
    for ( int idx = 0; idx < n; idx++ ) {
        nodes[ idx ].height = h[ idx ];
    }
    // printf( "Initial: %d\n", calc_beauty( nodes, n ) );

    // look up
    int most_beauty = look_up( nodes, n );

    // dupe output
    printf( "%d\n", most_beauty );
}
