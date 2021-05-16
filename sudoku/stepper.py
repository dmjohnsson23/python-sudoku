from dataclasses import dataclass
from .model import Puzzle
from typing import Tuple

ELIMINATE = 'eliminate' # Eliminated values from a cell
PLACE = 'place' # Place the final value in a cell
LIMIT = 'limit' # Limit a cell to any of a given few values
SOURCE = 'source' # This cell was not modified, but was the source that caused a modification


@dataclass(frozen=True)
class StepUnit:
    """
    A representation to highlight one unit of change in a step. 
    This could be:

    * An elimination of a value from a cell (set mode to ELIMINATE)
    * The placing of a value in a cell (set mode to PLACE)
    * The designation of a cell as a source cell for an algorithm (set mode to SOURCE or whatever other custom designation is needed for the algorithm)
    """
    row: int
    column: int
    values: Tuple[int]
    mode: str


@dataclass(frozen=True)
class Step:
    """
    A representation of one step in a sudoku solve
    """
    algorithm: str
    step_units: Tuple[StepUnit]
    puzzle_before: Puzzle
    puzzle_after: Puzzle



class Stepper:
    """
    A class to track changes to the puzzle
    """
    def __init__(self, puzzle):
        self._starting_puzzle = puzzle.copy()
        self._steps = [('start', ())]
    
    def record_step(self, algorithm_name, step_units):
        self._steps.append((algorithm_name, step_units))
    
    def get_puzzle_before_step(self, step_index):
        """
        Get the state of the puzzle before a given step

        Note that this is not the most efficient way to get the puzzle state at any given time; 
        it has to re-calculate all deltas from the beginning. If you are trying to iterate 
        through the puzzle at each step, you should iterate over the stepper object rather 
        than calling this method.
        """
        return self.get_puzzle_after_step(step_index - 1)

    def get_puzzle_after_step(self, step_index):
        """
        Get the state of the puzzle after a given step

        Note that this is not the most efficient way to get the puzzle state at any given time; 
        it has to re-calculate all deltas from the beginning. If you are trying to iterate 
        through the puzzle at each step, you should iterate over the stepper object rather 
        than calling this method.
        """
        if step_index >= len(self._steps):
            raise IndexError("Step index not yet recorded")
        puzzle = self._starting_puzzle.copy()
        for _, step_units in self._steps[:step_index+1]: 
            _apply_steps(puzzle, step_units)
        return puzzle
    

    def __iter__(self):
        puzzle_before = self._starting_puzzle.copy()
        for algorithm, step_units in self._steps:
            puzzle_after = puzzle_before.copy()
            _apply_steps(puzzle_after, step_units)
            yield Step(algorithm, step_units, puzzle_before, puzzle_after)
            puzzle_before = puzzle_after

    



    


def _apply_steps(puzzle, step_units):
    for unit in step_units:
        if unit.mode == PLACE:
            puzzle[unit.row, unit.column].value = unit.values[0]
        elif unit.mode == ELIMINATE:
            puzzle[unit.row, unit.column].remove_possible(*unit.values)
        elif unit.mode == LIMIT:
            puzzle[unit.row, unit.column].limit_possible(*unit.values)

    

class StepUnitSetBuilder:
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.units = []
        self.puzzle_modified = False
    
    def add_source_cells(self, *cells, values=None, value=None, mode=SOURCE):
        if values is None and value is not None:
            values = (value,)
        for cell in cells:
            self.units.append(StepUnit(*self.puzzle.index(cell), tuple(values), mode))
        return self
    
    def add_modified_cells(self, *cells, values=None, value=None, mode='unknown'):
        if values is None and value is not None:
            values = (value,)
        for cell in cells:
            self.units.append(StepUnit(*self.puzzle.index(cell), tuple(values), mode))
        if cells:
            self.puzzle_modified = True
        return self
    
    def add_placed_value(self, cell, value):
        return self.add_modified_cells(cell, value=value, mode=PLACE)

    def add_eliminated_cells(self, *cells, values=None, value=None):
        return self.add_modified_cells(*cells, value=value, values=values, mode=ELIMINATE)

    def add_limited_cells(self, *cells, values=None, value=None):
        return self.add_modified_cells(*cells, value=value, values=values, mode=LIMIT)
    
    def final(self):
        if self.puzzle_modified:
            return tuple(self.units)