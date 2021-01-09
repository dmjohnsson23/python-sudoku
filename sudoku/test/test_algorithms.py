import unittest

from ..model import *
from ..algorithms import *
from ..puzzles import puzzles

class TestBasicAlgorithms(unittest.TestCase):

    def test_eliminate_possibilities(self):
        puzzle = Puzzle(puzzles['Crosswise'])
        eliminate_possibilities(*puzzle.iter_cells())

        self.assertEqual(puzzle[0, 1].possible, [4, 5, 6, 7, 8, 9])
        self.assertEqual(puzzle[0, 3].possible, [2, 3, 5, 6, 7, 8, 9])
        self.assertEqual(puzzle[3, 0].possible, [2, 3, 5, 6, 7, 8, 9])
        self.assertEqual(puzzle[3, 5].possible, [1, 2, 3, 7, 8, 9])
        self.assertEqual(puzzle[0, 8].possible, [2, 3, 4, 5, 6, 7, 8])


    def test_find_single_possibilities(self):
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

        find_single_possibilities(*cells)

        self.assertEqual(cells[0].possible, [1, 3, 4])
        self.assertEqual(cells[1].possible, [1, 3, 6])
        self.assertEqual(cells[2].possible, [3, 4])
        self.assertEqual(cells[3].value, 2)
        self.assertEqual(cells[3].possible, [])
        self.assertEqual(cells[4].possible, [1, 3, 4, 5, 6, 7, 8, 9])
        self.assertEqual(cells[5].value, 7)
        self.assertEqual(cells[5].possible, [])
        self.assertEqual(cells[6].possible, [1, 3, 4, 5, 6, 7, 8, 9])
        self.assertEqual(cells[7].possible, [1, 3, 4, 5, 6, 7, 8, 9])
        self.assertEqual(cells[8].possible, [1, 3, 4, 5, 6, 7, 8, 9])


    def test_find_exclusive_possibilities(self):
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

        find_exclusive_possibilities(row)

        self.assertEqual(row[5].value, 6)
        self.assertEqual(row[5].possible, [])
        self.assertEqual(row[6].possible, [7, 8, 9])
        self.assertEqual(row[7].possible, [7, 8, 9])
        self.assertEqual(row[8].possible, [7, 8, 9])


                
class TestAlignedAlgorithms(unittest.TestCase):

    def test_find_aligned_in_square(self):
        puzzle = Puzzle(puzzles['Blank'])
        # Remove the possibility of a 1 from certain cells
        puzzle[1, 0].remove_possible(1)
        puzzle[1, 1].remove_possible(1)
        puzzle[1, 2].remove_possible(1)
        puzzle[2, 0].remove_possible(1)
        puzzle[2, 1].remove_possible(1)
        puzzle[2, 2].remove_possible(1)

        find_aligned_in_square(*puzzle.squares)

        # Make sure the effect was correct
        for col in range(3):
            cell = puzzle[0, col]
            self.assertEqual(cell.possible, [1, 2, 3, 4, 5, 6, 7, 8, 9], 
            'First 3 (group source) cells should be unaffected by algorithm, coords: {}'.format(puzzle.index(cell)))
        for col in range(3, 9):
            cell = puzzle[0, col]
            self.assertEqual(cell.possible, [2, 3, 4, 5, 6, 7, 8, 9], 
            '1 should be removed from all other cells in the row, coords: {}'.format(puzzle.index(cell)))
        for row in puzzle.rows[3:]:
            for cell in row:
                self.assertEqual(cell.possible, [1, 2, 3, 4, 5, 6, 7, 8, 9], 
                'Cells below the third row should be unaffected, coords: {}'.format(puzzle.index(cell)))
    

    def test_find_aligned_in_row_or_column(self):
        puzzle = Puzzle(puzzles['Blank'])
        # Remove the possibility of a 5 from certain cells
        for col in range(3, 9):
            puzzle[0, col].remove_possible(5)

        find_aligned_in_row_or_column(*puzzle.rows)

        # Make sure the effect was correct
        for col in range(3):
            cell = puzzle[0, col]
            self.assertEqual(cell.possible, [1, 2, 3, 4, 5, 6, 7, 8, 9], 
            'First 3 (group source) cells should be unaffected by algorithm, coords: {}'.format(puzzle.index(cell)))
        self.assertEqual(puzzle[1, 0].possible, [1, 2, 3, 4, 6, 7, 8, 9], '5 should be removed from other cells in the first square')
        self.assertEqual(puzzle[1, 1].possible, [1, 2, 3, 4, 6, 7, 8, 9], '5 should be removed from other cells in the first square')
        self.assertEqual(puzzle[1, 2].possible, [1, 2, 3, 4, 6, 7, 8, 9], '5 should be removed from other cells in the first square')
        self.assertEqual(puzzle[2, 0].possible, [1, 2, 3, 4, 6, 7, 8, 9], '5 should be removed from other cells in the first square')
        self.assertEqual(puzzle[2, 1].possible, [1, 2, 3, 4, 6, 7, 8, 9], '5 should be removed from other cells in the first square')
        self.assertEqual(puzzle[2, 2].possible, [1, 2, 3, 4, 6, 7, 8, 9], '5 should be removed from other cells in the first square')
        for row in puzzle.rows[3:]:
            for cell in row:
                self.assertEqual(cell.possible, [1, 2, 3, 4, 5, 6, 7, 8, 9], 
                'Cells below the third row should be unaffected, coords: {}'.format(puzzle.index(cell)))



