from .house import Row, Column, Square
from .cell import Cell
import itertools
from copy import deepcopy

class Puzzle:
    "The entire puzzle"
    
    def __init__(self, puzzle_array):
        self.rows=[Row(*(Cell(cell, puzzle=self) for cell in row)) for row in puzzle_array]
        self.columns=[Column(*(cell for cell in column)) for column in zip(*self.rows)]
        if len(self.rows) != 9 or len(self.columns) != 9:
            raise ValueError('A sudoku puzzle must be a 9x9 grid')
        self.squares=[]
        for Y in range(0, 9, 3):
            for X in range(0, 9, 3):
                square=[]
                for y in range(3):
                    for x in range(3):
                        square.append(self[Y+y, X+x])
                self.squares.append(Square(*square))
    

    @classmethod
    def parse(cls, string):
        """
        Parse a puzzle string into a puzzle.

        Format should be like this:

        81__5_23_
        ___6___74
        5763____8
        ___4__721
        __8___4__
        142__5___
        4____6917
        62___7___
        _37_1__62
        """
        string = (string.strip()
            .replace('│', '')
            .replace('║', '')
            .replace('─', '')
            .replace('═', '')
            .replace('┼', '')
            .replace('╬', '')
            .replace('╪', '')
            .replace('╫', '')
            .replace('╔', '')
            .replace('╗', '')
            .replace('╚', '')
            .replace('╝', '')
            .replace(' ', '')
        )
        
        return cls(list(filter(
            lambda item: bool(item), # filter any blank lines out
            map(
                lambda row: list(map( # Convert numbers to ints, anything else to blanks (ignoring whitespace)
                    lambda cell: int(cell) if cell.isnumeric() else None, 
                    row.strip())), 
                string.splitlines())
            )))
    
    
    def iter_cells(self, skip_full_cells=False, skip_open_cells=False, central_call=None):
        """
        Iterates over all cells in the puzzle. 
        
        If `skip_full_cells` is True, skips any cell which already has a value in it. 
        
        If `central_call` is given, only iterates over cells in the same row, column, 
        or square as that cell (not including the central cell itself). 
        
        When `central_call` is given, cells are in no particular order. If `central_call` 
        is not given, cells are given in order from left to right, top to bottom.
        """
        if central_call is None:
            for row in self.rows:
                for cell in row:
                    if skip_full_cells and cell.is_full:
                        continue
                    if skip_open_cells and cell.is_open:
                        continue
                    yield cell
        else:
            cells=set(central_call.row.cells+central_call.column.cells+central_call.square.cells)
            cells.remove(central_call)
            for cell in cells:
                if skip_full_cells and cell.is_full:
                    continue
                if skip_open_cells and cell.is_open:
                    continue
                yield cell
    
    
    def iter_houses(self):
        "Iterates over all rows, columns, and squares"
        return itertools.chain(self.rows, self.columns, self.squares)
    
    
    def update(self, other):
        "For every filled cell in other, set that same cell in self to the value from other"
        for cell, other_cell in zip(self.iter_cells(), other.iter_cells()):
            if other_cell.is_full:
                cell.value = other_cell.value
    
    
    def index(self, cell):
        "Returns the global coordinates of the cell"
        return (self.rows.index(cell.row), cell.row.cells.index(cell))
    
    
    def __getitem__(self, coords):
        row, column = coords
        return self.rows[row][column]
    
    
    def copy(self):
        return deepcopy(self)
    
    
    def __str__(self):
        return PUZZLE_FORMAT_STRING.format(*(str(cell) for cell in self.iter_cells()))
    

    @property
    def debug_string(self):
        return "{}\n\nOpen Cells (row, col) -> [possible values]:\n{}".format(
                self,
                '\n'.join([
                    "\t> Cell {} -> {}".format(self.index(cell), cell.possible) 
                    for cell in self.iter_cells(skip_full_cells = True)])
            )
    
    
    @property
    def is_solved(self):
        "Returns True if all the cells in the puzzle are filled. "
        "Does not check if solution is valid. Use check for that."
        for cell in self.iter_cells():
            if cell.is_open:
                return False
        return True
    
    def check(self):
        "Checks to make sure all values in puzzle are acceptable."
        "Does not check if puzzle is actually solved. Use isSolved for that."
        for cell in self.iter_cells():
            if cell.is_open:
                if not 1 <= len(cell.possible) <= 9:
                    return False, cell
            
            else:
                if not cell.value_valid:
                    return False, cell
                
                for other_cell in self.iter_cells(central_call=cell):
                    if cell.value==other_cell.value:
                        return False, cell
        return True, None


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