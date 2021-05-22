"""
A set of very basic algorithms, just above the fundamentals, that begin to take multiples into consideration
"""

from ..utils import all_equal
from .base_class import algorithm
from ..stepper import StepUnitSetBuilder, StepUnit, PLACE, ELIMINATE, SOURCE
from ..model import Puzzle
import math

__all__ = [
    'find_locked_candidates_squares',
    'find_locked_candidates_rows_columns',
    'find_hidden_multiples',
    'find_naked_multiples',
]


    
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
                        removed_values = cell.possible.intersection(possible)
                        cell.remove_possible(*removed_values)
                        if removed_values:
                            step_units.add_eliminated_cells(cell, values=removed_values)
                yield step_units.final()

