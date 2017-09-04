# This file is responsible for displaying comments in PEDA.
import re

import gdb

from gdb_comments import commenter

def _get_comment(line):
    # return ''
    match = re.search('0x[a-f\d]+', line)
    if match is None:
        return ''
    address = int(match.group(), 16)
    comments = commenter.get_comments(gdb.current_progspace().filename)
    comment = comments.get_comment(address)
    if comment:
        return '; %s' % comment
    else:
        return ''

def _patch_disassemble_around(peda):
    # Monkey patch but leave the original one on the object to allow for unpatching.
    peda._original_disassemble_around = peda.disassemble_around
    def patched_disassemble_around(*args, **kwargs):
        code = peda._original_disassemble_around(*args, **kwargs)
        new_code = []
        lines = code.splitlines()
        max_line = max(len(s.strip()) for s in lines)
        for line in lines:
            if len(line.strip()) > 0:
                comment = _get_comment(line)
                print('line')
                print(line.rjust(max_line) + '|')
                line = line.ljust(80) + comment
            new_code.append(line)
        return '\n'.join(new_code)

    peda.disassemble_around = patched_disassemble_around

def _unpatch_if_needed(peda):
    if hasattr(peda, '_original_disassemble_around'):
        peda.disassemble_around = peda._original_disassemble_around

def load(peda):
    _unpatch_if_needed(peda)
    _patch_disassemble_around(peda)
