"""
A set of very basic algorithms, just above the fundamentals, that begin to take multiples into consideration
"""

from ...algorithms.base_class import algorithm
from ...stepper import StepUnitSetBuilder
from ...model import Puzzle

__all__ = [
    'apply_pointers_forward',
    'apply_pointers_backward',
    'apply_pointer_possibilities_forward',
    'apply_pointer_possibilities_backward',
]


    
@algorithm(difficulty=1)
def apply_pointers_forward(puzzle: Puzzle):
    """
    This technique looks for set values in pointer cells, and applies the appropriate value in the indexed house
    """
    for pointer_house in puzzle.pointer_houses:
        for pointer_cell, indexed_house in pointer_house.iter_pointers():
            if pointer_cell.is_full:
                indexed_cell = indexed_house[pointer_cell.value - 1] # Convert 1-indexed to 0-indexed
                if indexed_cell.is_open:
                    indexed_cell.value = pointer_house.value
                    step_units = StepUnitSetBuilder(puzzle)
                    step_units.add_source_cells(pointer_cell, value=pointer_cell.value)
                    step_units.add_placed_value(indexed_cell, indexed_cell.value)
                    yield step_units.final()





@algorithm(difficulty=1)
def apply_pointers_backward(puzzle: Puzzle):
    """
    This technique looks through indexed houses for the pointer values, an sets the pointer cell to the corresponding value
    """
    for pointer_house in puzzle.pointer_houses:
        for pointer_cell, indexed_house in pointer_house.iter_pointers():
            if pointer_cell.is_open:
                for index, indexed_cell in enumerate(indexed_house):
                    if indexed_cell.value == pointer_house.value:
                        pointer_cell.value = index + 1 # Convert 0-index to 1-index
                        step_units = StepUnitSetBuilder(puzzle)
                        step_units.add_source_cells(indexed_cell, value=indexed_cell.value)
                        step_units.add_placed_value(pointer_cell, pointer_cell.value)
                        yield step_units.final()



@algorithm(difficulty=2)
def apply_pointer_possibilities_forward(puzzle: Puzzle):
    """
    For each pointer cell, limit the possible locations of the pointer house value to cells that could be indexed by the pointer cell
    """
    for pointer_house in puzzle.pointer_houses:
        for pointer_cell, indexed_house in pointer_house.iter_pointers():
            if pointer_cell.is_open:
                step_units = StepUnitSetBuilder(puzzle)
                step_units.add_source_cells(pointer_cell, values=pointer_cell.possible)
                for index, indexed_cell in enumerate(indexed_house):
                    if (index + 1) not in pointer_cell.possible and pointer_house.value in indexed_cell.possible:
                        indexed_cell.remove_possible(pointer_house.value)
                        step_units.add_eliminated_cells(indexed_cell, value=pointer_house.value)
                yield step_units.final()





@algorithm(difficulty=2)
def apply_pointer_possibilities_backward(puzzle: Puzzle):
    """
    For each indexed cell that cannot be the pointer value, eliminate their index from the appropriate pointer cell's values
    """
    for pointer_house in puzzle.pointer_houses:
        for pointer_cell, indexed_house in pointer_house.iter_pointers():
            if pointer_cell.is_open:
                step_units = StepUnitSetBuilder(puzzle)
                for index, indexed_cell in enumerate(indexed_house):
                    if pointer_house.value not in indexed_cell.possible and (index + 1) in pointer_cell.values:
                        pointer_cell.remove_possible(index + 1)
                        step_units.add_source_cells(indexed_cell)
                        step_units.add_eliminated_cells(pointer_cell, value=index + 1)
                yield step_units.final()


# TODO within each square, the three pointer cells in that square have exactly 1 value from each of these three sets: (1, 2, 3), 
# (4, 5, 6), (7, 8, 9). If it were not so, then there would be more than one of the same digit in a square. E.g. if row 1 column 1 
# was a 4, and row 2 column 1 was a 6, that would place a 1 in both row 1 column 4 and row 2 column 6; both of which are in the 
# same square.