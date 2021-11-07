from ..model import *
from .models import ClassicTestContext
from ..solver import Solver
import sys
import unittest
from .puzzles import puzzles, solutions
import traceback
from ..variant_context import ClassicContext
from .utils import solve_puzzle

class TestSolver(unittest.TestCase):
    def solve_named_puzzle(self, name, *solver_args, **solver_kwargs):
        if name in solutions:
            context = ClassicTestContext()
            puzzle = context.Puzzle(puzzles[name], solutions[name])
        else:
            context = ClassicContext()
            puzzle = context.Puzzle(puzzles[name])

        solve_puzzle(self, context, puzzle, *solver_args, **solver_kwargs)

    
    def test_already_solved(self):
        self.solve_named_puzzle('Already Solved')
    
    def test_ridiculously_easy(self):
        self.solve_named_puzzle('Ridiculously Easy')

    def test_easy(self):
        self.solve_named_puzzle('Easy 7,797,002,451')

    def test_medium(self):
        self.solve_named_puzzle('Medium 1,465,295,375')

    def test_hard(self):
        self.solve_named_puzzle('Hard 4,658,865,853')

    def test_evil(self):
        self.solve_named_puzzle('Evil 7,360,298,562')

    def test_only_17(self):
        self.solve_named_puzzle('Only 17')

    def test_brute_force(self):
        # This puzzle has 2 solutions and therefore can only be solved with brute force
        with self.assertWarns(Warning):
            self.solve_named_puzzle('Brute Force Prevails', brute_force_level=1)
