from .algorithms import *
from .exception import SudokuError
    
def solve(puzzle, brute_force_levels = 1):
    """
    Try to solve the given puzzle. Returns True if a valid solution was 
    found.

    The puzzle will be modified in-place with the new solution
    """
    eliminate_possibilities(*puzzle.iter_cells())
    while any((
        find_single_possibilities(*puzzle.iter_cells(skip_full_cells=True)),
        find_exclusive_possibilities(*puzzle.iter_houses()),
        find_aligned_in_square(*puzzle.squares),
        find_aligned_in_row_or_column(*puzzle.rows, *puzzle.columns),
        find_exclusive_groups(*puzzle.iter_houses()),
        find_constrained_groups(*puzzle.iter_houses()),
        )): pass
    
        
    if puzzle.is_solved:
        ok, problem_cell = puzzle.check()
        if ok:
            return True
        else:
            raise SudokuError("Invalid Solution", puzzle, problem_cell)
    else:
        if brute_force_levels:
            brute_forced = brute_force_attack(puzzle, brute_force_levels)
            if brute_forced is not None:
                puzzle.update(brute_forced)
                return True
                
        return False


def brute_force_attack(puzzle, recurse_level):
    """
    Try to brute force a solution. This will loop through each possibility 
    of each empty cell, and call solve() on a puzzle with that cell set
    to that value.

    Use the `recurse_level` parameter to control how many times the 
    solver will be allowed to recursively attempt a brute force. Higher
    values have better chances of finding solutions, lower values are
    more performant. There is probably little to gain from more than
    a couple recursion layers however.

    Return a solved copy of the puzzle if a solution is found.
    """
    for cell in puzzle.iter_cells():
        for possible in cell.possible:
            copy = puzzle.copy()
            copy_cell = copy[puzzle.index(cell)]
            copy_cell.value = possible
            try:
                success = solve(copy, brute_force_levels = (recurse_level-1) if recurse_level else 0)
            except SudokuError:
                continue #Try the next possibility
            else:
                if success:
                    return copy

 