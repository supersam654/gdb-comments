# This file is responsible for displaying comments in pwndbg.
import re

import gdb
from pwndbg import color as C
from pwndbg.commands import nearpc

from gdb_comments import commenter

def _get_comment(line):
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

def _patch_nearpc():
    # Monkey patch but leave the original one on the
    nearpc._original_nearpc = nearpc.nearpc
    def patched_nearpc(*args, **kwargs):
        result = nearpc._original_nearpc(*args, **kwargs)
        new_result = []
        max_line = max(len(C.strip(s)) for s in result)
        for line in result:
            if len(line.strip()) > 0:
                comment = _get_comment(line)
                comment = C.enhance.comment(comment)
                line = C.ljust_colored(line, max_line) + comment
            new_result.append(line)
        return new_result

    nearpc.nearpc = patched_nearpc

def _unpatch_if_needed():
    if hasattr(nearpc, '_original_nearpc'):
        nearpc.nearpc = nearpc._original_nearpc

def load():
    _unpatch_if_needed()
    _patch_nearpc()

if __name__ == '__main__':
    load()
