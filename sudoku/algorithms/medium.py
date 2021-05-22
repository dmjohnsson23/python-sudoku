"""
The entry level of more advanced algorithms
"""

from ..utils import  candidate_coordinate_plot
from .base_class import algorithm
from ..stepper import StepUnitSetBuilder
from ..model import Puzzle

__all__ = [
    'find_x_wing',
    # 'find_y_wing',
    # 'find_swordfish',
]



@algorithm(difficulty=5)
def find_x_wing(puzzle: Puzzle):
    """
    An x-wing is when there are 4 cells which are the corners of a given rectangular area of the grid, 
    such that every one of the four cell shares a row with exactly one other cell, and a column with 
    exactly one other cell. In these cells, all have the same candidate value. If either in both rows
    occupied by the cells, or in both columns occupied by the cells, those two cells are the only two 
    cells which can contain that value, this is an x-wing.

    If there is an x-wing, that value can be removed as a possibility from all other cells in the rows
    and columns occupied by the x-wing. For example image x represented all the open cells which can
    possibly contain a given value in the puzzle:

    ╔═══╤═══╤═══╦═══╤═══╤═══╦═══╤═══╤═══╗
    ║   │   │   ║   │   │   ║   │   │   ║
    ╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
    ║   │   │ x ║   │   │   ║ x │   │   ║
    ╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
    ║   │   │ x ║   │   │   ║   │   │ x ║
    ╠═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣
    ║   │   │   ║   │ x │   ║   │   │   ║
    ╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
    ║   │   │ x ║   │   │   ║ x │   │   ║
    ╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
    ║   │ x │   ║   │ x │   ║ x │   │   ║
    ╠═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣
    ║   │   │   ║   │   │   ║ x │   │   ║
    ╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
    ║   │   │   ║   │   │   ║   │   │   ║
    ╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
    ║ x │ x │ x ║   │   │   ║   │ x │ x ║
    ╚═══╧═══╧═══╩═══╧═══╧═══╩═══╧═══╧═══╝

    The cells in row 2 columns 3 and 7, and row 5 columns 3 and 7, form an x-wing, as they are the only
    two possibilities in their rows. Thus, x can be removed from all other cells in their columns as well,
    as follows:

    ╔═══╤═══╤═══╦═══╤═══╤═══╦═══╤═══╤═══╗
    ║   │   │   ║   │   │   ║   │   │   ║
    ╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
    ║   │   │ x ║   │   │   ║ x │   │   ║
    ╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
    ║   │   │   ║   │   │   ║   │   │ x ║
    ╠═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣
    ║   │   │   ║   │ x │   ║   │   │   ║
    ╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
    ║   │   │ x ║   │   │   ║ x │   │   ║
    ╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
    ║   │ x │   ║   │ x │   ║   │   │   ║
    ╠═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣
    ║   │   │   ║   │   │   ║   │   │   ║
    ╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
    ║   │   │   ║   │   │   ║   │   │   ║
    ╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
    ║ x │ x │   ║   │   │   ║   │ x │ x ║
    ╚═══╧═══╧═══╩═══╧═══╧═══╩═══╧═══╧═══╝
    """
    # TODO this algorithm could probably be tweaked to also find swordfishes, though it might complicate the logic
    for value in range(1, 10):
        row_plot = candidate_coordinate_plot(puzzle.rows, value)
        col_plot = candidate_coordinate_plot(puzzle.columns, value)
        # For the purpose of this code, we define the "main axis" as the axis that the houses travel along, 
        # e.g the vertical axis for rows, and the horizontal axis for columns, and the "secondary axis" as
        # the axis running along the house itself, e.g. the horizontal axis for rows, and the vertical for
        # columns.
        for plot in (row_plot, col_plot):
            # This is a list of indices for houses (along the primary axis) which have only two cells which can contain the value
            len_2_indices = [house_index for house_index, cell_indices in enumerate(plot) if len(cell_indices) == 2]
            # This is a set of frozensets which each contain cell indices (on the secondary axis) which can contain the value
            seen_index_sets = set()
            for primary_loop_main_axis_index in len_2_indices: # primary x-wing detection loop
                if plot[primary_loop_main_axis_index] in seen_index_sets:
                    # We've seen this exact same set of 2 cell indices before. This means we've found an x-wing!
                    # Now we can eliminate values from other cells in the secondary axis
                    step_units = StepUnitSetBuilder(puzzle)
                    cross_axis_houses = puzzle.columns if plot is row_plot else puzzle.rows
                    for cross_axis_cell_index in plot[primary_loop_main_axis_index]:
                        cross_axis_house = cross_axis_houses[cross_axis_cell_index]
                        for main_axis_cell_index, main_axis_cell in enumerate(cross_axis_house):
                            # We loop through cells along the secondary axis, eliminating the value from all but the source cells
                            if plot[primary_loop_main_axis_index] == plot[main_axis_cell_index]:
                                # This is one of the source cells, don't modify it, only record it
                                step_units.add_source_cells(main_axis_cell, value=value)
                            elif main_axis_cell.has_possible(value):
                                # This is not a source cell and needs to be modified
                                main_axis_cell.remove_possible(value)
                                step_units.add_eliminated_cells(main_axis_cell, value=value)
                    yield step_units.final()
                    break

                else:
                    # Potential x-wing, we're not sure yet, save it for the next loop
                    seen_index_sets.add(frozenset(plot[primary_loop_main_axis_index]))



def find_y_wing(puzzle):
    """
    A y-wing takes three cells, a "stem" and two "branches". Each branch shares either a row, column, or square 
    with the stem. The branch is limited to exactly two possible values: a and b. The first branch cell is also 
    limited to two remaining values: b and c. The second branch cell is limited to a and c.

    The y-wing tells us that the value c must be in one of the two branch cells, regardless of the value of the stem 
    cell. Thus, any cell which shares either a row, column, or square with *both* branch cells cannot be a c.

    For example:

    ╔═══╤════════╤═══╦═══╤════════╤═══╦
    ║   │        │   ║   │        │   ║
    ╟───┼────────┼───╫───┼────────┼───╫
    ║   │ [a, b] │   ║   │ [b, c] │   ║
    ╟───┼────────┼───╫───┼────────┼───╫
    ║   │        │   ║   │        │   ║
    ╠═══╪════════╪═══╬═══╪════════╪═══╬
    ║   │        │   ║   │        │   ║
    ╟───┼────────┼───╫───┼────────┼───╫
    ║   │ [a, c] │   ║   │ [c, d] │   ║
    ╟───┼────────┼───╫───┼────────┼───╫
    ║   │        │   ║   │        │   ║
    ╠═══╪════════╪═══╬═══╪════════╪═══╬

    Becomes:

    ╔═══╤════════╤═══╦═══╤════════╤═══╦
    ║   │        │   ║   │        │   ║
    ╟───┼────────┼───╫───┼────────┼───╫
    ║   │ [a, b] │   ║   │ [b, c] │   ║
    ╟───┼────────┼───╫───┼────────┼───╫
    ║   │        │   ║   │        │   ║
    ╠═══╪════════╪═══╬═══╪════════╪═══╬
    ║   │        │   ║   │        │   ║
    ╟───┼────────┼───╫───┼────────┼───╫
    ║   │ [a, c] │   ║   │    d   │   ║
    ╟───┼────────┼───╫───┼────────┼───╫
    ║   │        │   ║   │        │   ║
    ╠═══╪════════╪═══╬═══╪════════╪═══╬
    """
    return False # TODO