class Algorithm:
    """
    A representation of an algorithm that can be applied to a sudoku puzzle or a variant thereof
    """
    registry = {}

    def __init__(self, name, difficulty):
        self.name = name
        self.difficulty = difficulty
        if name in Algorithm.registry: 
            raise ValueError(f'Algorithm names must be unique; "{name}" has already been registered')
        Algorithm.registry[name] = self

    def run(self, puzzle, stepper):
        """
        Run the algorithm, recording any applicable steps in the stepper.

        Returns True if the algorithm modified the puzzle, False otherwise
        """
        raise NotImplementedError('Algorithm base class should be extended, or use the algorithm decorator')



def algorithm(difficulty, multistep=False):
    """
    Decorator to use to convert a basic generator (yielding tuples of StepUnit objects) into an Algorithm class

    Algorithms will be run in order of difficulty. Negative difficulty values indicate that the algorithm is used
    for initial setup only, and are only run once per solve. Zero or positive difficulty algorithms will be run 
    repeatedly in the solver loop. Zero difficulty algorithms are considered as rudimentary/common sense algorithms,
    so you might choose to consider them as extensions of previous steps when replaying a solve to users.

    If multistep is False (the default) then the algorithm will stop at the first yield and re-run all of the
    lower-difficulty algorithms before running this algorithm again. It it is True, the algorithm will run all the
    way through before re-running the basic algorithms, and is allowed to make multi-step modifications to the puzzle.
    Not that, regardless of whether the algorithm is single-step or multi-step, you should use `yield` instead of
    `return`. The `yield` acts like a `return` in this context, unless the value yielded is None.
    """
    def decorator(generator_function):
        class AlgorithmFromDecorator(Algorithm):
            def run(self, puzzle, stepper):
                modified = False
                for step_units in generator_function(puzzle):
                    if step_units is None:
                        continue
                    stepper.record_step(self.name, step_units)
                    modified = True
                    if not multistep:
                        break
                return modified
        AlgorithmFromDecorator.__doc__ = generator_function.__doc__
        AlgorithmFromDecorator.__name__ = generator_function.__name__
        return AlgorithmFromDecorator(generator_function.__name__, difficulty)
    return decorator


algorithm(-99)
def start():
    """
    This is a dummy algorithm used by the stepper to indicate the initial state of the puzzle. 
    It never does anything. This is just a placeholder to reserve the name in the algorithm
    registry.
    """
    pass