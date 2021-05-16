import unittest

from ..model import *
from ..algorithms import *
from ..puzzles import puzzles
from ..stepper import Stepper
from .utils import *
from sudoku import stepper


class TestBasicAlgorithms(unittest.TestCase):

    def test_eliminate_possibilities(self):
        puzzle = Puzzle(puzzles['Crosswise'])
        stepper = Stepper(puzzle)
        eliminate_possibilities.run(puzzle, stepper)

        self.assertEqual(puzzle[0, 1].possible, set([4, 5, 6, 7, 8, 9]))
        self.assertEqual(puzzle[0, 3].possible, set([2, 3, 5, 6, 7, 8, 9]))
        self.assertEqual(puzzle[3, 0].possible, set([2, 3, 5, 6, 7, 8, 9]))
        self.assertEqual(puzzle[3, 5].possible, set([1, 2, 3, 7, 8, 9]))
        self.assertEqual(puzzle[0, 8].possible, set([2, 3, 4, 5, 6, 7, 8]))


    def test_find_naked_singles(self):
        puzzle = empty_grid()
        stepper = Stepper(puzzle)
        row = puzzle.rows[0]

        row[0].limit_possible(1, 3, 4)
        row[1].limit_possible(1, 2, 3, 6)
        row[2].limit_possible(2, 3, 4)
        row[3].limit_possible(2)
        row[5].value = 7

        success = find_naked_singles.run(puzzle, stepper)
        self.assertTrue(success, "Algorithm should update puzzle")

        self.assertEqual(row[0].possible, set([1, 3, 4]), "Other cells should not be affected")
        self.assertEqual(row[1].possible, set([1, 2, 3, 6]), "Other cells should not be affected")
        self.assertEqual(row[2].possible, set([2, 3, 4]), "Other cells should not be affected")
        self.assertEqual(row[3].value, 2, "Naked value should be properly set")
        self.assertEqual(row[3].possible, set(), "Naked value should be properly set")
        self.assertEqual(row[4].possible, set([1, 2, 3, 4, 5, 6, 7, 8, 9]), "Other cells should not be affected")
        self.assertEqual(row[5].value, 7, "Other cells should not be affected")
        self.assertEqual(row[5].possible, set(), "Other cells should not be affected")
        self.assertEqual(row[6].possible, set([1, 2, 3, 4, 5, 6, 7, 8, 9]), "Other cells should not be affected")
        self.assertEqual(row[7].possible, set([1, 2, 3, 4, 5, 6, 7, 8, 9]), "Other cells should not be affected")
        self.assertEqual(row[8].possible, set([1, 2, 3, 4, 5, 6, 7, 8, 9]), "Other cells should not be affected")


    def test_find_hidden_singles(self):
        puzzle = empty_grid()
        stepper = Stepper(puzzle)
        row = puzzle.rows[0]

        row[0].value = 1
        row[1].value = 2
        row[2].value = 3
        row[3].value = 4
        row[4].value = 5
        row[5].limit_possible(6, 7, 8, 9)
        row[6].limit_possible(7, 8, 9)
        row[7].limit_possible(7, 8, 9)
        row[8].limit_possible(7, 8, 9)
        

        find_hidden_singles.run(puzzle, stepper)

        self.assertEqual(row[5].value, 6)
        self.assertEqual(row[5].possible, set([]))
        self.assertEqual(row[6].possible, set([7, 8, 9]))
        self.assertEqual(row[7].possible, set([7, 8, 9]))
        self.assertEqual(row[8].possible, set([7, 8, 9]))


                
