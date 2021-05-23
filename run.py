#! /usr/bin/python3
"""
Example Usage:

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

Run `python ./run.py puzzle.txt` to see the solved puzzle. The puzzle input format is flexible. Any spaces or 
box-drawing characters (│║─═┼╬╪╫╔╗╚╝) are ignored. Beyond that, any non-numeric character can stand in for a 
blank in the puzzle grid. 

You can also input your puzzle directly via the command line. Run `./run.py` in the terminal, then type out the 
puzzle string. Press Ctrl+D on your keyboard when finished to see the solution.
"""

import sys
import sudoku
import fileinput

def solve_lines(puzzle_lines):
    solver = sudoku.Solver(sudoku.ClassicContext())
    try:
        puzzle = sudoku.Puzzle.parse('\n'.join(puzzle_lines))
    except Exception as err:
        print('Error reading puzzle:', err)
        return
    try:
        solution = solver.solve(puzzle)
        solved = solution.success
    except sudoku.SudokuError as err:
        print(err)
        solved = False
    finally:
        print('Solved!' if solved else 'Not solved...')
        print(puzzle if solved else puzzle.debug_string)

with fileinput.input() as puzzle_file:
    puzzle_lines = []
    for line in puzzle_file:
        if fileinput.isfirstline():
            # We've started a new file
            if puzzle_lines:
                solve_lines(puzzle_lines)
                puzzle_lines = []
        puzzle_lines.append(line)
    solve_lines(puzzle_lines)