class TestFindExclusiveGroups(unittest.TestCase):

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

        find_exclusive_groups(house)

        self.assertEqual(house.cells[0].possible, [1, 2])
        self.assertEqual(house.cells[1].possible, [1, 2])
        self.assertEqual(house.cells[2].possible, [3, 4, 5, 6, 7, 8, 9])
        self.assertEqual(house.cells[3].possible, [3, 4, 5, 6, 7, 8, 9])
        self.assertEqual(house.cells[4].possible, [3, 4, 5, 6, 7, 8, 9])
        self.assertEqual(house.cells[5].possible, [3, 4, 5, 6, 7, 8, 9])
        self.assertEqual(house.cells[6].possible, [3, 4, 5, 6, 7, 8, 9])
        self.assertEqual(house.cells[7].possible, [3, 4, 5, 6, 7, 8, 9])
        self.assertEqual(house.cells[8].possible, [3, 4, 5, 6, 7, 8, 9])


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

        find_constrained_groups(house)

        self.assertEqual(house.cells[0].possible, [7, 8, 9])
        self.assertEqual(house.cells[1].possible, [7, 8, 9])
        self.assertEqual(house.cells[2].possible, [7, 8, 9])
        self.assertEqual(house.cells[3].possible, [1, 2, 3, 4, 5, 6])
        self.assertEqual(house.cells[4].possible, [1, 2, 3, 4, 5, 6])
        self.assertEqual(house.cells[5].possible, [1, 2, 3, 4, 5, 6])
        self.assertEqual(house.cells[6].possible, [1, 2, 3, 4, 5, 6])
        self.assertEqual(house.cells[7].possible, [1, 2, 3, 4, 5, 6])
        self.assertEqual(house.cells[8].possible, [1, 2, 3, 4, 5, 6])


class TestFindConstrainedGroups(unittest.TestCase):
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

        find_constrained_groups(house)

        self.assertEqual(house.cells[0].possible, [1, 2])
        self.assertEqual(house.cells[1].possible, [1, 2])
        self.assertEqual(house.cells[2].possible, [3, 4, 5, 6, 7, 8, 9])
        self.assertEqual(house.cells[3].possible, [3, 4, 5, 6, 7, 8, 9])
        self.assertEqual(house.cells[4].possible, [3, 4, 5, 6, 7, 8, 9])
        self.assertEqual(house.cells[5].possible, [3, 4, 5, 6, 7, 8, 9])
        self.assertEqual(house.cells[6].possible, [3, 4, 5, 6, 7, 8, 9])
        self.assertEqual(house.cells[7].possible, [3, 4, 5, 6, 7, 8, 9])
        self.assertEqual(house.cells[8].possible, [3, 4, 5, 6, 7, 8, 9])

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

        find_constrained_groups(house)

        self.assertEqual(house.cells[0].possible, [7, 8, 9])
        self.assertEqual(house.cells[1].possible, [7, 8, 9])
        self.assertEqual(house.cells[2].possible, [7, 8, 9])
        self.assertEqual(house.cells[3].possible, [1, 2, 3, 4, 5, 6])
        self.assertEqual(house.cells[4].possible, [1, 2, 3, 4, 5, 6])
        self.assertEqual(house.cells[5].possible, [1, 2, 3, 4, 5, 6])
        self.assertEqual(house.cells[6].possible, [1, 2, 3, 4, 5, 6])
        self.assertEqual(house.cells[7].possible, [1, 2, 3, 4, 5, 6])
        self.assertEqual(house.cells[8].possible, [1, 2, 3, 4, 5, 6])
    
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

        find_constrained_groups(house)

        self.assertEqual(house.cells[0].possible, [1, 9])
        self.assertEqual(house.cells[1].possible, [7, 8])
        self.assertEqual(house.cells[2].possible, [2, 3, 4, 5, 6, 7, 8])
        self.assertEqual(house.cells[3].possible, [])
        self.assertEqual(house.cells[4].possible, [2, 3, 4, 5, 6, 7, 8])
        self.assertEqual(house.cells[5].possible, [2, 3, 4, 5, 6, 7, 8])
        self.assertEqual(house.cells[6].possible, [])
        self.assertEqual(house.cells[7].possible, [2, 3, 4, 5, 6, 7, 8])
        self.assertEqual(house.cells[8].possible, [1, 9])

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

        find_constrained_groups(house)

        self.assertEqual(house.cells[0].possible, [1, 9])
        self.assertEqual(house.cells[1].possible, [7, 8])
        self.assertEqual(house.cells[2].value, 4)
        self.assertEqual(house.cells[2].possible, [])
        self.assertEqual(house.cells[3].possible, [3, 5, 6])
        self.assertEqual(house.cells[4].possible, [2, 6])
        self.assertEqual(house.cells[5].possible, [4, 5, 6])
        self.assertEqual(house.cells[6].possible, [4, 7, 8])
        self.assertEqual(house.cells[7].possible, [2, 3, 4, 5, 6])
        self.assertEqual(house.cells[8].possible, [1, 9])