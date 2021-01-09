import itertools
import copy
import sys


import puzzles
import utils
#from textTable import Gird, DOUBLE_BORDER as DOUBLE, SINGLE_BORDER as SINGLE

class SudokuError(Exception):
    def __init__(self, errorMessage, puzzle, cell=None):
        msg=[errorMessage, 
             "Puzzle:",
             str(puzzle)]
        
        if cell is not None:
            msg.extend((
                "Problem Cell Details:",
                "\tCoordinates (Indexed from zero): {}".format(puzzle.coordinatesOf(cell)),
                "\tValue: {}".format(cell.value),
                "\tPossible Values: {}".format(cell.possible)
                ))
        Exception.__init__(self, "\n".join(msg))

class Cell:
    "One cell of the puzzle"
    def __init__(self, value=None):
        self.value=value
        if self.value is None:
            self.possible=[1, 2, 3, 4, 5, 6, 7, 8, 9]
        else:
            self.possible=[value]
    
    
    def isFull(self):
        return not self.value is None
    
    
    def isOpen(self):
        return self.value is None
    
    
    def __str__(self):
        if self.isFull():
            return str(self.value)
        else:
            return " "
    
    
    def removePossible(self, value):
        "Safely removes value from cell.possible"
        if value in self.possible:
            self.possible.remove(value)
    
    
    def valueValid(self, value=None):
        "Checks to see if cell.value is valid"
        if value is None:
            value = self.value
        
        return value in utils.SUDOKU_VALUES
    
    
    def setValue(self, value):
        "Sets the value, and removes it from cell.possible for all cells in the same row, column, or square."
        self.value = value
        self.row.eliminatePossible(value)
        self.column.eliminatePossible(value)
        self.square.eliminatePossible(value)
    
    

class House:
    "The base class for columns, rows, and squares"
    def __init__(self, *cells):
        if not len(cells) == 9:
            print(cells)
            raise TypeError("Each row, column, and square must have exactly nine cells")
        self.cells=cells
        
        #The following three vars should be set when cell is added to house
        self.row=None
        self.column=None
        self.square=None
    
    
    def __contains__(self, value):
        for cell in self.cells:
            if cell.value == value:
                return True
        return False
    
    
    def __iter__(self):
        return iter(self.cells)
    
    
    def __getitem__(self, index):
        return self.cells[index]
    
    
    def coordinatesOf(self, cell):
        return self.cells.index(cell)
    
    
    def cellAt(self, index):
        return self.cells[index]
    
    
    def eliminatePossible(self, value):
        "Calls cell.removePossible(value) for every child cell."
        for cell in self.cells:
            cell.removePossible(value)
    
    
    def getAllCellsWithPossible(self, value):
        "Returns a list of all cells with value in cell.possible, skipping full cells."
        r=[]
        for cell in self.cells:
            if cell.isOpen() and value in cell.possible:
                r.append(cell)
        return r
    
    
    @property
    def houses(self):
        h=[]
        
        if self.row is not None: h.append(self.row)
        if self.column is not None: h.append(self.column)
        if self.square is not None: h.append(self.square)
        
        return h
        
        
class Square(House):
    "One 9x9 square of the puzzle"
    def __init__(self, *cells):
        House.__init__(self, *cells)
        for cell in self.cells:
            cell.square=self
    
    
    def coordinatesOf(self, cell):
        "Finds the coordinates (relative to the square) of the cell"
        index=self.cells.index(cell)
        if index < 3:
            return 0, index
        elif index < 6:
            return 1, index-3
        else:
            return 2, index-6
    
    
    def cellAt(self, *args):
        "Returns the cell at the given coordinates (relative to the square)"
        if len(args) == 1:
            row, column = args[0]
        else:
            row, column = args
            
        return self.cells[column+(row*3)]



class Row(House):
    "One row in the puzzle"
    def __init__(self, *cells):
        House.__init__(self, *cells)
        for cell in self.cells:
            cell.row=self


class Column(House):
    "ONe column in the puzzle"
    def __init__(self, *cells):
        House.__init__(self, *cells)
        for cell in self.cells:
            cell.column=self




