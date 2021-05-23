from ..exception import SudokuError

class Cell:
    "One cell of the puzzle"
    variant_context = None


    def __init__(self, value=None, possible=None, puzzle=None, coords=None):
        if self.variant_context is None:
            if puzzle is not None and puzzle.variant_context is not None:
                self.variant_context = puzzle.variant_context
            else:
                raise NotImplementedError(
                    "Puzzle cannot be created without a variant context. Either "
                    "pass the context to the constructor, or create the puzzle "
                    "from within the context")
        self._value = value
        self._puzzle = puzzle
        self._coords = coords

        if self._value is None:
            self.possible = set(possible or range(1, 10))
        else:
            self.possible=set()

        self._features = {}
    

    def __getattr__(self, name):
        try:
            features = object.__getattribute__(self, '_features')
            if name in features:
                return features[name]
        except AttributeError:
            pass # _features is not yet defined
        raise AttributeError(f"No object property or cell feature '{name}'")
    

    def __setattr__(self, name, value):
        try:
            is_feature = name in object.__getattribute__(self, '_features')
        except AttributeError:
            # The features dict hasn't even been set yet. (We are proably setting it right now)
            is_feature = False
        if is_feature:
            raise AttributeError('Cell features are read-only')
        super().__setattr__(name, value)

    
    

    @property
    def coords(self):
        if not self._coords and self._puzzle:
            self._coords = self._puzzle.index(self)
        return self._coords
    

    @property
    def puzzle(self):
        return self._puzzle
    

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
        if self._coords or self._puzzle:
            return "Cell(value={}, possible={}) @ {}".format(repr(self._value), repr(self.possible), self.coords)
        else:
            return "Cell(value={}, possible={})".format(repr(self._value), repr(self.possible))
    
    
    def remove_possible(self, *values):
        "Safely removes value from cell.possible"
        self.possible.difference_update(values)
        if not self.possible and not self.value:
            raise SudokuError('Cell has no possible values, {} removed'.format(values), self.puzzle, self)
    

    def limit_possible(self, *values):
        """
        Limit cell possibilities to only the given values
        
        This will only remove possibilities, never add them.
        """
        self.possible.intersection_update(values)
    

    def has_possible(self, value, true_on_actual_value=False):
        return value in self.possible or (true_on_actual_value and value == self.value)
    

    @property
    def value_valid(self):
        "Checks to see if cell.value is valid"
        return self.value in range(1, 10)
    
    
    @property
    def value(self):
        return self._value
    

    @value.setter
    def value(self, value):
        "Sets the value, and clears the possible set"
        self._value = value
        self.possible.clear()
    

    @property
    def houses(self):
        h=[]  
        if self.row: h.append(self.row)
        if self.column: h.append(self.column)
        if self.square: h.append(self.square)
        return h