class TestLockedCandidateAlgorithms(unittest.TestCase):

    def test_find_locked_candidates_squares(self):
        puzzle = empty_grid()
        stepper = Stepper(puzzle)
        # Remove the possibility of a 1 from certain cells
        puzzle[1, 0].remove_possible(1)
        puzzle[1, 1].remove_possible(1)
        puzzle[1, 2].remove_possible(1)
        puzzle[2, 0].remove_possible(1)
        puzzle[2, 1].remove_possible(1)
        puzzle[2, 2].remove_possible(1)

        find_locked_candidates_squares.run(puzzle, stepper)

        # Make sure the effect was correct
        for col in range(3):
            cell = puzzle[0, col]
            self.assertEqual(cell.possible, set([1, 2, 3, 4, 5, 6, 7, 8, 9]), 
            'First 3 (group source) cells should be unaffected by algorithm, coords: {}'.format(puzzle.index(cell)))
        for col in range(3, 9):
            cell = puzzle[0, col]
            self.assertEqual(cell.possible, set([2, 3, 4, 5, 6, 7, 8, 9]), 
            '1 should be removed from all other cells in the row, coords: {}'.format(puzzle.index(cell)))
        for row in puzzle.rows[3:]:
            for cell in row:
                self.assertEqual(cell.possible, set([1, 2, 3, 4, 5, 6, 7, 8, 9]), 
                'Cells below the third row should be unaffected, coords: {}'.format(puzzle.index(cell)))
    

    def test_find_locked_candidates_rows_columns(self):
        puzzle = empty_grid()
        stepper = Stepper(puzzle)
        # Remove the possibility of a 5 from certain cells
        for col in range(3, 9):
            puzzle[0, col].remove_possible(5)

        find_locked_candidates_rows_columns.run(puzzle, stepper)

        # Make sure the effect was correct
        for col in range(3):
            cell = puzzle[0, col]
            self.assertEqual(cell.possible, set([1, 2, 3, 4, 5, 6, 7, 8, 9]), 
            'First 3 (group source) cells should be unaffected by algorithm, coords: {}'.format(puzzle.index(cell)))
        self.assertEqual(puzzle[1, 0].possible, set([1, 2, 3, 4, 6, 7, 8, 9]), '5 should be removed from other cells in the first square')
        self.assertEqual(puzzle[1, 1].possible, set([1, 2, 3, 4, 6, 7, 8, 9]), '5 should be removed from other cells in the first square')
        self.assertEqual(puzzle[1, 2].possible, set([1, 2, 3, 4, 6, 7, 8, 9]), '5 should be removed from other cells in the first square')
        self.assertEqual(puzzle[2, 0].possible, set([1, 2, 3, 4, 6, 7, 8, 9]), '5 should be removed from other cells in the first square')
        self.assertEqual(puzzle[2, 1].possible, set([1, 2, 3, 4, 6, 7, 8, 9]), '5 should be removed from other cells in the first square')
        self.assertEqual(puzzle[2, 2].possible, set([1, 2, 3, 4, 6, 7, 8, 9]), '5 should be removed from other cells in the first square')
        for row in puzzle.rows[3:]:
            for cell in row:
                self.assertEqual(cell.possible, set([1, 2, 3, 4, 5, 6, 7, 8, 9]), 
                'Cells below the third row should be unaffected, coords: {}'.format(puzzle.index(cell)))



