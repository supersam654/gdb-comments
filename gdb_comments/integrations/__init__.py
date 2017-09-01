from collections import namedtuple

import gdb

def _load_pwndbg():
    try:
        import pwndbg
    except:
        return None

    from gdb_comments.integrations.pwndbg_patch import load
    load()

    from gdb_comments.integrations import pwndbg_utils
    return pwndbg_utils

def _load_peda():
    # PEDA was never designed to be imported. Instead of writing an overt rant
    # here, I will simply list a series of facts and let the astute reader draw
    # their own conclusions (and my appologies to the keen gramarian for my use
    # of the gender-neutral, singular "they").
    #
    # Typically in Python, when you want to import something, you type
    # `import something` at the top of your file and it Just Works. Sadly, peda
    # cannot be imported this way. The main file (that contains the majority of
    # code in peda) is a 6,000+ line script that contains at least two classes
    # and 50 lines of initialization code that is not guarded inside of a
    # standard `if __name__ == '__main__'` construct.
    #
    # In the event that you could convince Python to load this file, peda would
    # generate a second instance of the PEDA class which would be in direct
    # violation of the comment above the instance stating
    #
    #    # global instances of PEDA() and PEDACmd()
    #    peda = PEDA()
    #
    # Typically, a project implicitly demonstrates how to import itself via its
    # test suite. However, peda has no tests and therefore cannot serve as a
    # reference on importing itself.
    #
    # With that said, I know that the peda object exists in memory. I can (and
    # do) `import gdb` and potentially the global namespace accessible through
    # the GDB interpreter is available through that import although I could
    # never find it. I wouldn't be surprised if a knowledgable someone came
    # across this comment and just so happened to know how to access the
    # interpreter environment through `import gdb`. However, I was unable to
    # find it.
    #
    # And that finally brings us to the third and current solution. Given that
    # the peda object is sitting somewhere in memory and this code is getting
    # executed under the same Python process, this code should be able to find
    # the peda object. A quick search on SO yielded a simple, yet horrific,
    # answer: just get a list of every object known to the garbage collector.
    # From there, find one with the correct class name (although I need to
    # compare strings because I don't actually have a reference to the PEDA
    # class).
    #
    # If you have had the patience to read this rather lengthy wall of text, my
    # hope is that you will understand why the next few lines of code exist and
    # why I am not a terrible person for writing them.
    import gc

    peda = None
    for obj in gc.get_objects():
        if str(obj.__class__) == "<class '__main__.PEDA'>":
            peda = obj
            break
    if peda is None:
        return None

    from gdb_comments.integrations.peda_patch import load
    load(peda)

    from gdb_comments.integrations import peda_utils
    return peda_utils

# This is lumped into integrations because it used to be integration-specific.
def _get_pc():
    pc_line = gdb.execute('info registers pc', to_string=True)
    pc_addr = pc_line.split('\t')[0].replace(' ', '').replace('pc', '')
    return int(pc_addr, 16)

def _make_utils():
    _utils = None
    if _utils is None:
        _utils = _load_pwndbg()

    # Loading PEDA is very inefficient so make sure it's the last thing we try.
    if _utils is None:
        _utils = _load_peda()

    if _utils is None:
        raise EnvironmentError('Could not find a supported environment to load comments.')
    Utils = namedtuple('GdbCommentsUtils', 'info error get_pc')
    utils = Utils(info=_utils.info, error=_utils.error, get_pc=_get_pc)
    return utils


utils = _make_utils()
