from ..utils import all_equal, candidate_coordinate_plot
from .base_class import algorithm
from ..stepper import StepUnitSetBuilder, StepUnit, PLACE, ELIMINATE, SOURCE
from ..model import Puzzle
import math

__all__ = [
    'eliminate_possibilities',
    'find_naked_singles',
    'find_hidden_singles',
    'find_locked_candidates_squares',
    'find_locked_candidates_rows_columns',
    'find_hidden_multiples',
    'find_naked_multiples',
    'find_x_wing',
]

@algorithm(difficulty=0, multistep=True)
def eliminate_possibilities(puzzle: Puzzle):
    """
    Eliminates any possibilities from cells in which are not actually
    possible given the rules of sudoku. 

    This performs basic elimination based on filled cells in the house,
    without applying more complex logic
    """
    for filled_cell in puzzle.iter_cells(skip_open_cells=True):
        step_units = StepUnitSetBuilder(puzzle)
        step_units.add_source_cells(filled_cell, value=filled_cell.value)
        for empty_cell in puzzle.iter_cells(central_call=filled_cell, skip_full_cells=True):
            if empty_cell.has_possible(filled_cell.value):
                empty_cell.remove_possible(filled_cell.value)
                step_units.add_eliminated_cells(empty_cell, value=filled_cell.value)
        yield step_units.final()

                    
    
@algorithm(difficulty=0, multistep=True)
def find_naked_singles(puzzle: Puzzle):
    """
    If there is only one remaining possibility in any cells, sets those 
    cells to their only possible value
    """
    
    for cell in puzzle.iter_cells(skip_full_cells=True):
        if len(cell.possible) == 1:
            cell.value = cell.possible.pop()
            yield (StepUnit(*puzzle.index(cell), (cell.value,), PLACE),)

    
@algorithm(difficulty=0, multistep=True)
def find_hidden_singles(puzzle: Puzzle):
    """
    Checks to see if there are any cells which are the only possible 
    location in their row, column, or square which can contain a certain 
    value. If so, sets those cells to that exclusive value.
    """
    for house in puzzle.iter_houses():
        for value in range(1, 10):
            cells = house.get_cells_with_possible(value) #Note: Skips full cells
            if len(cells) == 1: #i.e. There is only one cell in house that can be value
                cells[0].value = value
                yield (StepUnit(*puzzle.index(cells[0]), (value,), PLACE),)

    
@algorithm(difficulty=1)
def find_locked_candidates_squares(puzzle: Puzzle):
    """
    This technique is sometimes called "pointing pairs" or "pointing triples".

    Searches all squares to see if all the possible cells for a value are in a 
    line. If so, removes that value from all other cells in that row/column. 

    For example,
    ```
    ╔═══╤═══╤═══╦═══╤═══╤═══╦
    ║   │ x │ x ║ x │ x │ x ║
    ╟───┼───┼───╫───┼───┼───╫
    ║   │   │   ║ x │ x │ x ║
    ╟───┼───┼───╫───┼───┼───╫
    ║   │   │   ║   │   │   ║
    ╠═══╪═══╪═══╬═══╪═══╪═══╬
    ```
    becomes
    ```
    ╔═══╤═══╤═══╦═══╤═══╤═══╦
    ║   │ x │ x ║   │   │   ║
    ╟───┼───┼───╫───┼───┼───╫
    ║   │   │   ║ x │ x │ x ║
    ╟───┼───┼───╫───┼───┼───╫
    ║   │   │   ║   │   │   ║
    ╠═══╪═══╪═══╬═══╪═══╪═══╬
    ```
    where x represents a possible location for a given value.
    """
    for square in puzzle.squares:
        for possible in range(1, 10):
            cells = square.get_cells_with_possible(possible)
            if all_equal(*cells, key=lambda cell: square.index(cell)[0]):
                #All in same row
                house = cells[0].row      
            elif all_equal(*cells, key=lambda cell: square.index(cell)[1]):
                #All in same column
                house = cells[0].column
            else:
                continue
            # All the cells are aligned; see if they eliminate anything
            step_units = StepUnitSetBuilder(puzzle)
            step_units.add_source_cells(*cells, value=possible)
            for cell in house:
                if cell not in square.cells and cell.is_open and cell.has_possible(possible):
                    cell.remove_possible(possible)
                    step_units.add_eliminated_cells(cell, value=possible)
            yield step_units.final()

                


@algorithm(difficulty=1)
def find_locked_candidates_rows_columns(puzzle: Puzzle):
    """
    This technique is also known as "box/line reduction"

    If all the possibilities for a value in any given row or column
    are also all in the same square, no other cells in that square
    can be the given value.

    For example,
    ```
    ╔═══╤═══╤═══╦═══╤═══╤═══╦═══╤═══╤═══╗
    ║   │   │   ║ x │   │ x ║   │   │   ║
    ╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
    ║   │   │   ║   │ x │ x ║   │ x │ x ║
    ╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
    ║   │   │   ║   │   │   ║   │   │   ║
    ╠═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣
    ```
    becomes
    ```
    ╔═══╤═══╤═══╦═══╤═══╤═══╦═══╤═══╤═══╗
    ║   │   │   ║ x │   │ x ║   │   │   ║
    ╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
    ║   │   │   ║   │   │   ║   │ x │ x ║
    ╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
    ║   │   │   ║   │   │   ║   │   │   ║
    ╠═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣
    ```
    where x represents a possible location for a given value.
    """
    for house in (*puzzle.rows, *puzzle.columns):
        for possible in range(1, 10):
            cells = house.get_cells_with_possible(possible)
            if len(cells) < 2: continue # Hidden single, leave that for the appropriate algorithm
            squares_seen = set()
            for cell in cells:
                index = house.index(cell)
                squares_seen.add(math.floor(index/3))
            if len(squares_seen) == 1:
                # All values are in the same square
                step_units = StepUnitSetBuilder(puzzle)
                step_units.add_source_cells(*cells, value=possible)
                for cell in cells[0].square:
                    if cell not in cells and cell.is_open and cell.has_possible(possible):
                        cell.remove_possible(possible)
                        step_units.add_eliminated_cells(cell, value=possible)
                yield step_units.final()


