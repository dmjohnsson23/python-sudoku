
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


def candidate_coordinate_plot(rows_or_columns, value):
    """
    Builds a list of sets, one set for each house, of the indexes of cells 
    which have a possibility for a given value
    """
    plot = []
    for house in rows_or_columns:
        plot.append(set())
        for index, cell in enumerate(house):
            if cell.has_possible(value):
                plot[-1].add(index)
    return plot

