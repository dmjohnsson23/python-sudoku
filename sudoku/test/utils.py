from ..solver import Solver
from ..variant_context import ClassicContext
import traceback

def empty_grid():
    return ClassicContext().Puzzle([[None]*9]*9)

def grid_with_possible_only_at_coordinates(*coordinates, starting_puzzle=None, candidate_value=1):
    """
    Generate a puzzle which the only candidates for a given value are at the given coordinates
    """
    puzzle = starting_puzzle or empty_grid()
    coordinates = set(coordinates)
    for row in range(9):
        for col in range(9):
            if (row, col) not in coordinates:
                puzzle[row, col].remove_possible(candidate_value)
    return puzzle

def solve_puzzle(test_case, context, puzzle, *solver_args, **solver_kwargs):
    solver = Solver(context)
    orig_puzzle = puzzle.copy()
    try:
        solution = solver.solve(puzzle, *solver_args, **solver_kwargs)
        success = solution.success
        exception_message = ''
    except Exception as e:
        success = False
        exception_message = '\n\nException Raised:\n'+traceback.format_exc()
    if not success:
        test_case.fail("Failed to solve puzzle.\n\nInitial state:\n{}\n\nFinal State:\n{}{}".format(
            orig_puzzle,
            puzzle.debug_string,
            exception_message
        ))