class Puzzle:
    "The entire puzzle"
    
    def __init__(self, puzzleArray):
        self.rows=[Row(*(Cell(cell) for cell in row)) for row in puzzleArray]
        self.columns=[Column(*(cell for cell in column)) for column in zip(*self.rows)]
        self.squares=[]
        for Y in range(0, 9, 3):
            for X in range(0, 9, 3):
                square=[]
                for y in range(3):
                    for x in range(3):
                        square.append(self.cellAt(Y+y, X+x))
                self.squares.append(Square(*square))
    
    
    def iterCells(self, skipFullCells=False, skipOpenCells=False, centralCell=None):
        "Iterates over all cells in the puzzle. If skipFullCells is "
        "True, skips any cell which already has a value in it. If "
        "centralCell is given, only iterates over cells in the same "
        "row, column, or square as that cell (not including the "
        "central cell itself). When centralCell is given, cells "
        "are in no particular order. If centralCell is not given, "
        "cells are given in order from left to right, top to bottom."
        if centralCell is None:
            for row in self.rows:
                for cell in row:
                    if skipFullCells and cell.isFull():
                        continue
                    if skipOpenCells and cell.isOpen():
                        continue
                    yield cell
        else:
            cells=set(centralCell.row.cells+centralCell.column.cells+centralCell.square.cells)
            cells.remove(centralCell)
            for cell in cells:
                if skipFullCells and cell.isFull():
                    continue
                if skipOpenCells and cell.isOpen():
                    continue
                yield cell
    
    
    def iterHouses(self):
        "Iterates over all rows, columns, and squares"
        return itertools.chain(self.rows, self.columns, self.squares)
    
    
    def update(self, other):
        "For every filled cell in other, set that same cell in self to otherCell.value"
        for cell, otherCell in zip(self.iterCells(), other.iterCells()):
            if otherCell.isFull():
                cell.setValue(otherCell.value)
    
    
    def coordinatesOf(self, cell):
        "Returns the global coordinates of the cell"
        return (self.rows.index(cell.row), cell.row.cells.index(cell))
    
    
    def cellAt(self, *args):
        "Returns the cell at the given global coordinates."
        "Accepts either cellAt(row, col) or cellAt((row, col))."
        if len(args) == 1:
            row, column = args[0]
        else:
            row, column = args
        return self.rows[row][column]
    
    
    def copy(self):
        return copy.deepcopy(self)
    
    
    def __str__(self):
        return PUZZLE_FORMAT_STRING.format(*(str(cell) for cell in self.iterCells()))
    
    
    #puzzle solving logic functions
    
    def isSolved(self):
        "Returns True if all the cells in the puzzle are filled. "
        "Does not check if solution is valid. Use check for that."
        for cell in self.iterCells():
            if cell.isOpen():
                return False
        return True
    
    def check(self):
        "Checks to make sure all values in puzzle are acceptable."
        "Does not check if puzzle is actually solved. Use isSolved for that."
        for cell in self.iterCells():
            if cell.isOpen():
                if not 1 <= len(cell.possible) <= 9:
                    return False, cell
            
            else:
                if not cell.valueValid():
                    return False, cell
                
                for otherCell in self.iterCells(centralCell=cell):
                    if cell.value==otherCell.value:
                        return False, cell
        return True, None
    
    
    def eliminatePossibilities(self):
        "Eliminates any possibilities from cell which are not possible. "
        for cell in self.iterCells():
            if cell.isFull():
                cell.square.eliminatePossible(cell.value)
                cell.row.eliminatePossible(cell.value)
                cell.column.eliminatePossible(cell.value)
                    
    
    
    def searchForSinglePossibilities(self):
        "If there is only one possibility in a cell, sets that cell to "
        "it's only possible value"
        modified = False
        
        for cell in self.iterCells(skipFullCells=True):
            if len(cell.possible) == 1:
                cell.setValue(cell.possible[0])
                modified = True
                
        return modified
    
    
    def searchForExclusivePossibilities(self):
        "Checks to see if there are any cells which are the only possible "
        "location in their row, column, or square which can contain a certain "
        "value. If so, sets the cell(s) to that value."
        modified = False
        
        for house in self.iterHouses():
            for value in utils.SUDOKU_VALUES:
                cells = house.getAllCellsWithPossible(value) #Note: Skips full cells
                if len(cells) == 1: #i.e. There is only one cell in house that can be value
                    cells[0].setValue(value)
                    modified = True
        return modified
    
    
    def searchForAllAligned(self):
        "Searches all squares to see if all the possible cells "
        "for a value are in a line. If so, removes that value "
        "from all other cells in that row/column. For example,\n"
        "╔═══╤═══╤═══╦═══╤═══╤═══╦\n"
        "║   │ x │ x ║ x │ x │ x ║\n"
        "╟───┼───┼───╫───┼───┼───╫\n"
        "║   │   │   ║ x │ x │ x ║\n"
        "╟───┼───┼───╫───┼───┼───╫\n"
        "║   │   │   ║   │   │   ║\n"
        "╠═══╪═══╪═══╬═══╪═══╪═══╬\n"
        "becomes\n"
        "╔═══╤═══╤═══╦═══╤═══╤═══╦\n"
        "║   │ x │ x ║   │   │   ║\n"
        "╟───┼───┼───╫───┼───┼───╫\n"
        "║   │   │   ║ x │ x │ x ║\n"
        "╟───┼───┼───╫───┼───┼───╫\n"
        "║   │   │   ║   │   │   ║\n"
        "╠═══╪═══╪═══╬═══╪═══╪═══╬\n"
        "where x represents a possible location for a given value."
        modified = False
        
        for square in self.squares:
            for possible in utils.SUDOKU_VALUES:
                cells = square.getAllCellsWithPossible(possible)
                if utils.allEqual(*cells, key=lambda cell: square.coordinatesOf(cell)[0]):
                    #All in same row
                    row = cells[0].row
                    for c in row:
                        if c not in square.cells:
                            oldP=c.possible[:]
                            c.removePossible(possible)
                            if c.possible != oldP:
                                modified = True
                            
                elif utils.allEqual(*cells, key=lambda cell: square.coordinatesOf(cell)[1]):
                    #All in same column
                    col = cells[0].column
                    for c in col:
                        if c not in square.cells:
                            oldP=c.possible
                            c.removePossible(possible)
                            if c.possible != oldP:
                                modified = True
        return modified
    
    
    def searchForExclusiveBlocks(self):
        "If in any cell there are x different values which can "
        "go in any of x different cells, removes all other values "
        "from those cells. For example,\n"
        "╔════════════════╤════════════════╤════════════════╦\n"
        "║ [a, b, c, ...] │ [a, b, c, ...] │      [...]     ║\n"
        "╟────────────────┼────────────────┼────────────────╫\n"
        "║      [...]     │      [...]     │      [...]     ║\n"
        "╟────────────────┼────────────────┼────────────────╫\n"
        "║      [...]     │      [...]     │ [a, b, c, ...] ║\n"
        "╠════════════════╪════════════════╪════════════════╬\n"
        "becomes\n"
        "╔═══════════╤═══════════╤═══════════╦\n"
        "║ [a, b, c] │ [a, b, c] │   [...]   ║\n"
        "╟───────────┼───────────┼───────────╫\n"
        "║   [...]   │   [...]   │   [...]   ║\n"
        "╟───────────┼───────────┼───────────╫\n"
        "║   [...]   │   [...]   │ [a, b, c] ║\n"
        "╠═══════════╪═══════════╪═══════════╬\n"
        "where a, b, and c are possible values and '...' represents "
        "any number of values besides those three."
        modified = False
        for house in self.iterHouses():
            mapping={}
            
            for value in utils.SUDOKU_VALUES:
                cells = house.getAllCellsWithPossible(value)
                cells = tuple(house.coordinatesOf(cell) for cell in cells)
                if cells in mapping:
                    mapping[cells].append(value)
                else:
                    mapping[cells] = [value]
            
            for cells, values in mapping.items():
                if len(cells) == len(values):
                    #Eligible
                    cells = [house.cellAt(coords) for coords in cells]
                    for cell in cells:
                        oldP = cell.possible[:]
                        for v in utils.SUDOKU_VALUES:
                            if v not in values:
                                cell.removePossible(v)
                                if cell.possible != oldP:
                                    modified = True
        return modified
    
    
    def searchForNakedGroups(self):
        "If there are x cells in a house which all contain the "
        "same x possibilities and only those x possibilities, "
        "then those possibilities can be excluded from all other "
        "cells in the house. For example,\n"
        "╔═════════════╤══════════╤═════════════╦\n"
        "║    [a, b]   │  [a, b]  │    [...]    ║\n"
        "╟─────────────┼──────────┼─────────────╫\n"
        "║   [a, ...]  │ [a, ...] │   [b, ...]  ║\n"
        "╟─────────────┼──────────┼─────────────╫\n"
        "║ [a, b, ...] │ [b, ...] │ [a, b, ...] ║\n"
        "╠═════════════╪══════════╪═════════════╬\n"
        "becomes,\n"
        "╔════════╤════════╤═══════╦\n"
        "║ [a, b] │ [a, b] │ [...] ║\n"
        "╟────────┼────────────────╫\n"
        "║  [...] │  [...] │ [...] ║\n"
        "╟────────┼────────┼───────╫\n"
        "║  [...] │  [...] │ [...] ║\n"
        "╠════════╪════════╪═══════╬\n"
        "where a and b are possible values and '...' represents "
        "any values besides those two."
        modified = False
        
        for house in self.iterHouses():
            mapping = {}
            for cell in house:
                p = tuple(cell.possible)
                if p in mapping:
                    mapping[p].append(cell)
                else:
                    mapping[p] = [cell]
            
            for possible, cells in mapping.items():
                if len(possible) == len(cells):
                    #Eligible
                    for cell in house:
                        oldP = cell.possible[:]
                        if cell not in cells:
                            for value in possible:
                                cell.removePossible(value)
                            if cell.possible != oldP:
                                modified = True
            
            return modified
                        
                      
    
    
    def solve(self, allowBruteForce=False):
        self.eliminatePossibilities()
        while any((
            self.searchForSinglePossibilities(),
            self.searchForExclusivePossibilities(),
            self.searchForAllAligned(),
            self.searchForExclusiveBlocks(),
#            self.searchForNakedGroups(), #Causes problems
            )): pass
        
            
        if self.isSolved():
            ok, problemCell = self.check()
            if ok:
                return True
            else:
                raise SudokuError("Invalid Solution", self, problemCell)
        else:
            if allowBruteForce:
                bruteForced = self.bruteForceAttack()
                if bruteForced is not None:
                    self.update(bruteForced)
                    return True
                    
            return False
    
    
    def bruteForceAttack(self, recursive=True):
        for cell in self.iterCells():
            for possible in cell.possible:
                copy = self.copy()
                copyCell = copy.cellAt(self.coordinatesOf(cell))
                copyCell.setValue(possible)
                try:
                    success = copy.solve(allowBruteForce=recursive)
                except SudokuError:
                    continue #Try the next possibility
                else:
                    if success:
                        return copy
    
    
