import os, sys
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

import command
import commenter

command.load()

print('Loaded Comments!')
