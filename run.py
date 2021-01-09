#! /usr/bin/python3

import sys
import sudoku
import fileinput

def solve_lines(puzzle_lines):
    try:
       puzzle = sudoku.Puzzle.parse('\n'.join(puzzle_lines))
    except Exception as err:
        print('Error reading puzzle:', err)
        return
    try:
        solved = sudoku.solve(puzzle)
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