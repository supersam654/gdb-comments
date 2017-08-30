import os, sys
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

# Force import GDB now so the rest of the files can just assume it exists.
try:
    import gdb
except ImportError:
    print('Could not load gdb. Make sure this script is run from within GDB.')
    sys.exit(1)

from gdb_comments import command

command.load()

print('Loaded Comments!')
