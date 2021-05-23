# Sudoku Solver

A library for analyzing, solving, and creating sudoku puzzles.

This began as a basic solver for classic sudoku puzzles which I wrote in high school. After getting my bachelor's degree, I have decided to revisit the project and repurpose it as an extensible and general-purpose sudoku python library. This is a development library; the API will change. Probably a lot.

The purpose of this library it to be used in tools that aid in:

* Learning Sudoku techniques
* Getting hints for difficult puzzles
* Test-solving hand-crafted puzzles or looking for contradictions


## Road Map

I am currently working on refactoring the project and developing the plugin system that will allow it to support sudoku variants and variant-hybrids. 

Once the plugin system is in place, I will add a number of variants. Killer, chess, arrow, and thermo are the first priorities.

After at least several of the planned variants are finished, I think I might work on the ability of the library to generate puzzles. The generator would rely on the solver to test-solve puzzles, so we can only generate what we can solve. This might even be a separate project entirely: a second complementary library. My current focus however is exclusively on the solving aspect, not generation.

Eventually, I will try to add more advanced solving algorithms. The existing algorithms, at least for classic sudoku, can already solve all but the most devious of puzzles, so this is a low priority.


## Example Usage

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

# Use a stepper object to record solve steps taken on the puzzle
stepper = sudoku.Stepper(puzzle)

# Use algorithms and inspect the puzzle state...
sudoku.algorithms.eliminate_possibilities.run(puzzle, stepper)
puzzle[0, 1].value # 5
puzzle[0, 2].possible # set([6, 7, 9])

# ... or use the solver to run all preset algorithms repeatedly to solve the puzzle
is_solved = sudoku.solve(puzzle) # True
puzzle[0, 2].value # 9

# Try the example puzzles too
# Note: not all the example puzzles are solvable
from sudoku.test.puzzles import puzzles
for puzzle_name, puzzle_array in puzzles:
    puzzle = sudoku.Puzzle(puzzle_array)
    print('Attempting puzzle:', puzzle_name)
    print(puzzle)
    solution = sudoku.solve(puzzle)
    print('Solved!' if solution.success else 'Not Solved...')
    print(puzzle) # Note: The puzzle is solved in-place, you can use puzzle.copy() to keep the original state somewhere

```

## Goals / Non-Goals

* The library should be extensible: 
  * It should be easy to create plugins to support sudoku variants
  * It should allow mixing and matching variant plugins to create hybrid variants
* The library should produce meaningful output, which would be useful to show a human how the puzzle was solved
* The library should avoid using techniques that are to overly difficult for a human to spot or compute
* It should solve the puzzle logically, like a human would
* CPU and memory efficiency are not a focus at all, as this is often at odds with the previous points. The existing human-centric algorithms are more than preformat enough for the use case anyway.
* No graphical interface will be provided; this is intended as a back-end library that a GUI application would use as a dependency
* Command-line usage will remain limited, or possibly even removed, for the reasons listed above
* Although both are important, currently a greater focus will be placed on adding new variants over adding more advanced algorithms. This is mostly because novel rulesets with interesting logic are more interesting to me than extremely difficult puzzles; I'm not opposed to adding advanced techniques so long as they are not so advanced as to be un-spottable by a human.

## Extensions to (eventually) implement

#### Arrow Clues

Arrow clues indicate that any value place on the circle at the base of an arrow represents the sum of all digits along the arrow. Circles may encompass multiple cells to build multidigit sum clues.

#### Chess Move Clues

Chess sudoku introduces an additional constraint in the form of "chess move" constraints. For example, a digit may be excluded from appearing within a  knight's move, bishop's move, or kings move of another of the same digit.

#### Jigsaw Sudoku

Jigsaw replaces squares with irregularly-shaped 9-cell "jigsaw" regions.

#### Killer Sudoku

*A work-in-progress extension for this is in being developed mainly to inform the development of the extension system*

Killer sudoku introduces the concept of cage clues. Cages have arbitrary lengths and shapes. There is a sum clue written in the corner of the cage which all digits in the cage must add up to. Digits cannot repeat within a cage.

#### Kropki Dots

Also known as ratio dots and difference dots, Kropki dots sit between to cells and indicate the ratio or difference of the cells. Typically, a black dot indicates a ratio of 2:1 and a white dot indicates a difference of 1. However, some variants have different ratios and differences

#### Little Killer Clues

Shown outside the grid, little killer clues point along arbitrary diagonals somewhere in the grid, with a number indicating the sum of all digits on the diagonal. In contrast to regular killer sudoku, digits *are* allowed to repeat along little killer diagonals.

#### Odd/Even Parity Clues

Some variants, as an additional constraint, add parity clues. For example, a large gray circle to indicate a cell contains an odd digit, and a gray square in the cell to indicate it contains an even digit.

#### Sandwich Clues

Numbers written outside the grid tell the sum of all digits between the position of the 1 and the position of the 9 in that row or column. Variants might use different "crust" digits other than 1 and 9.

#### Thermometer Clues

Thermometer shapes are drawn in the grid to indicate that the value of digits must increase from the "bulb" side of the thermometer to the end. They do not have to increase sequentially, simply increase.

#### Windows, Diagonals, and Other Additional Houses

Some puzzles add additional regions to the grid, which must contain all nine digits once each just like the main houses (rows, columns, squares)

* Windows: 4 extra 3x3 squares in the middle of the grid
* Diagonals (Sudoku X): across either or both of the two main diagonals of the grid
* Relative Position RegionsL Each position within a square comines to form an additional region, e.g. if there is 9 in the top-right cell of a square, there cannot be a 9 in the top-right cell of any other square
* The asterisk: Cells r2c5, r3c3, r3c7, r5c2, r5c5, r5c8, r7c3, r7c7 and r8c5 form a special region

#### Other Possible Mixin Constraints

* Two consecutive digits cannot appear adjacent to one another
* Two adjacent digits cannot have a certain sum

## Variants that probably won't be implemented anytime soon (if at all)

#### Differently sized grids 

For example, 6x6 or 12x12 grids

#### Sukaku (Pencil Mark Clues)

This variant does not require special constraints or additional solver algorithms, so technically it is already implemented, but I add it here for completeness.

The grid starts with predetermined pencil marks in place of given digits

#### Multi-grid variants

There are multiple overlapping sudoku grids. For a few examples:

* Samurai: 5 grids, one on each corner of the central grid with a 1-square (9 cell) overlap
* Flower: 5 grids, one on each edge of the central grid, with a 6-row or 2-column overlap
* A larger grid comprised of 9 normal grids in a 3x3 pattern. No overlap, but the central square of each grid forms a tenth grid.

I will probably eventually implement this style, but it's a very low priority.