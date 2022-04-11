import io
import re
import os
import sys


# gather input files
args = sys.argv[1:]
if not args:
    print('Error: no input files')
    exit(1)
if len(args) % 2 == 1:
    args.insert(0, 'en')
data = {}
for file_idx, (code, filename) in enumerate(zip(args[::2], args[1::2])):
    if not code:
        print('Error: empty code')
        exit(1)
    if code in data:
        print(f'Dupe code: {code} at {file_idx + 1}')
    if not filename:
        print('Error: empty filename')
        exit(1)
    exists = os.path.isfile(filename)
    # if not exists:
    #     print(f'Error: {code} - not found - {filename}')
    data[file_idx] = {
        'code'     : code,
        'filename' : filename,
        'exists'   : exists,
    }

# look shorter filenames - as simple as it can for now
all_filenames    = [v['filename'] for v in data.values()]
min_filename_len = min(len(fn) for fn in all_filenames)
last_sep         = 0
for ofs in range(min_filename_len - 1):
    if not all(fn[:ofs + 1] == all_filenames[0][:ofs + 1] for fn in all_filenames):
        max_common_len = last_sep
        break
    if all_filenames[0][ofs] == '/':
        last_sep       = ofs + 1
else:
    max_comoon_len = min_filename_len - 1
for data_cur in data.values():
    data_cur['filename_short'] = data_cur['filename'][max_common_len:]

def get_problems_base():
    return {
        'dupe_case'       : 0,
        'dupe_caseless'   : 0,
        'dupe_case_trans' : 0,
        'orphan'          : 0,
        'missing'         : 0,
    }

total_cntd = get_problems_base()

for file_idx in data.keys():

    print(f'\n\n{"-" * 32}\n')
    data_cur = data[file_idx]
    if not data_cur['exists']:
        print(f'{data_cur["code"]} - not found - {data_cur["filename_short"]}')
        continue
    print(f'{data_cur["code"]} - {data_cur["filename_short"]}')

    with io.open(data_cur['filename'], mode = 'r' ) as f:
        lines = f.readlines()

    base_data          = data         [0         ]
    base_data_case     = base_data.get('case'    )
    base_data_caseless = base_data.get('caseless')
    cntd               = data_cur['problems'] = get_problems_base()
    data_case          = {}
    data_caseless      = {}
    for idx, line in enumerate(lines):

        l = line.strip()
        if not l                : continue # empty
        if not l.startswith('"'): continue # comment or something wierd
        m = re.fullmatch(r'"(?P<key>[^"]+)"\s*=\s*"(?P<val>.*)"\s*;', l)
        if not m                : continue # bad one
        key = m.group('key')
        val = m.group('val')
        if not key              : continue # still bad

        if key in data_case: # dupe
            cntd['dupe_case'] += 1
            key_pad_case       = ' ' * max( 0, 32 - len( key ) )
            vals_match         = val == data_case[key]['val']
            if val != data_case[key]['val']:
                cntd['dupe_case_trans'] += 1
                org_val                  = data_case[key]["val"]
                if max(len(val), len(org_val)) < 32:
                    vals_report = f' translations not match - "{val}" != "{data_case[key]["val"]}"'
                else:
                    val_pad     = ' ' * (6 + 32 + 9)
                    vals_report = f' translations not match - \n{val_pad}"{val}"\n{val_pad}"{data_case[key]["val"]}"'
            else:
                vals_report = ''
            print(f'Dupe   : "{key}"{key_pad_case} line {idx + 1: 5} dupes          line {data_case[key]["idx"] + 1: 5}{vals_report}')
            continue
        data_case[key] = {
            'idx' : idx,
            'val' : val
        }

        key_caseless = key.casefold()
        if key_caseless in data_caseless:
            cntd['dupe_caseless'] += 1
            key_pad_caseless       = ' ' * max( 0, 32 - len( key_caseless ) )
            print(f'Dupe   : "{key_caseless}"{key_pad_caseless} line {idx + 1: 5} dupes caseless line {data_caseless[key_caseless]["idx"] + 1: 5} "{data_caseless[key_caseless]["key"]}"')
            continue
        data_caseless[key_caseless] = {
            'idx' : idx,
            'val' : val,
            'key' : key,
        }

        if file_idx <= 0: # base language
            continue
        if key not in base_data_case:
            cntd['orphan'] += 1
            key_pad_case    = ' ' * max( 0, 32 - len( key ) )
            print(f'Orphan : "{key}"{key_pad_case} line {idx + 1: 5} is missing at {base_data["code"]}')

    data_cur['case'    ] = data_case
    data_cur['caseless'] = data_caseless

    if file_idx > 0: # not base language
        for key_case in sorted( base_data_case.keys() - data_case.keys(), key = lambda k: base_data_case[k]['idx']):
            cntd['missing'] += 1
            key_pad_case     = ' ' * max(0, 32 - len(key_case))
            print(f'Missing: "{key_case}"{key_pad_case} line {base_data_case[key_case]["idx"] + 1: 5} is missing at {data_cur["code"]}')

    for key in cntd.keys():
        total_cntd[key] += cntd[key]

base_cntd = base_data['problems']

print(f'\n\n{"-" * 32}\n')
if total_cntd['missing']:
    print(f'Missing: {total_cntd["missing"   ]: 5} in total')
if total_cntd['missing']:
    print(f'Orphan : {total_cntd["orphan"    ]: 5} in total')
if base_cntd['dupe_case']:
    if base_cntd['dupe_case_trans']:
        trans_report = f' among them {base_cntd["dupe_case_trans"]: 5} with different translations'
    else:
        trans_report = ''
    print(f'Dupe   : {base_cntd ["dupe_case"    ]: 5} at {base_data["code"]}{trans_report}')
if base_cntd['dupe_caseless']:
    print(f'Dupe   : {base_cntd ["dupe_caseless"]: 5} caseless at {base_data["code"]}')
