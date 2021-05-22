"""
The absolute most basic and fundamental algorithms for sudoku: performing basic 
elimination and finding singles.
"""
from .base_class import algorithm
from ..stepper import StepUnitSetBuilder, StepUnit, PLACE
from ..model import Puzzle

__all__ = [
    'eliminate_possibilities',
    'find_naked_singles',
    'find_hidden_singles',
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
            if house.has_value_set(value):
                continue
            cells = house.get_cells_with_possible(value) #Note: Skips full cells
            if len(cells) == 1: #i.e. There is only one cell in house that can be value
                cells[0].value = value
                yield (StepUnit(*puzzle.index(cells[0]), (value,), PLACE),)
