from ..extensions.index159 import *
from ..stepper import Stepper
from .puzzles import index_159_puzzles
from .utils import solve_puzzle
import unittest

class TestIndex159Algorithms(unittest.TestCase):

    def test_apply_pointers_forward(self):
        puzzle = Classic159Context().Puzzle()
        stepper = Stepper(puzzle)
        puzzle[0, 0].value = 7
        apply_pointers_forward.run(puzzle, stepper)

        self.assertEqual(puzzle[0, 6].value, 1)



    def test_apply_pointers_backward(self):
        puzzle = Classic159Context().Puzzle()
        stepper = Stepper(puzzle)
        puzzle[0, 6].value = 1
        apply_pointers_backward.run(puzzle, stepper)

        self.assertEqual(puzzle[0, 0].value, 7)
    

    def test_solve(self):
        context = Classic159Context()
        puzzle = context.Puzzle(index_159_puzzles['CTC Intro'])
        solve_puzzle(self, context, puzzle)
