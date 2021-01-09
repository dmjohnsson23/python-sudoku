
def all_equal(*args, key=None):
    """
    Tests if all given values are equal, applying key if given.
    If no values are given, returns None
    """
    if len(args) == 0:
        return None
    
    val=args[0] if key is None else key(args[0])
    for x in args:
        if val != (x if key is None else key(x)):
            return False
    return True


