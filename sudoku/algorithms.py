from .utils import all_equal
import math

__all__ = [
    'eliminate_possibilities',
    'find_naked_singles',
    'find_hidden_singles',
    'find_locked_candidates_squares',
    'find_locked_candidates_rows_columns',
    'find_hidden_multiples',
    'find_naked_multiples',
]

def eliminate_possibilities(*cells):
    """
    Eliminates any possibilities from cells in which are not actually
    possible given the rules of sudoku. 

    This performs basic elimination based on filled cells in the house,
    without applying more complex logic
    """
    for cell in cells:
        if cell.is_full:
            cell.square.eliminate_possible(cell.value)
            cell.row.eliminate_possible(cell.value)
            cell.column.eliminate_possible(cell.value)
                    
    
    
def find_naked_singles(*cells):
    """
    If there is only one remaining possibility in any cells, sets those 
    cells to their only possible value

    Returns True if the algorithm modified any cells
    """
    modified = False
    
    for cell in cells:
        if len(cell.possible) == 1:
            cell.value = cell.possible[0]
            modified = True
            
    return modified
    
    
def find_hidden_singles(*houses):
    """
    Checks to see if there are any cells which are the only possible 
    location in their row, column, or square which can contain a certain 
    value. If so, sets those cells to that exclusive value.

    Returns True if the algorithm modified any cells
    """
    modified = False
    
    for house in houses:
        for value in range(1, 10):
            cells = house.get_cells_with_possible(value) #Note: Skips full cells
            if len(cells) == 1: #i.e. There is only one cell in house that can be value
                cells[0].value = value
                modified = True
    return modified
    
    
def find_locked_candidates_squares(*squares):
    """
    Searches all squares to see if all the possible cells for a value are in a 
    line. If so, removes that value from all other cells in that row/column. 

    For example,
    ```
    ╔═══╤═══╤═══╦═══╤═══╤═══╦
    ║   │ x │ x ║ x │ x │ x ║
    ╟───┼───┼───╫───┼───┼───╫
    ║   │   │   ║ x │ x │ x ║
    ╟───┼───┼───╫───┼───┼───╫
    ║   │   │   ║   │   │   ║
    ╠═══╪═══╪═══╬═══╪═══╪═══╬
    ```
    becomes
    ```
    ╔═══╤═══╤═══╦═══╤═══╤═══╦
    ║   │ x │ x ║   │   │   ║
    ╟───┼───┼───╫───┼───┼───╫
    ║   │   │   ║ x │ x │ x ║
    ╟───┼───┼───╫───┼───┼───╫
    ║   │   │   ║   │   │   ║
    ╠═══╪═══╪═══╬═══╪═══╪═══╬
    ```
    where x represents a possible location for a given value.

    Returns True if the algorithm changed any cells
    """
    modified = False
    
    for square in squares:
        for possible in range(1, 10):
            cells = square.get_cells_with_possible(possible)
            if all_equal(*cells, key=lambda cell: square.index(cell)[0]):
                #All in same row
                house = cells[0].row      
            elif all_equal(*cells, key=lambda cell: square.index(cell)[1]):
                #All in same column
                house = cells[0].column
            else:
                continue
            for cell in house:
                if cell not in square.cells:
                    old_possible=cell.possible[:]
                    cell.remove_possible(possible)
                    if cell.possible != old_possible:
                        modified = True
    return modified


