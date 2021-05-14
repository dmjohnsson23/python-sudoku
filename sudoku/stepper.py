from dataclasses import dataclass
from .model import Puzzle


@dataclass(frozen=True)
class StepUnit:
    """
    A representation to highlight one unit of change in a step. 
    This could be:

    * An elimination of a value from a cell (set mode to 'eliminate')
    * The placing of a value in a cell (set mode to 'place')
    * The designation of a cell as a source cell for an algorithm (set mode to whatever designation is needed for the algorithm)
    """
    row: int
    column: int
    value: int
    mode: str


@dataclass
class Step(frozen=True):
    """
    A representation of one step in a sudoku solve
    """
    algorithm: str
    step_units: tuple[StepUnit]
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
        if unit.mode == 'place':
            puzzle[unit.row, unit.column].value = unit.value
        elif unit.mode == 'eliminate':
            puzzle[unit.row, unit.column].remove_possible(unit.value)

    

