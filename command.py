import sys

import commenter

try:
    import gdb
except ImportError:
    print('Could not load gdb. Make sure this script is run from within GDB.')
    sys.exit(1)

class Command(gdb.Command):
  """Greet the whole world."""

  def __init__ (self):
    super(Command, self).__init__('comment', gdb.COMMAND_USER)


  def _load_existing_comments(self):
      pass

  def invoke (self, arg, from_tty):
      address, comment = arg.split(' ')
      address = int(gdb.parse_and_eval(address))
      comments = commenter.get_comments(gdb.current_progspace().filename)
      comments.add_comment(address, comment)


from pwndbg import color as C
from pwndbg.commands import nearpc
import re

def get_comment(line):
    address = int(re.search('0x\d+', line).group(), 16)
    comments = commenter.get_comments(gdb.current_progspace().filename)
    comment = comments.get_comment(address)
    print('Comment!')
    print(comment)
    if comment:
        return '; %s' % comment
    else:
        return ''

def patch_pwndbg():
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
    Command()

    # Monkey patching to the rescue!
    patch_pwndbg()
