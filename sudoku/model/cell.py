from ..exception import SudokuError

class Cell:
    "One cell of the puzzle"
    def __init__(self, value=None, possible=None, row=None, column=None, square=None, puzzle=None):
        self._value = value
        self.row = row
        self.column = column
        self.square = square
        self.puzzle = puzzle

        if self._value is None:
            self.possible = set(possible or range(1, 10))
        else:
            self.possible=set()
    

    @property
    def is_full(self):
        return self._value is not None
    

    @property
    def is_open(self):
        return self._value is None
    
    
    def __str__(self):
        if self.is_full:
            return str(self._value)
        else:
            return " "
    

    def __repr__(self):
        if self.puzzle:
            return "Cell(value={}, possible={}) @ {}".format(repr(self._value), repr(self.possible), self.puzzle.index(self))
        else:
            return "Cell(value={}, possible={})".format(repr(self._value), repr(self.possible))
    
    
    def remove_possible(self, value):
        "Safely removes value from cell.possible"
        if value in self.possible:
            self.possible.remove(value)
            if not self.possible and not self.value:
                raise SudokuError('Cell has no possible values, last value ({}) removed'.format(value), self.puzzle, self)
            if len(self.possible) == 1:
                self.value = self.possible.pop()
    

    def limit_possible(self, values):
        """
        Limit cell possibilities to only the given values
        
        This will only remove possibilities, never add them.
        """
        self.possible.intersection_update(set(values))
    

    def has_possible(self, value):
        return value in self.possible or value == self.value
    

    @property
    def value_valid(self):
        "Checks to see if cell.value is valid"
        return self.value in range(1, 10)
    
    
    @property
    def value(self):
        return self._value
    

    @value.setter
    def value(self, value):
        "Sets the value, and removes it from cell.possible for all cells in the same row, column, or square."
        self._value = value
        self.possible.clear()
        if self.row: self.row.eliminate_possible(value)
        if self.column: self.column.eliminate_possible(value)
        if self.square: self.square.eliminate_possible(value)
    

    @property
    def houses(self):
        h=[]  
        if self.row: h.append(self.row)
        if self.column: h.append(self.column)
        if self.square: h.append(self.square)
        return h