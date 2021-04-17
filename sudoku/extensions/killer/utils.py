from functools import lru_cache

@lru_cache()
def calculate_cage_combinations(cage_sum, cell_count):
    """
    Calculates all possible sets of unique digits that could work for a cage with the given
    sum and cell count.

    This function uses an lru cache rather than doing combinations afresh every time,
    and also has optimizations in place to quickly cut out the upper and lower bounds of
    the possible combinations, so performance is actually pretty good
    """
    return tuple(frozenset(perm) for perm in _calculate_cage_combinations(cage_sum, cell_count))


def _calculate_cage_combinations(cage_sum, cell_count, digits = [1, 2, 3, 4, 5, 6, 7, 8, 9]):
    if len(digits) < cell_count:
        return
    max_sum = sum(digits[-cell_count:])
    min_sum = sum(digits[:cell_count])
    if cage_sum < min_sum or cage_sum > max_sum:
        return
    if cell_count == 1:
        if cage_sum in digits:
            yield set((cage_sum,))
        else:
            return

    for digit in digits:
        partial_sum = cage_sum - digit
        if partial_sum <= 0:
            break
        remaining_digits = [d for d in digits if d > digit]
        if not remaining_digits:
            break
        for combination in _calculate_cage_combinations(partial_sum, cell_count-1, remaining_digits):
            combination.add(digit)
            if len(combination) == cell_count:
                yield combination


def calculate_cage_possibilities(cage_sum, cell_count):
    possibilities = set()
    for combination in calculate_cage_combinations(cage_sum, cell_count):
        possibilities = possibilities.union(combination)
    return frozenset(possibilities)