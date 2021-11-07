from .algorithms import *
from .model import *

class VariantContext:
    """
    This class is used to implement the plugin system. It tracks which algorithms are
    appropriate for the solver to use, and provides functionality to check that solution 
    to the puzzle
    """
    def __new__(cls):
        # Make the class a singleton
        if not '_instance' in cls.__dict__:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        class ContextualizedCell(Cell):
            variant_context = self
        class ContextualizedPuzzle(Puzzle):
            variant_context = self
        self.Cell = ContextualizedCell
        self.Puzzle = ContextualizedPuzzle

    def get_algorithms(self, description):
        """
        Get the ordered list of algorithms to use for solving the puzzle, optionally filtering based on the description parameter
        """
        raise NotImplementedError("The variant context must either be a subclass which implements this method, or a HybridContext which combines variants")
    
    def init_features(self, puzzle, feature_map):
        """
        Initialize the features of the puzzle (houses, regions, cages, and other clues)
        """
        raise NotImplementedError("The variant context must either be a subclass which implements this method, or a HybridContext which combines variants")

    def check_puzzle(self, puzzle):
        """
        Verify that the puzzle, in it's current state, does not violate any constraints for this context

        Should return a tuple (False, Cell) if there is a problem, indicating which cell the violation was found in.
        Otherwise, return (True, None)
        """
        raise NotImplementedError("The variant context must either be a subclass which implements this method, or a HybridContext which combines variants")


class ClassicContext(VariantContext):
    # TODO I want to generalize this a lot more and allow composing hybrid contexts by 
    # combining constraints from different variants. This is a placeholder to allow 
    # testing things until I can code all that functionality

    def get_algorithms(self, description):
        #TODO actually use the description to filter algorithms
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
    
    def init_features(self, puzzle, feature_map):
        rows=[Row(*(cell for cell in row)) for row in puzzle.cells]
        columns=[Column(*(cell for cell in column)) for column in zip(*puzzle.cells)]
        squares=[]
        for Y in range(0, 9, 3):
            for X in range(0, 9, 3):
                square=[]
                for y in range(3):
                    for x in range(3):
                        square.append(puzzle.cells[Y+y][X+x])
                squares.append(Square(*square))
        puzzle._features['rows'] = rows
        puzzle._features['columns'] = columns
        puzzle._features['squares'] = squares

        for row in rows:
            for cell in row:
                cell._features['row'] = row
        for column in columns:
            for cell in column:
                cell._features['column'] = column
        for square in squares:
            for cell in square:
                cell._features['square'] = square
    
    def check_puzzle(self, puzzle):
        # TODO move the check logic from the puzzle class to here
        return puzzle.check()


class HybridContext(VariantContext):
    def __new__(cls, *args, **kwargs):
        # Revert back to a non-singleton, only for hybrids
        return object.__new__(cls, *args, **kwargs)
    
    def __init__(self, *contexts):
        self._subcontexts = contexts
        super().__init__()
    
    def get_algorithms(self, description):
        algs = set()
        for context in self._subcontexts:
            algs = algs.union(context.get_algorithms(description))
        return sorted(algs, key=lambda alg: alg.difficulty)
    
    def init_features(self, puzzle, feature_map):
        for context in self._subcontexts:
            context.init_features(puzzle, feature_map)
    

    def check_puzzle(self, puzzle):
        for context in self._subcontexts:
            okay, cell = context.check_puzzle(puzzle)
            if not okay:
                return False, cell
        return True, None