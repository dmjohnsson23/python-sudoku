from .algorithms import *

class VariantContext:
    """
    This class is used to implement the plugin system. It tracks which algorithms are
    appropriate for the solver to use, and provides functionality to check that solution 
    to the puzzle
    """
    def get_algorithms(self, description):
        raise NotImplementedError("The variant context must either be a subclass which implements this method, or a VariantComposition which combines variants")
    
    def check(self, puzzle):
        raise NotImplementedError("The variant context must either be a subclass which implements this method, or a VariantComposition which combines variants")


class ClassicContext(VariantContext):
    # TODO I want to generalize this a lot more and allow composing hybrid contexts by 
    # combining constraints from different variants. This is a placeholder to allow 
    # testing things until I can code all that functionality

    def get_algorithms(self, description):
        return [
            eliminate_possibilities,
            find_naked_singles,
            find_hidden_singles,
            find_locked_candidates_squares,
            find_locked_candidates_rows_columns,
            find_hidden_multiples,
            find_naked_multiples,
            find_x_wing,
        ]
    
    def check(self, puzzle):
        return puzzle.check()