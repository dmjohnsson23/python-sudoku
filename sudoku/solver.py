from .exception import SudokuError
from .stepper import Stepper, StepUnit, PLACE
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
        
        for _ in self.step_through_algorithms(puzzle, stepper):
            pass
        
        if puzzle.is_solved:
            ok, problem_cell = self.variant_context.check_puzzle(puzzle)
            if ok:
                return Solution(True, stepper, puzzle)
            else:
                raise SudokuError("Invalid Solution", puzzle, cell=problem_cell, stepper=stepper)
        else:
            if brute_force_level:
                brute_forced = self.brute_force_solve(puzzle, brute_force_level)
                if brute_forced is not None:
                    puzzle.update(brute_forced.puzzle)
                    warnings.warn("Brute force used; puzzle may not have a unique solution")
                    return Solution(True, stepper, puzzle)
                    
            return Solution(False, stepper, puzzle)


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
            cell_index = puzzle.index(cell)
            for possible in cell.possible:
                copy_puzzle = puzzle.copy()
                copy_stepper = stepper.copy()
                copy_cell = copy_puzzle[cell_index]
                copy_cell.value = possible
                copy_stepper.record_step('brute_force', StepUnit(*cell_index, (possible,), PLACE))
                try:
                    solution = self.solve(copy_puzzle, brute_force_level = (recurse_level-1) if recurse_level else 0)
                except SudokuError:
                    continue #Try the next possibility
                else:
                    if solution.success:
                        return solution
    

    def step_through_algorithms(self, puzzle: Puzzle, stepper: Stepper):
        """
        Run through the list of algorithms repeatedly, from the first until an algorithm 
        reports having updated the puzzle. Then restarts from the beginning. Stop iterating 
        if, after a full cycle, no algorithm has reported a change.

        This is a generator function. It yields None after every completed step to allow 
        stepping through a solve one step at a time. The current state can be examined if 
        desired by inspecting the puzzle and stepper objects passed as parameters, as they 
        are modified in-place.
        """
        algorithms = self.variant_context.get_algorithms(self.algorithms)
        # TODO we need to get setup algorithms (negative difficulty), run them once each, and remove them from the list
        while True:
            try:
                for alg in algorithms:
                    if alg.run(puzzle, stepper):
                        # break out of the for loop and start over with the most basic algorithm. This ensures 
                        # we are always using the most simple techniques possible, only reaching for advanced 
                        # techniques when required
                        yield
                        if alg is not algorithms[0]: # If this is the first algorithm, no need to run it again
                            break 
                else:
                    # All algorithms ran without changing anything, break the outer while loop
                    break
            except SudokuError as err:
                # We want to add the stepper to any raised sudoku errors for debug purposes
                err.stepper = stepper
                raise err
