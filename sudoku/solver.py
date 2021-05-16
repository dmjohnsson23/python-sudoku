from .exception import SudokuError
from .stepper import Stepper
from .model import Puzzle
from dataclasses import dataclass
import warnings


@dataclass
class Solution:
    success: bool
    steps: Stepper
    puzzle: Puzzle
 
class Solver:
    def __init__(self, variant_context, algorithms='auto'):
        self.variant_context = variant_context
        self.algorithms = algorithms
    

    def solve(self, puzzle: Puzzle, brute_force_level: int = 0, stepper: Stepper = None) -> Solution:
        """
        Try to solve the given puzzle. 

        The puzzle will be modified in-place with the new solution. If you want to keep the
        original value, pass the puzzle with puzzle.copy()
        """
        if stepper is None:
            stepper = Stepper(puzzle)
        algorithms = self.variant_context.get_algorithms(self.algorithms)
        while True:
            try:
                for alg in algorithms:
                    if alg.run(puzzle, stepper):
                        # break out of the for loop and start over with the most basic algorithm. This ensures 
                        # we are always using the most simple techniques possible, only reaching for advanced 
                        # techniques when required
                        break 
                else:
                    # All algorithms ran without changing anything, break the outer while loop
                    break
            except SudokuError as err:
                # We want to add the stepper to any raised sudoku errors for debug purposes
                err.stepper = stepper
                raise err
        
        if puzzle.is_solved:
            ok, problem_cell = self.variant_context.check(puzzle)
            if not ok:
                raise SudokuError("Invalid Solution", puzzle, problem_cell)
        else:
            if brute_force_level:
                brute_forced = self.brute_force_solve(puzzle, brute_force_level)
                if brute_forced is not None:
                    puzzle.update(brute_forced)
                    warnings.warn("Brute force used; puzzle may not have a unique solution")
                    return True
                    
            return False

    def brute_force_solve(self, puzzle: Puzzle, recurse_level: int, stepper: Stepper = None) -> Solution:
        """
        Try to brute force a solution. This will loop through each possibility 
        of each empty cell, and call solve() on a puzzle with that cell set
        to that value.

        Use the `recurse_level` parameter to control how many times the 
        solver will be allowed to recursively attempt a brute force. Higher
        values have better chances of finding solutions, lower values are
        more performant. There is probably little to gain from more than
        one or two recursion layers however.

        Return a solved copy of the puzzle if a solution is found.
        """
        if stepper is None:
            stepper = Stepper(puzzle)
        for cell in puzzle.iter_cells():
            for possible in cell.possible:
                copy = puzzle.copy()
                copy_stepper = stepper.copy()
                copy_stepper.record_step('brute_force')
                copy_cell = copy[puzzle.index(cell)]
                copy_cell.value = possible
                try:
                    success, steps, puzzle = self.solve(copy, brute_force_levels = (recurse_level-1) if recurse_level else 0)
                except SudokuError:
                    continue #Try the next possibility
                else:
                    if success:
                        return success, steps, copy
