from .utils import calculate_cage_combinations, calculate_cage_possibilities

def eliminate_cage_possibilities(*cages):
    for cage in cages:
        possibilities = calculate_cage_possibilities(cage.sum, cage.cell_count)
        for cell in cage:
            cell.limit_possible(possibilities)


def evaluate_permutations(*cages):
    for cage in cages:
        for index, permutation in reversed(enumerate(cage.permutations)):
            for cell, value in zip(cage.cells, permutation):
                if not cell.has_possible(value, True):
                    cage.permutations.pop(index)


def apply_permutations(*cages):
    for cage in cages:
        if cage.permutations:
            for cell_possibility_sets in zip(*cage.permutations):
                for cell, possibility_set in zip(cage.cells, cell_possibility_sets):
                    cell.limit_possible(possibility_set)


# TODO 45 rule: any row, column, or square can be thought of as a cage with 9 cells and a 
# sum of 45. Intersections between the killer cages and the ordinary sudoku houses can 
# subdivide cages to provide additional insights. For example, if some number of cages
# are all contained in the same house, then the combined total of all those cages can
# be subtracted from 45 to get the sum of a new imaginary cage which includes all the 
# cells in the house that were not in one of those original cages. A cage that straddles
# the boundary between two house can also provide a similar insight so long as all the 
# other cages in the house exactly fill the house.
#
# These conditions are pretty easy for a human to see, but I'm still working out how to
# make a computer do them.