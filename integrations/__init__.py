def load_integration():
    try:
        import pwndbg
        from .pwndbg_patch import load
        load()
    except:
        # print('Could not ')
        raise
