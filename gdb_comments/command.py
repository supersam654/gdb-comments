import gdb
from gdb_comments import commenter, utils, integrations

class Command(gdb.Command):
    """Defines the `comment` command in GDB."""

    def __init__ (self):
        super(Command, self).__init__('comment', gdb.COMMAND_USER)

    def invoke (self, arg, from_tty):
        arg = arg.strip()
        # Comments don't need to be quoted into a single argument.
        parts = arg.split(' ')
        # Prevent index out of bounds exceptions.
        parts.append('')
        # Most people are just going to comment the current instruction.
        # Just pass -a <address> <comment> to put a comment on a particular address.
        clear = False
        if '-c' in parts:
              clear = True
              parts.remove('-c')
        if '--clear' in parts:
            clear = True
            parts.remove('--clear')

        if parts[0] in ('-a', '--at'):
            address = int(gdb.parse_and_eval(parts[1]))
            comment = ' '.join(parts[2:])
        else:
            address = utils.get_pc()
            comment = ' '.join(parts)

        if clear:
            if len(comment) > 0:
                integrations.error("Cannot clear a comment and add a new one at the same time.")
                integrations.error("To overwrite a comment, just add a new comment in the same spot.")
                return
            comment = ''
        try:
            current_file = utils.get_current_filename()
        except RuntimeError:
            # Don't print the exception message because I'm far too lazy to make
            # exception handling Python 2 and 3 compatible at the same time.
            integrations.error("Cannot add a comment to a non-existant file")
        comments = commenter.get_comments(current_file)
        comments.add_comment(address, comment)

def load():
    Command()
