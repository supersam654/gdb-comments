import gdb
import commenter

class Command(gdb.Command):
  """Defines the `comment` command in GDB."""

  def __init__ (self):
    super(Command, self).__init__('comment', gdb.COMMAND_USER)

  def invoke (self, arg, from_tty):
      address, comment = arg.split(' ', 1)
      address = int(gdb.parse_and_eval(address))
      comments = commenter.get_comments(gdb.current_progspace().filename)
      comments.add_comment(address, comment)

def load():
    Command()
