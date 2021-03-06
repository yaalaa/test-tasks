# Parses Firebase devices stats CSV and outputs subtotals for OS version

import csv
import io
import os
import sys

if len( sys.argv ) < 2:
    print('Error: no filename')
    exit(1)
input_fn = sys.argv[ 1 ]
if not input_fn:
    print('Error: no filename')
    exit(1)
if not os.path.isfile(input_fn):
    print(f'Error: not exist - {input_fn}')
    exit(1)

KEY_PREFIXES   = [
    'iOS',
    'Android',
]
STRIP_PREFIXES = [
    # 'iOS',
]
STRIP_LEVEL    = 1
VER_SEP        = '.'
COL_DEVICE     = 'Device model'
COL_OS_VERSION = 'OS with version'
COL_USERS      = 'Users'
COL_PERCENT    = '%'
MARKER         = (
    COL_DEVICE,
    COL_OS_VERSION,
    COL_USERS
)

def process_os_version(value):
    # general checks
    if not value: return
    value = value.strip()
    if not value: return
    # key prefixes
    if KEY_PREFIXES:
        for prefix in KEY_PREFIXES:
            if value.startswith( prefix ):
                value = value[ len( prefix ): ].strip()
                if not value: return
                key = prefix
                break
        else:
            # no key prefix
            return
    else:
        key = None
    # prefixes
    for prefix in STRIP_PREFIXES:
        if value.startswith( prefix ):
            value = value[ len( prefix ): ].strip()
            if not value: return
            break
    # levels
    if STRIP_LEVEL > 0:
        parts = value.split( VER_SEP )
        if len( parts ) >= STRIP_LEVEL:
            parts = parts[ : STRIP_LEVEL ]
            value = VER_SEP.join( parts )
    return key, value



data           = {}
found_marker   = None
col_os_version = -1
col_users      = -1
with io.open( input_fn, mode = 'r' ) as f:
    reader = csv.reader( f, delimiter = ',' )
    for row in reader:

        if not found_marker:
            if row and tuple( row[ : len( MARKER ) ] ) == MARKER:
                found_marker = {
                    name : index
                    for index, name in enumerate( row )
                }
                col_os_version = found_marker.get( COL_OS_VERSION )
                col_users      = found_marker.get( COL_USERS      )
                if col_os_version is None or col_users is None:
                    print(f'Error: found marker but not the desired columns:\n    "{", ".join( row )}"')
                    break
        else:
            if not row                                       : break    # guess the end
            if len( row ) <= max( col_os_version, col_users ): break    # guess stup
            val_key, val_os_v  = process_os_version( row[ col_os_version ] ) or ( None, None )
            if not val_os_v                                  : continue # skip it
            val_users = row[ col_users ]
            if not val_users                                 : continue # skip it
            try:
                val_users_n = int( val_users )
            except ValueError:
                continue # skip it
            if not val_users_n                               : continue # skip it
            data    [ val_key  ] = data_key = data.get( val_key ) or {}
            data_key[ val_os_v ] = ( data_key.get( val_os_v ) or 0 ) + val_users_n

if not data: # nothing fount
    if not found_marker:
        print('Error: marker was not found')
        exit(1)
    print('Error: no data was found')
    exit(1)

sums = {
    key : sum( data_key.values() )
    for key, data_key in data.items()
}

pad_key = False
writer  = csv.writer( sys.stdout )
for key in sorted( data.keys() ):
    if pad_key:
        for _ in range( 2 ):
            writer.writerow( () )
    else:
        pad_key = True
    data_key = data[ key ]
    total    = sums[ key ]
    writer.writerow( ( key, ) )
    writer.writerow( ( COL_OS_VERSION, COL_USERS, COL_PERCENT ) )
    keys_to_sort = {
        key : tuple( int( p ) for p in key.split( VER_SEP ) )
        for key in data_key.keys()
    }
    for os_v in sorted( data_key.keys(), key = lambda k: keys_to_sort[ k ] ):
        val     = data_key[ os_v ]
        percent = val * 100 / total
        writer.writerow( ( os_v, f'{val}', f'{percent: 2.2f}' ) )

