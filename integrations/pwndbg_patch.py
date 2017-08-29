# This file is responsible for displaying comments in pwndbg.
import re

import gdb
from pwndbg import color as C
from pwndbg.commands import nearpc

import commenter

def get_comment(line):
    address = int(re.search('0x\d+', line).group(), 16)
    comments = commenter.get_comments(gdb.current_progspace().filename)
    comment = comments.get_comment(address)
    if comment:
        return '; %s' % comment
    else:
        return ''

def patch_nearpc():
    _nearpc = nearpc.nearpc
    def patched_nearpc(*args, **kwargs):
        result = _nearpc(*args, **kwargs)
        new_result = []
        max_line = max(len(C.strip(s)) for s in result)
        for line in result:
            if len(line.strip()) > 0:
                comment = get_comment(line)
                line = C.ljust_colored(line, max_line) + comment
            new_result.append(line)
        return new_result

    nearpc.nearpc = patched_nearpc

def load():
    patch_nearpc()
