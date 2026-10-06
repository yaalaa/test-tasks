"""
python -m tryout.yaml_align
"""
from __future__ import annotations


def y2s( 
    value
):
    
    import yaml
    class str1( str ):
        indent_right : int
        @classmethod
        def from_str( cls, s, indent_right ):
            out = cls( s )
            out.indent_right = indent_right
            return out
        @classmethod
        def patch_scalar_node( cls, node, max_w ):
            if isinstance( node.value, str ):
                node.value = cls.from_str( node.value, indent_right = max_w - len( node.value ) )
            return node
    class MyDumper( yaml.Dumper ):
        def represent_mapping( self, tag, mapping, flow_style = None ):
            node = super().represent_mapping( tag = tag, mapping = mapping, flow_style = flow_style )
            if isinstance( mapping, dict ) and mapping and all(( isinstance( k, str ) for k in mapping.keys() ) ):
                max_w = max(( len( k.value ) for k, _ in node.value ))
                node.value = [
                    ( str1.patch_scalar_node( k, max_w = max_w ), v )
                    for k,v in node.value
                ]
            return node
        def process_scalar( self ):
            super().process_scalar()
            if isinstance( self.event.value, str1 ) and self.event.value.indent_right > 0:
                self.write_indicator( ' ' * self.event.value.indent_right, False )

    return yaml.dump( value, Dumper = MyDumper, default_flow_style = False )


src = """
{
    "id" : "007",
    "given_name" : "James",
    "surname" : "Bond",
    "title" : "agent",
    "weapon": "Beretta"
}
"""

import json
d   = json.loads( src )
s   = y2s       ( d   )
print( f'{'-' * 32}' )
print( s )
print( f'{'-' * 32}' )
