class House:
    "The base class for columns, rows, and squares"
    def __init__(self, *cells):
        if not len(cells) == 9:
            raise ValueError("Each row, column, and square must have exactly nine cells, received {} of {}: [{}]".format(
                type(self).__name__.lower(),
                len(cells),
                ', '.join(map(str, cells))
            ))
        self.cells=cells
    
    
    def __contains__(self, value):
        for cell in self.cells:
            if cell.value == value:
                return True
        return False
    
    
    def __iter__(self):
        return iter(self.cells)
    
    
    def __getitem__(self, index):
        return self.cells[index]
    
    
    def index(self, cell):
        return self.cells.index(cell)

    
    def eliminate_possible(self, value):
        "Calls cell.remove_possible(value) for every child cell."
        for cell in self.cells:
            cell.remove_possible(value)
    
    
    def get_cells_with_possible(self, value):
        "Returns a list of all cells with value in cell.possible, skipping full cells."
        r=[]
        for cell in self.cells:
            if cell.is_open and value in cell.possible:
                r.append(cell)
        return r
    


class Square(House):
    "One 9x9 square of the puzzle"
    def __init__(self, *cells):
        super().__init__(*cells)
        for cell in self.cells:
            cell.square=self
    
    
    def index(self, cell):
        "Finds the coordinates (relative to the square) of the cell"
        index=self.cells.index(cell)
        if index < 3:
            return 0, index
        elif index < 6:
            return 1, index-3
        else:
            return 2, index-6
    
    
    def __getitem__(self, coords):
        "Returns the cell at the given coordinates (relative to the square)"
        row, column = coords
        return self.cells[column+(row*3)]



class Row(House):
    "One row in the puzzle"
    def __init__(self, *cells):
        House.__init__(self, *cells)
        for cell in self.cells:
            cell.row=self



class Column(House):
    "One column in the puzzle"
    def __init__(self, *cells):
        House.__init__(self, *cells)
        for cell in self.cells:
            cell.column=self


