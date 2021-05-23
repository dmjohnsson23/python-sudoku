from ..exception import SudokuError
from ..model import Puzzle, Cell
from ..variant_context import ClassicContext

class PresolvedTestPuzzleViolation(SudokuError):
    pass

class TestCell(Cell):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._expected_value = None

    @property
    def expected_value(self):
        if self._expected_value is None:
            row, col = self.puzzle.index(self)
            self._expected_value = self.puzzle.solved_array[row][col]
        return self._expected_value
    
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if value != self.expected_value:
            raise PresolvedTestPuzzleViolation(f"Solver placed {value} where {self.expected_value} was the correct solution", self.puzzle, self)
        self._value = value
        self.possible.clear()
    
    def remove_possible(self, *values):
        if self.expected_value in values:
            raise PresolvedTestPuzzleViolation(f"Solver incorrectly removed {self.expected_value} as a candidate", self.puzzle, self)
        super().remove_possible(*values)

    def limit_possible(self, *values):
        if self.expected_value not in values:
            raise PresolvedTestPuzzleViolation(f"Solver incorrectly removed {self.expected_value} as a candidate", self.puzzle, self)
        super().limit_possible(*values)



class TestPuzzle(Puzzle):
    def __init__(self, puzzle_array, solved_array):
        self.solved_array = solved_array
        super().__init__(puzzle_array)
    

class ClassicTestContext(ClassicContext):
    def __init__(self):
        class ContextualizedTestCell(TestCell):
            variant_context = self
        class ContextualizedTestPuzzle(TestPuzzle):
            variant_context = self
        self.Cell = ContextualizedTestCell
        self.Puzzle = ContextualizedTestPuzzle
