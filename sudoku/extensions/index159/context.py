from .pointer import PointerHouse
from ...variant_context import VariantContext, HybridContext, ClassicContext
from .algorithms import *

class Index159Context(VariantContext):
    def get_algorithms(self, description):
        #TODO actually use the description to filter algorithms
        return [
            apply_pointers_forward,
            apply_pointers_backward,
            apply_pointer_possibilities_forward,
            apply_pointer_possibilities_backward
        ]
    
    def init_features(self, puzzle, feature_map):
        pointer_houses = []
        for pointer_value in (1, 5, 9):
            pointer_houses.append(PointerHouse(
                puzzle.columns[pointer_value - 1], # convert 1-index to 0-index
                puzzle.rows,
                pointer_value
            ))
        puzzle._features['pointer_houses'] = pointer_houses
    
    def check_puzzle(self, puzzle):
        for pointer_house in puzzle.pointer_houses:
            for pointer_cell, indexed_house in pointer_house.iter_pointers():
                if pointer_cell.is_full and indexed_house[pointer_cell.value - 1].value != pointer_house.value:
                    return False, indexed_house[pointer_cell.value - 1]
        return True, None


class Classic159Context(HybridContext): 
    def __init__(self):
        super().__init__(ClassicContext(), Index159Context())