class TestFindHiddenMultiples(unittest.TestCase):

    def test_simple_2(self):
        puzzle = empty_grid()
        stepper = Stepper(puzzle)
        
        house = puzzle.rows[0]
        house[2].remove_possible(1, 2)
        house[3].remove_possible(1, 2)
        house[4].remove_possible(1, 2)
        house[5].remove_possible(1, 2)
        house[6].remove_possible(1, 2)
        house[7].remove_possible(1, 2)
        house[8].remove_possible(1, 2)

        find_hidden_multiples.run(puzzle, stepper)

        self.assertEqual(house.cells[0].possible, set([1, 2]))
        self.assertEqual(house.cells[1].possible, set([1, 2]))
        self.assertEqual(house.cells[2].possible, set([3, 4, 5, 6, 7, 8, 9]))
        self.assertEqual(house.cells[3].possible, set([3, 4, 5, 6, 7, 8, 9]))
        self.assertEqual(house.cells[4].possible, set([3, 4, 5, 6, 7, 8, 9]))
        self.assertEqual(house.cells[5].possible, set([3, 4, 5, 6, 7, 8, 9]))
        self.assertEqual(house.cells[6].possible, set([3, 4, 5, 6, 7, 8, 9]))
        self.assertEqual(house.cells[7].possible, set([3, 4, 5, 6, 7, 8, 9]))
        self.assertEqual(house.cells[8].possible, set([3, 4, 5, 6, 7, 8, 9]))


    def test_simple_3(self):
        puzzle = empty_grid()
        stepper = Stepper(puzzle)
        
        house = puzzle.rows[0]
        house[3].remove_possible(7, 8, 9)
        house[4].remove_possible(7, 8, 9)
        house[5].remove_possible(7, 8, 9)
        house[6].remove_possible(7, 8, 9)
        house[7].remove_possible(7, 8, 9)
        house[8].remove_possible(7, 8, 9)

        find_hidden_multiples.run(puzzle, stepper)

        self.assertEqual(house.cells[0].possible, set([7, 8, 9]))
        self.assertEqual(house.cells[1].possible, set([7, 8, 9]))
        self.assertEqual(house.cells[2].possible, set([7, 8, 9]))
        self.assertEqual(house.cells[3].possible, set([1, 2, 3, 4, 5, 6]))
        self.assertEqual(house.cells[4].possible, set([1, 2, 3, 4, 5, 6]))
        self.assertEqual(house.cells[5].possible, set([1, 2, 3, 4, 5, 6]))
        self.assertEqual(house.cells[6].possible, set([1, 2, 3, 4, 5, 6]))
        self.assertEqual(house.cells[7].possible, set([1, 2, 3, 4, 5, 6]))
        self.assertEqual(house.cells[8].possible, set([1, 2, 3, 4, 5, 6]))


