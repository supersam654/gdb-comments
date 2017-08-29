import pwndbg

def info(s):
    print(s)

def error(s):
    # It's good enough for printing exceptions and it's good enough for me.
    print(pwndbg.color.red(s))

# pwndbg already handles a bunch of architectures. No reason to reinvent the wheel.
def get_pc():
    return pwndbg.regs.pc
