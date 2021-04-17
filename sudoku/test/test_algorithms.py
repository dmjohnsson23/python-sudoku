import unittest

from ..model import *
from ..algorithms import *
from ..puzzles import puzzles

class TestBasicAlgorithms(unittest.TestCase):

    def test_eliminate_possibilities(self):
        puzzle = Puzzle(puzzles['Crosswise'])
        eliminate_possibilities(*puzzle.iter_cells())

        self.assertEqual(puzzle[0, 1].possible, set([4, 5, 6, 7, 8, 9]))
        self.assertEqual(puzzle[0, 3].possible, set([2, 3, 5, 6, 7, 8, 9]))
        self.assertEqual(puzzle[3, 0].possible, set([2, 3, 5, 6, 7, 8, 9]))
        self.assertEqual(puzzle[3, 5].possible, set([1, 2, 3, 7, 8, 9]))
        self.assertEqual(puzzle[0, 8].possible, set([2, 3, 4, 5, 6, 7, 8]))


    def test_find_naked_singles(self):
        cells = [
            Cell(possible=[1, 3, 4]),
            Cell(possible=[1, 2, 3, 6]),
            Cell(possible=[2, 3, 4]),
            Cell(possible=[2]),
            Cell(),
            Cell(7),
            Cell(),
            Cell(),
            Cell(),
        ]

        Row(*cells)

        find_naked_singles(*cells)

        self.assertEqual(cells[0].possible, set([1, 3, 4]))
        self.assertEqual(cells[1].possible, set([1, 3, 6]))
        self.assertEqual(cells[2].possible, set([3, 4]))
        self.assertEqual(cells[3].value, 2)
        self.assertEqual(cells[3].possible, set([]))
        self.assertEqual(cells[4].possible, set([1, 3, 4, 5, 6, 7, 8, 9]))
        self.assertEqual(cells[5].value, 7)
        self.assertEqual(cells[5].possible, set([]))
        self.assertEqual(cells[6].possible, set([1, 3, 4, 5, 6, 7, 8, 9]))
        self.assertEqual(cells[7].possible, set([1, 3, 4, 5, 6, 7, 8, 9]))
        self.assertEqual(cells[8].possible, set([1, 3, 4, 5, 6, 7, 8, 9]))


    def test_find_hidden_singles(self):
        row = Row(
            Cell(1),
            Cell(2),
            Cell(3),
            Cell(4),
            Cell(5),
            Cell(possible=[6, 7, 8, 9]),
            Cell(possible=[7, 8, 9]),
            Cell(possible=[7, 8, 9]),
            Cell(possible=[7, 8, 9]),
        )

        find_hidden_singles(row)

        self.assertEqual(row[5].value, 6)
        self.assertEqual(row[5].possible, set([]))
        self.assertEqual(row[6].possible, set([7, 8, 9]))
        self.assertEqual(row[7].possible, set([7, 8, 9]))
        self.assertEqual(row[8].possible, set([7, 8, 9]))


                
class TestLockedCandidateAlgorithms(unittest.TestCase):

    def test_find_locked_candidates_squares(self):
        puzzle = Puzzle(puzzles['Blank'])
        # Remove the possibility of a 1 from certain cells
        puzzle[1, 0].remove_possible(1)
        puzzle[1, 1].remove_possible(1)
        puzzle[1, 2].remove_possible(1)
        puzzle[2, 0].remove_possible(1)
        puzzle[2, 1].remove_possible(1)
        puzzle[2, 2].remove_possible(1)

        find_locked_candidates_squares(*puzzle.squares)

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
        puzzle = Puzzle(puzzles['Blank'])
        # Remove the possibility of a 5 from certain cells
        for col in range(3, 9):
            puzzle[0, col].remove_possible(5)

        find_locked_candidates_rows_columns(*puzzle.rows)

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
        house = House(
            Cell(),
            Cell(),
            Cell(possible=[3, 4, 5, 6, 7, 8, 9]),
            Cell(possible=[3, 4, 5, 6, 7, 8, 9]),
            Cell(possible=[3, 4, 5, 6, 7, 8, 9]),
            Cell(possible=[3, 4, 5, 6, 7, 8, 9]),
            Cell(possible=[3, 4, 5, 6, 7, 8, 9]),
            Cell(possible=[3, 4, 5, 6, 7, 8, 9]),
            Cell(possible=[3, 4, 5, 6, 7, 8, 9]),
        )

        find_hidden_multiples(house)

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
        house = House(
            Cell(),
            Cell(),
            Cell(),
            Cell(possible=[1, 2, 3, 4, 5, 6]),
            Cell(possible=[1, 2, 3, 4, 5, 6]),
            Cell(possible=[1, 2, 3, 4, 5, 6]),
            Cell(possible=[1, 2, 3, 4, 5, 6]),
            Cell(possible=[1, 2, 3, 4, 5, 6]),
            Cell(possible=[1, 2, 3, 4, 5, 6]),
        )

        find_hidden_multiples(house)

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
        house = House(
            Cell(possible=[1, 2]),
            Cell(possible=[1, 2]),
            Cell(),
            Cell(),
            Cell(),
            Cell(),
            Cell(),
            Cell(),
            Cell(),
        )

        find_naked_multiples(house)

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
        house = House(
            Cell(possible=[7, 8, 9]),
            Cell(possible=[7, 8, 9]),
            Cell(possible=[7, 8, 9]),
            Cell(),
            Cell(),
            Cell(),
            Cell(),
            Cell(),
            Cell(),
        )

        find_naked_multiples(house)

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
        house = House(
            Cell(possible=[1, 9]),
            Cell(possible=[7, 8, 9]),
            Cell(),
            Cell(6),
            Cell(),
            Cell(),
            Cell(4),
            Cell(),
            Cell(possible=[1, 9]),
        )

        find_naked_multiples(house)

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
        house = House(
            Cell(possible=[1, 9]),
            Cell(possible=[7, 8, 9]),
            Cell(possible=[1, 4, 9]),
            Cell(possible=[3, 5, 6]),
            Cell(possible=[2, 6, 9]),
            Cell(possible=[1, 4, 5, 6]),
            Cell(possible=[4, 7, 8, 9]),
            Cell(possible=[1, 2, 3, 4, 5, 6]),
            Cell(possible=[1, 9]),
        )

        find_naked_multiples(house)

        self.assertEqual(house.cells[0].possible, set([1, 9]))
        self.assertEqual(house.cells[1].possible, set([7, 8]))
        self.assertEqual(house.cells[2].value, 4)
        self.assertEqual(house.cells[2].possible, set())
        self.assertEqual(house.cells[3].possible, set([3, 5, 6]))
        self.assertEqual(house.cells[4].possible, set([2, 6]))
        self.assertEqual(house.cells[5].possible, set([4, 5, 6]))
        self.assertEqual(house.cells[6].possible, set([4, 7, 8]))
        self.assertEqual(house.cells[7].possible, set([2, 3, 4, 5, 6]))
        self.assertEqual(house.cells[8].possible, set([1, 9]))