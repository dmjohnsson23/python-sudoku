import unittest

from ..variant_context import ClassicContext
from .puzzles import puzzles
from .utils import *


class TestTestingUtilities(unittest.TestCase):
    def test_empty_grid(self):
        puzzle = empty_grid()
        for cell in puzzle.iter_cells():
            self.assertCountEqual(cell.possible, range(1, 10), "All values should be possible for all cells")
            self.assertIsNone(cell.value, "All given values should be present in the puzzle")

    def test_grid_with_possible_only_at_coordinates(self):
        base_puzzle = ClassicContext().Puzzle(puzzles["Already Solved"])
        working_puzzle = None
        for value in range(1, 10):
            coords = set()
            for row in range(9):
                for col in range(9):
                    cell = base_puzzle[row, col]
                    if cell.value == value:
                        coords.add((row, col))
            self.assertEqual(len(coords), 9, 
                "The testing code should find exactly nine coords for each value, "
                "{} found for value {}. This (probably) is a bug in test code, not program code.".format(coords, value))
            working_puzzle = grid_with_possible_only_at_coordinates(*coords, starting_puzzle=working_puzzle, candidate_value=value)
            for row in range(9):
                for col in range(9):
                    base_cell = base_puzzle[row, col]
                    working_cell = working_puzzle[row, col]
                    self.assertTrue(
                        working_cell.has_possible(base_cell.value), 
                        "The possible value of each cell should always contain the actual value "
                        "in the original puzzle. A value of {} was incorrectly removed from ({}, {})\n"
                        "Possible for cell: {}, loop value: {}".format(base_cell.value, row, col, cell.possible, value))
        for cell in working_puzzle.iter_cells():
            self.assertEqual(len(cell.possible), 1, "There should only be one remaining value in each cell after all loops")