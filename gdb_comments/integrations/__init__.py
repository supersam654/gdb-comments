utils = None

try:
    import pwndbg
    from gdb_comments.integrations.pwndbg_patch import load
    load()
    from gdb_comments.integrations import pwndbg_utils
    utils = pwndbg_utils
except:
    # TODO: Support more environments and don't raise.
    raise
    