More_Algorithms_To_Try = """
>>> If there is a pair of cells in a house which alone can contain 
a certain value, try each of them and see if it leads to a SuDokuError.
If so, remove that possibility.

>>> If there are x cells in a house which each have the same x number
of possibilities, those possibilities can be safely excluded from all
other cells in the house.
"""
            
        
 
PUZZLE_FORMAT_STRING="""\
╔═══╤═══╤═══╦═══╤═══╤═══╦═══╤═══╤═══╗
║ x │ x │ x ║ x │ x │ x ║ x │ x │ x ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║ x │ x │ x ║ x │ x │ x ║ x │ x │ x ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║ x │ x │ x ║ x │ x │ x ║ x │ x │ x ║
╠═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣
║ x │ x │ x ║ x │ x │ x ║ x │ x │ x ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║ x │ x │ x ║ x │ x │ x ║ x │ x │ x ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║ x │ x │ x ║ x │ x │ x ║ x │ x │ x ║
╠═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣
║ x │ x │ x ║ x │ x │ x ║ x │ x │ x ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║ x │ x │ x ║ x │ x │ x ║ x │ x │ x ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║ x │ x │ x ║ x │ x │ x ║ x │ x │ x ║
╚═══╧═══╧═══╩═══╧═══╧═══╩═══╧═══╧═══╝""".replace('x', "{}")

