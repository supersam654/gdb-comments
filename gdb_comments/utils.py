import re
from collections import Counter

import gdb

def get_pc():
    pc_line = gdb.execute('info registers pc', to_string=True)
    pc_addr = pc_line.split('\t')[0].replace(' ', '').replace('pc', '')
    return int(pc_addr, 16)

def get_mappings():
    mappings = gdb.execute('info proc mappings', to_string=True)
    # The first 4 rows are a process ID, the string "Mapped address spaces:", a
    # blank line, and then column headers for the actual mappings.
    regions = {}
    objfiles = Counter()
    for mapping in mappings.splitlines()[4:]:
        mapping = mapping.strip()
        # Combine runs of spaces into single spaces
        values = re.sub(' +', ' ', mapping).split(' ')
        if len(values) == 5:
            start_address, end_address, size, offset, objfile = values
        else:
            start_address, end_address, _, _ = values
            objfile = ''
        start_address, end_address = int(start_address, 16), int(end_address, 16)

        regions[range(start_address, end_address)] = (objfile, objfiles[objfile])
        # Increment the counter on the objfile.
        objfiles.update((objfile,))
    return regions

def get_core_dump_mappings():
    mappings = gdb.execute('maintenance info sections', to_string=True)
    ranges = set()
    for mapping in mappings:
        result = re.search('0x[a-f\d]+->0x[\da-f]+', mapping)
        if result is None:
            continue
        start_address, end_address = result.group().split('->')
        ranges.add(range(start_address, end_address))
    return ranges
