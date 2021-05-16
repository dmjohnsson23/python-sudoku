from ..model import *

def empty_grid():
    return Puzzle([[None]*9]*9)

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
