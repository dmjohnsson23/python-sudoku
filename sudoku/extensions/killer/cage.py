from itertools import permutations
from .utils import calculate_cage_combinations

class Cage:
    def __init__(self, sum, *cells):
        self.sum = sum
        self.cells = cells
        self.permutations = permutations(calculate_cage_combinations(sum, len(cells)))
    
    @property
    def cell_count(self):
        return len(self.cells)
    

    def __iter__(self):
        return iter(self.cells)
    
    
    def __getitem__(self, index):
        return self.cells[index]
    
    
    def index(self, cell):
        return self.cells.index(cell)
