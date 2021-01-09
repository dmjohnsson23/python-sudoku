_=None #Just makes the puzzles look neater


puzzles = {
           "Blank":
           [
            [_, _, _,   _, _, _,    _, _, _],
            [_, _, _,   _, _, _,    _, _, _],
            [_, _, _,   _, _, _,    _, _, _],
            
            [_, _, _,   _, _, _,    _, _, _],
            [_, _, _,   _, _, _,    _, _, _],
            [_, _, _,   _, _, _,    _, _, _],
            
            [_, _, _,   _, _, _,    _, _, _],
            [_, _, _,   _, _, _,    _, _, _],
            [_, _, _,   _, _, _,    _, _, _]
           ],
           
           
           "Already Solved":  #Made it myself!
           [
            [1, 2, 3,   4, 5, 6,    7, 8, 9],
            [4, 5, 6,   7, 8, 9,    1, 2, 3],
            [7, 8, 9,   1, 2, 3,    4, 5, 6],
            
            [2, 3, 1,   5, 6, 7,    8, 9, 4],
            [5, 6, 4,   8, 9, 1,    2, 3, 7],
            [8, 9, 7,   2, 3, 4,    5, 6, 1],
            
            [3, 4, 2,   6, 7, 8,    9, 1, 5],
            [6, 7, 5,   9, 1, 2,    3, 4, 8],
            [9, 1, 8,   3, 4, 5,    6, 7, 2]
           ],
           
           
           "Ridiculously Easy":  #Based on "Already Solved"
           [
            [1, 2, 3,   4, 5, 6,    7, 8, 9],
            [4, _, 6,   7, 8, 9,    1, _, 3],
            [7, 8, 9,   1, 2, 3,    4, 5, 6],
            
            [2, 3, 1,   5, 6, 7,    8, 9, 4],
            [5, 6, 4,   8, _, 1,    2, 3, 7],
            [8, 9, 7,   2, 3, 4,    5, 6, 1],
            
            [3, 4, 2,   6, 7, 8,    9, 1, 5],
            [6, _, 5,   9, 1, 2,    3, _, 8],
            [9, 1, 8,   3, 4, 5,    6, 7, 2]
           ],
           
           
###          puzzles from websudoku.com          ###
           
           "Easy 7,797,002,451":
           [
            [8, 1, _,   _, 5, _,    2, 3, _],
            [_, _, _,   6, _, _,    _, 7, 4],
            [5, 7, 6,   3, _, _,    _, _, 8],
            
            [_, _, _,   4, _, _,    7, 2, 1],
            [_, _, 8,   _, _, _,    4, _, _],
            [1, 4, 2,   _, _, 5,    _, _, _],
            
            [4, _, _,   _, _, 6,    9, 1, 7],
            [6, 2, _,   _, _, 7,    _, _, _],
            [_, 3, 7,   _, 1, _,    _, 6, 2]
           ],
           
           
           
           "Medium 1,465,295,375":
           [
            [4, _, _,   _, _, 9,    _, 3, _],
            [_, 5, _,   2, _, _,    1, _, 9],
            [_, _, _,   8, 6, _,    5, _, _],
            
            [_, 9, _,   _, _, _,    2, _, 7],
            [5, _, _,   _, _, _,    _, _, 8],
            [2, _, 4,   _, _, _,    _, 5, _],
            
            [_, _, 1,   _, 8, 5,    _, _, _],
            [6, _, 2,   _, _, 7,    _, 9, _],
            [_, 4, _,   3, _, _,    _, _, 6]
           ],
           
           
           
           "Hard 4,658,865,853":
           [
            [_, _, _,   9, _, _,    7, _, _],
            [6, 3, 5,   _, _, _,    _, _, _],
            [9, _, _,   5, _, 8,    3, _, _],
            
            [_, 6, _,   _, _, _,    _, _, 3],
            [4, 2, 3,   _, _, _,    6, 9, 5],
            [7, _, _,   _, _, _,    _, 8, _],
            
            [_, _, 9,   3, _, 1,    _, _, 8],
            [_, _, _,   _, _, _,    9, 1, 2],
            [_, _, 4,   _, _, 9,    _, _, _]
           ],
           
           
           
           "Evil 7,360,298,562":
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
           ],
           
           
           "Only 17": #From http://www.qedcat.com/archive/106.html
           [          #They say that 17 is the least number of filled
            [_, _, _,   _, _, _,    _, 1, _],# squares a puzzle can
            [4, _, _,   _, _, _,    _, _, _],# have (so far) and
            [_, 2, _,   _, _, _,    _, _, _],# still only have one
                                             # solution
            [_, _, _,   _, 5, _,    4, _, 7],
            [_, _, 8,   _, _, _,    3, _, _],
            [_, _, 1,   _, 9, _,    _, _, _],
            
            [3, _, _,   4, _, _,    2, _, _],
            [_, 5, _,   1, _, _,    _, _, _],
            [_, _, _,   8, _, 6,    _, _, _]
           ],
           
           
           "Brute Force Prevails": #From http://www.qedcat.com/archive/106.html
           [                       #There are two possible solutions to this puzzle
            [2, 8, 3,   6, 7, 1,    9, 4, 5],
            [9, 7, 6,   5, 4, _,    _, 3, 1], #Empty spaces are 2 and 8
            [4, 1, 5,   3, 9, _,    _, 7, 6],
            
            [5, 6, 7,   4, 1, 9,    3, 8, 2],
            [8, 3, 4,   2, 6, 7,    1, 5, 9],
            [1, 9, 2,   8, 3, 5,    4, 6, 7],
            
            [3, 2, 1,   7, 8, 6,    5, 9, 4],
            [7, 5, 8,   9, 2, 4,    6, 1, 3],
            [6, 4, 9,   1, 5, 3,    7, 2, 8]
           ],
           }