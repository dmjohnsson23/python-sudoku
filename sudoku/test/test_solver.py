from ..model import *
from .models import TestPuzzle
from ..solver import Solver
import sys
import unittest
from ..puzzles import puzzles, solutions
import traceback
from ..variant_context import ClassicContext

class TestSolver(unittest.TestCase):
    def solve_named_puzzle(self, name):
        if name in solutions:
            puzzle = TestPuzzle(puzzles[name], solutions[name])
        else:
            puzzle = Puzzle(puzzles[name])

        solver = Solver(ClassicContext())
        try:
            solution = solver.solve(puzzle)
            success = solution.success
            exception_message = ''
        except Exception as e:
            success = False
            exception_message = '\n\nException Raised:\n'+traceback.format_exc()
        if not success:
            self.fail("Failed to solve puzzle.\n\nInitial state:\n{}\n\nFinal State:\n{}{}".format(
                Puzzle(puzzles[name]),
                puzzle.debug_string,
                exception_message
            ))

    
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
            self.solve_named_puzzle('Brute Force Prevails')
