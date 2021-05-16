class SudokuError(Exception):
    def __init__(self, error_message, puzzle, cell=None, stepper=None):
        msg=[error_message, 
             "Puzzle:",
             str(puzzle)]
        
        self.cell = cell
        if cell is not None:
            msg.extend((
                "Problem Cell Details:",
                "\tCoordinates (row, col): {}".format(puzzle.index(cell)),
                "\tValue: {}".format(cell.value),
                "\tPossible Values: {}".format(cell.possible)
                ))
        
        self.stepper = stepper
        if stepper is not None:
            msg.append("Additional details about the solve process can be found by examining the `stepper` attribute of this exception")
        Exception.__init__(self, "\n".join(msg))