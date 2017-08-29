import os, sys
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

# Force import GDB now so the rest of the files can just assume it exists.
try:
    import gdb
except ImportError:
    print('Could not load gdb. Make sure this script is run from within GDB.')
    sys.exit(1)

import command
from integrations import load_integration

command.load()
load_integration()

print('Loaded Comments!')
