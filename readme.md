# Sudoku Solver

A library / command-line utility for solving sudoku puzzles.

I originally wrote this in 2013. I recently re-discovered it while going through old projects and decided to make some upgrades and improvements. It is now significantly improved from the older version, and is able to solve any puzzle I have thus far been able to find online. Let me know if you find a solvable puzzle it can't solve!

## Example Usage (Command Line)

Assuming you have a file named `puzzle.txt` with the following contents, located in the same folder as `run.py`:

```
+++9++7++
635++++++
9++5+83++
+6++++++3
423+++695
7++++++8+
++93+1++8
++++++912
++4++9+++
```

Run `./run.py puzzle.txt` to see the solved puzzle. The puzzle input format is flexible. Any spaces or box-drawing characters (│║─═┼╬╪╫╔╗╚╝) are ignored. Beyond that, any non-numeric character can stand in for a blank in the puzzle grid. 

You can also input your puzzle directly via the command line. Run `./run.py` in the terminal, then type out the puzzle string. Press Ctrl+D on your keyboard when finished to see the solution.

## Example Usage (As Python Library)

```python
import sudoku

# Load from an array...
_ = None # Just to make the puzzle format below easier to read
puzzle = sudoku.Puzzle( 
    [
            [3, 5, _,   _, _, _,    _, 2, _],
            [_, _, _,   9, 6, _,    7, _, _],
            [_, _, _,   _, _, _,    5, _, 9],
            
            [1, _, _,   _, _, 8,    4, _, _],
            [_, _, _,   3, 2, 4,    _, _, _],
            [_, _, 4,   1, _, _,    _, _, 2],
            
            [2, _, 1,   _, _, _,    _, _, _],
            [_, _, 8,   _, 4, 6,    _, _, _],
            [_, 7, _,   _, _, _,    _, 9, 5]
           ]
)

# .. or from a string
puzzle = sudoku.Puzzle.parse("""
35-----2-
---96-7--
------5-9
1----84--
---324---
--41----2
2-1------
--8-46---
-7-----95
""")

# Use algorithms and inspect the puzzle state
sudoku.algorithms.eliminate_possibilities(*puzzle.iter_cells())
puzzle[0, 1].value # 5
puzzle[0, 2].possible # [6, 7, 9]

# Use the solver to finish solving the puzzle
is_solved = sudoku.solve(puzzle) # True
puzzle[0, 2].value # 9

# Try the example puzzles too
# Note: not all the example puzzles are solvable
from sudoku.puzzles import puzzles
for puzzle_name, puzzle_array in puzzles:
    puzzle = sudoku.Puzzle(puzzle_array)
    print('Attempting puzzle:', puzzle_name)
    print(puzzle)
    is_solved = sudoku.solve(puzzle)
    print('Solved!' if is_solved else 'Not Solved...')
    print(puzzle)

```