def find_locked_candidates_rows_columns(*rows_and_columns):
    """
    If all the possibilities for a value in any given row or column
    are also all in the same square, no other cells in that square
    can be the given value.

    For example,
    ```
    ╔═══╤═══╤═══╦═══╤═══╤═══╦═══╤═══╤═══╗
    ║   │   │   ║ x │   │ x ║   │   │   ║
    ╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
    ║   │   │   ║   │ x │ x ║   │ x │ x ║
    ╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
    ║   │   │   ║   │   │   ║   │   │   ║
    ╠═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣
    ```
    becomes
    ```
    ╔═══╤═══╤═══╦═══╤═══╤═══╦═══╤═══╤═══╗
    ║   │   │   ║ x │   │ x ║   │   │   ║
    ╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
    ║   │   │   ║   │   │   ║   │ x │ x ║
    ╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
    ║   │   │   ║   │   │   ║   │   │   ║
    ╠═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣
    ```
    where x represents a possible location for a given value.

    Returns True if the algorithm modified any cells.
    """
    modified = False
    for house in rows_and_columns:
        for possible in range(1, 10):
            cells = house.get_cells_with_possible(possible)
            if len(cells) < 2: continue
            squares_seen = set()
            for cell in cells:
                index = house.index(cell)
                squares_seen.add(math.floor(index/3))
            if len(squares_seen) == 1:
                # All values are in the same square
                for cell in cells[0].square:
                    if cell not in cells:
                        old_possible=cell.possible[:]
                        cell.remove_possible(possible)
                        if cell.possible != old_possible:
                            modified = True
    return modified


def find_hidden_multiples(*houses):
    """
    If in any house there are x different values which can only 
    go in any of  x different cells, removes all other values 
    from those cells. 
    
    For example,
    ```
    ╔════════════════╤════════════════╤════════════════╦
    ║ [a, b, c, ...] │ [a, b, c, ...] │      [...]     ║
    ╟────────────────┼────────────────┼────────────────╫
    ║      [...]     │      [...]     │      [...]     ║
    ╟────────────────┼────────────────┼────────────────╫
    ║      [...]     │      [...]     │ [a, b, c, ...] ║
    ╠════════════════╪════════════════╪════════════════╬
    ```
    becomes
    ```
    ╔═══════════╤═══════════╤═══════════╦
    ║ [a, b, c] │ [a, b, c] │   [...]   ║
    ╟───────────┼───────────┼───────────╫
    ║   [...]   │   [...]   │   [...]   ║
    ╟───────────┼───────────┼───────────╫
    ║   [...]   │   [...]   │ [a, b, c] ║
    ╠═══════════╪═══════════╪═══════════╬
    ```
    where a, b, and c are possible values and '...' represents any number 
    of values besides those three.

    Returns True if the algorithm changed any cells
    """
    modified = False
    for house in houses:
        mapping={}
        
        for value in range(1, 10):
            cells = house.get_cells_with_possible(value)
            indices = tuple(house.index(cell) for cell in cells)
            if indices in mapping:
                mapping[indices].append(value)
            else:
                mapping[indices] = [value]
        
        for indices, values in mapping.items():
            if len(indices) == len(values):
                #Eligible
                cells = [house[index] for index in indices]
                for cell in cells:
                    old_possible = cell.possible[:]
                    for v in range(1, 10):
                        if v not in values:
                            cell.remove_possible(v)
                            if cell.possible != old_possible:
                                modified = True
    return modified


def find_naked_multiples(*houses):
    """
    If there are x cells in a house which all contain the same x 
    possibilities and *only* those x possibilities, then those 
    possibilities can be removed from all other cells in the house. 
    
    For example,
    ```
    ╔═════════════╤══════════╤═════════════╦
    ║    [a, b]   │  [a, b]  │    [...]    ║
    ╟─────────────┼──────────┼─────────────╫
    ║   [a, ...]  │ [a, ...] │   [b, ...]  ║
    ╟─────────────┼──────────┼─────────────╫
    ║ [a, b, ...] │ [b, ...] │ [a, b, ...] ║
    ╠═════════════╪══════════╪═════════════╬
    ```
    becomes,
    ```
    ╔════════╤════════╤═══════╦
    ║ [a, b] │ [a, b] │ [...] ║
    ╟────────┼────────────────╫
    ║  [...] │  [...] │ [...] ║
    ╟────────┼────────┼───────╫
    ║  [...] │  [...] │ [...] ║
    ╠════════╪════════╪═══════╬
    ```
    where a and b are possible values and '...' represents 
    any values besides those two.

    Returns True if the algorithm changed any cells
    """
    modified = False
    
    for house in houses:
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
                    old_possible = cell.possible[:]
                    if cell not in cells:
                        for value in possible:
                            cell.remove_possible(value)
                        if cell.possible != old_possible:
                            modified = True
        
        return modified