@algorithm(difficulty=2)
def find_hidden_multiples(puzzle: Puzzle):
    """
    If in any house there are x different values which can only 
    go in any of  x different cells, removes all other values 
    from those cells. 
    
    For example,
    ```
    ╔════════════════╤════════════════╤════════════════╦
    ║ [a, b, c, ...] │ [a, b, c, ...] │      [...]     ║
    ╟────────────────┼────────────────┼────────────────╫
    ║      [...]     │      [...]     │      [...]     ║
    ╟────────────────┼────────────────┼────────────────╫
    ║      [...]     │      [...]     │ [a, b, c, ...] ║
    ╠════════════════╪════════════════╪════════════════╬
    ```
    becomes
    ```
    ╔═══════════╤═══════════╤═══════════╦
    ║ [a, b, c] │ [a, b, c] │   [...]   ║
    ╟───────────┼───────────┼───────────╫
    ║   [...]   │   [...]   │   [...]   ║
    ╟───────────┼───────────┼───────────╫
    ║   [...]   │   [...]   │ [a, b, c] ║
    ╠═══════════╪═══════════╪═══════════╬
    ```
    where a, b, and c are possible values and '...' represents any number 
    of values besides those three.
    """
    for house in puzzle.iter_houses():
        # Here we build a mapping of cell indices of all cells which contain a set of possibility values to
        # the possibility values that all those cells contain. E.g. and entry `(1, 4, 6): {3, 5, 7}` indicates
        # That the cells at indices 1, 4, and 6 all have the possibility of being a 3, 5, or 7, and no other
        # cells have the possibility of being any of those values
        mapping={}
        
        for value in range(1, 10):
            cells = house.get_cells_with_possible(value)
            indices = tuple(house.index(cell) for cell in cells)
            if indices in mapping:
                mapping[indices].add(value)
            else:
                mapping[indices] = {value,}
        
        for indices, values in mapping.items():
            if len(indices) == len(values):
                #Eligible
                cells = [house[index] for index in indices]
                step_units = StepUnitSetBuilder(puzzle)
                step_units.add_source_cells(*cells, values=values)
                for cell in cells:
                    if cell.possible != values:
                        removed_values = cell.possible.difference(values)
                        cell.limit_possible(*values)
                        step_units.add_eliminated_cells(cell, values=removed_values)
                yield step_units.final()


@algorithm(difficulty=2)
def find_naked_multiples(puzzle: Puzzle):
    """
    If there are x cells in a house which all contain the same x 
    possibilities and *only* those x possibilities, then those 
    possibilities can be removed from all other cells in the house. 
    
    For example,
    ```
    ╔═════════════╤══════════╤═════════════╦
    ║    [a, b]   │  [a, b]  │    [...]    ║
    ╟─────────────┼──────────┼─────────────╫
    ║   [a, ...]  │ [a, ...] │   [b, ...]  ║
    ╟─────────────┼──────────┼─────────────╫
    ║ [a, b, ...] │ [b, ...] │ [a, b, ...] ║
    ╠═════════════╪══════════╪═════════════╬
    ```
    becomes,
    ```
    ╔════════╤════════╤═══════╦
    ║ [a, b] │ [a, b] │ [...] ║
    ╟────────┼────────────────╫
    ║  [...] │  [...] │ [...] ║
    ╟────────┼────────┼───────╫
    ║  [...] │  [...] │ [...] ║
    ╠════════╪════════╪═══════╬
    ```
    where a and b are possible values and '...' represents 
    any values besides those two.
    """
    
    for house in puzzle.iter_houses():
        mapping = {}
        for cell in house:
            p = tuple(cell.possible)
            if p in mapping:
                mapping[p].append(cell)
            else:
                mapping[p] = [cell]
        
        for possible, cells in mapping.items():
            if len(possible) == len(cells):
                #Eligible
                step_units = StepUnitSetBuilder(puzzle)
                step_units.add_source_cells(*cells, values=possible)
                for cell in house:
                    if cell not in cells:
                        removed_values = cell.possible.difference(possible)
                        cell.remove_possible(*possible)
                        if removed_values:
                            step_units.add_eliminated_cells(cell, values=removed_values)
                yield step_units.final()

@algorithm(difficulty=5)
def find_x_wing(puzzle):
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
            for primary_loop_main_axis_index in len_2_indices:
                if plot[primary_loop_main_axis_index] in seen_index_sets:
                    # We've seen this exact same set of 2 cell indices before. This means we've found an x-wing!
                    # Now we can eliminate values from other cells in the secondary axis
                    step_units = StepUnitSetBuilder(puzzle)
                    cross_axis_houses = puzzle.columns if plot is row_plot else puzzle.rows
                    for cross_axis_cell_index in plot[primary_loop_main_axis_index]:
                        cross_axis_house = cross_axis_houses[cross_axis_cell_index]
                        for main_axis_cell_index, main_axis_cell in enumerate(cross_axis_house):
                            if plot[primary_loop_main_axis_index] == plot[main_axis_cell_index]:
                                step_units.add_source_cells(main_axis_cell, value=value)
                            elif main_axis_cell.has_possible(value):
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