#sudokuGrid=Grid((DOUBLE, SINGLE, SINGLE, DOUBLE, SINGLE, SINGLE, DOUBLE, SINGLE, SINGLE, DOUBLE),
#                (DOUBLE, SINGLE, SINGLE, DOUBLE, SINGLE, SINGLE, DOUBLE, SINGLE, SINGLE, DOUBLE))
def main(puzDict, toDo=None, negFilter=[]):
    if toDo is None:
        toDo = puzDict.keys()
    total=0
    successes=0
    for puz in toDo:
        if puz in negFilter:
            continue
        total+=1
        print("Puzzle Name:", puz)
        puz=Puzzle(puzDict[puz])
        print("Initial Puzzle:")
        print(puz)
        print()
        print("Solving...", end="\t")
        sys.stdout.flush()
        success=puz.solve(allowBruteForce=True)
        if success:
            print("Success!")
            successes+=1
        else:
            print("Failure")
            
        print("Final Puzzle:")
        print(puz)
        if not success:
            print("Open Cells:")
            for cell in puz.iterCells(skipFullCells = True):
                print("\t> Cell {}: {}".format(puz.coordinatesOf(cell), cell.possible))
        print()
        print("-"*100)
        print()
    
    print("{} out of {} success rate.".format(successes, total))


if __name__ == "__main__":
    main(puzzles.puzzles, negFilter=["Blank", "Already Solved"])#, "Brute Force Prevails"])#, "Evil 7,360,298,562"])