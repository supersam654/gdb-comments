import pwndbg

def info(s):
    print(s)

def error(s):
    # It's good enough for printing exceptions and it's good enough for me.
    print(pwndbg.color.red(s))