class TestFindNakedMultiples(unittest.TestCase):
    def test_simple_2(self):
        puzzle = empty_grid()
        stepper = Stepper(puzzle)
        
        house = puzzle.rows[0]
        house[0].limit_possible(1, 2)
        house[1].limit_possible(1, 2)

        find_naked_multiples.run(puzzle, stepper)

        self.assertEqual(house.cells[0].possible, set([1, 2]))
        self.assertEqual(house.cells[1].possible, set([1, 2]))
        self.assertEqual(house.cells[2].possible, set([3, 4, 5, 6, 7, 8, 9]))
        self.assertEqual(house.cells[3].possible, set([3, 4, 5, 6, 7, 8, 9]))
        self.assertEqual(house.cells[4].possible, set([3, 4, 5, 6, 7, 8, 9]))
        self.assertEqual(house.cells[5].possible, set([3, 4, 5, 6, 7, 8, 9]))
        self.assertEqual(house.cells[6].possible, set([3, 4, 5, 6, 7, 8, 9]))
        self.assertEqual(house.cells[7].possible, set([3, 4, 5, 6, 7, 8, 9]))
        self.assertEqual(house.cells[8].possible, set([3, 4, 5, 6, 7, 8, 9]))

    def test_simple_3(self):
        puzzle = empty_grid()
        stepper = Stepper(puzzle)
        
        house = puzzle.rows[0]
        house[0].limit_possible(7, 8, 9)
        house[1].limit_possible(7, 8, 9)
        house[2].limit_possible(7, 8, 9)

        find_naked_multiples.run(puzzle, stepper)

        self.assertEqual(house.cells[0].possible, set([7, 8, 9]))
        self.assertEqual(house.cells[1].possible, set([7, 8, 9]))
        self.assertEqual(house.cells[2].possible, set([7, 8, 9]))
        self.assertEqual(house.cells[3].possible, set([1, 2, 3, 4, 5, 6]))
        self.assertEqual(house.cells[4].possible, set([1, 2, 3, 4, 5, 6]))
        self.assertEqual(house.cells[5].possible, set([1, 2, 3, 4, 5, 6]))
        self.assertEqual(house.cells[6].possible, set([1, 2, 3, 4, 5, 6]))
        self.assertEqual(house.cells[7].possible, set([1, 2, 3, 4, 5, 6]))
        self.assertEqual(house.cells[8].possible, set([1, 2, 3, 4, 5, 6]))
    
    def test_some_filled(self):
        puzzle = empty_grid()
        stepper = Stepper(puzzle)
        
        house = puzzle.rows[0]
        house[0].limit_possible(1, 9)
        house[1].limit_possible(7, 8, 9)
        house[3].value = 6
        house[6].value = 4
        house[8].limit_possible(1, 9)

        find_naked_multiples.run(puzzle, stepper)

        self.assertEqual(house.cells[0].possible, set([1, 9]))
        self.assertEqual(house.cells[1].possible, set([7, 8]))
        self.assertEqual(house.cells[2].possible, set([2, 3, 4, 5, 6, 7, 8]))
        self.assertEqual(house.cells[3].possible, set([]))
        self.assertEqual(house.cells[4].possible, set([2, 3, 4, 5, 6, 7, 8]))
        self.assertEqual(house.cells[5].possible, set([2, 3, 4, 5, 6, 7, 8]))
        self.assertEqual(house.cells[6].possible, set([]))
        self.assertEqual(house.cells[7].possible, set([2, 3, 4, 5, 6, 7, 8]))
        self.assertEqual(house.cells[8].possible, set([1, 9]))

    def test_all_mixed(self):
        puzzle = empty_grid()
        stepper = Stepper(puzzle)
        
        house = puzzle.rows[0]
        house[0].limit_possible(1, 9)
        house[1].limit_possible(7, 8, 9)
        house[2].limit_possible(1, 4, 9)
        house[3].limit_possible(3, 5, 6)
        house[4].limit_possible(2, 6, 9)
        house[5].limit_possible(1, 4, 5, 6)
        house[6].limit_possible(4, 7, 8, 9)
        house[7].limit_possible(1, 2, 3, 4, 5, 6)
        house[8].limit_possible(1, 9)

        find_naked_multiples.run(puzzle, stepper)

        self.assertEqual(house.cells[0].possible, set([1, 9]))
        self.assertEqual(house.cells[1].possible, set([7, 8]))
        self.assertEqual(house.cells[2].possible, set([4]))
        self.assertEqual(house.cells[3].possible, set([3, 5, 6]))
        self.assertEqual(house.cells[4].possible, set([2, 6]))
        self.assertEqual(house.cells[5].possible, set([4, 5, 6]))
        self.assertEqual(house.cells[6].possible, set([4, 7, 8]))
        self.assertEqual(house.cells[7].possible, set([2, 3, 4, 5, 6]))
        self.assertEqual(house.cells[8].possible, set([1, 9]))


class TestXwingSwordfish(unittest.TestCase):
    def test_find_xwing_rows(self):
        puzzle = grid_with_possible_only_at_coordinates(
            # The 4 wings
            (2, 5),
            (2, 8),
            (6, 5),
            (6, 8),
            # Some values to eliminate
            (1, 5),
            (8, 5),
            (7, 8),
            (8, 8),
            # Some values to leave alone
            (0, 0),
            (1, 1),
            (1, 6)
        )
        stepper = Stepper(puzzle)

        success = find_x_wing.run(puzzle, stepper)

        self.assertTrue(success, "Algorithm should detect x-wing")

        self.assertFalse(puzzle[1, 5].has_possible(1), "1 should be removed from cell (1, 5)")
        self.assertFalse(puzzle[8, 5].has_possible(1), "1 should be removed from cell (8, 5)")
        self.assertFalse(puzzle[7, 8].has_possible(1), "1 should be removed from cell (7, 8)")
        self.assertFalse(puzzle[8, 8].has_possible(1), "1 should be removed from cell (8, 8)")
        self.assertTrue(puzzle[0, 0].has_possible(1), "1 should not be removed from cell (0, 0)")
        self.assertTrue(puzzle[1, 1].has_possible(1), "1 should not be removed from cell (1, 1)")
        self.assertTrue(puzzle[1, 6].has_possible(1), "1 should not be removed from cell (1, 6)")
