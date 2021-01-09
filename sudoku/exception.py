class SudokuError(Exception):
    def __init__(self, errorMessage, puzzle, cell=None):
        msg=[errorMessage, 
             "Puzzle:",
             str(puzzle)]
        
        if cell is not None:
            msg.extend((
                "Problem Cell Details:",
                "\tCoordinates (row, col): {}".format(puzzle.index(cell)),
                "\tValue: {}".format(cell.value),
                "\tPossible Values: {}".format(cell.possible)
                ))
        Exception.__init__(self, "\n".join(msg))