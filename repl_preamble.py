"""
This is convenience code used for manual testing and debugging of the library via the python 
interactive shell. Import this with a wildcard import and test away.
"""
from sudoku import *
from sudoku.test.puzzles import puzzles, solutions
from sudoku.test.models import TestPuzzle
from sudoku.test.utils import empty_grid, grid_with_possible_only_at_coordinates

def named_puzzle(name):
    if name in solutions:
        return TestPuzzle(puzzles[name], solutions[name])
    else:
        return Puzzle(puzzles[name])

def live_debug_solve(puzzle, context=None):
    """
    Run the solver algorithms, printing out each step as it is completed. Useful 
    to debug tricky situations such as if the solver gets stuck in an infinate loop
    """
    if isinstance(puzzle, str):
        puzzle = named_puzzle(puzzle)
    elif not isinstance(puzzle, Puzzle):
        puzzle = Puzzle(puzzle)
    
    if context is None:
        context = ClassicContext()
    
    solver = Solver(context)
    stepper = Stepper(puzzle)

    current_index = 0
    for _ in solver.step_through_algorithms(puzzle, stepper):
        for i in range(current_index, len(stepper._steps)):
            algorithm, step_units = stepper._steps[i]
            print(f"\nfound {algorithm}:")
            for unit in step_units:
                print(f"\t{unit.mode} values {unit.values} from ({unit.row}, {unit.column})")
            current_index = i