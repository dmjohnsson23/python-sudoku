"""
The Index 359 variant has three special "pointer" columns on the grid: column 1, column 5, 
and column 9. Every value in those columns tells which column in the row that the respective 
digit appears in that row. For example, a 7 in row 2 column 1 means there is a 1 in row 2 column 7.
"""
from .algorithms import *
from .context import Index159Context, Classic159Context
from .pointer import PointerHouse