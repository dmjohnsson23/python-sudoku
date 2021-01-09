import math
import itertools

### CONSTANTS ###

# Border Constants #
SINGLE_BORDER="SINGLE BORDER"
DOUBLE_BORDER="DOUBLE BORDER"


# Char Type Constants #
TOP="TOP"
BOTTOM="BOTTOM"
LEFT="LEFT"
RIGHT="RIGHT"

TOP_LEFT="TOP LEFT"
TOP_RIGHT="TOP RIGHT"
BOTTOM_LEFT="BOTTOM LEFT"
BOTTOM_RIGHT="BOTTOM RIGHT"

HORIZONTAL="HORIZONTAL"
VERTICAL="VERTICAL"


# Alignment Constants #
ALIGNED_LEFT="ALIGNED LEFT"
ALIGNED_RIGHT="ALIGNED RIGHT"

ALIGNED_TOP="ALIGNED TOP"
ALIGNED_BOTTOM="ALIGNED BOTTOM"

ALIGNED_CENTER="ALIGNED CENTER"



### Char Tables ###
#        (TPYE,         HORIZONTAL,    VERTICAL     ):'CHAR',
CORNERS={(TOP_LEFT,     SINGLE_BORDER, SINGLE_BORDER):'┌',
         (TOP_RIGHT,    SINGLE_BORDER, SINGLE_BORDER):'┐',
         (BOTTOM_LEFT,  SINGLE_BORDER, SINGLE_BORDER):'└',
         (BOTTOM_RIGHT, SINGLE_BORDER, SINGLE_BORDER):'┘',
         
         (TOP_LEFT,     DOUBLE_BORDER, DOUBLE_BORDER):'╔',
         (TOP_RIGHT,    DOUBLE_BORDER, DOUBLE_BORDER):'╗',
         (BOTTOM_LEFT,  DOUBLE_BORDER, DOUBLE_BORDER):'╚',
         (BOTTOM_RIGHT, DOUBLE_BORDER, DOUBLE_BORDER):'╝',
         
         (TOP_LEFT,     SINGLE_BORDER, DOUBLE_BORDER):'╓',
         (TOP_RIGHT,    SINGLE_BORDER, DOUBLE_BORDER):'╖',
         (BOTTOM_LEFT,  SINGLE_BORDER, DOUBLE_BORDER):'╙',
         (BOTTOM_RIGHT, SINGLE_BORDER, DOUBLE_BORDER):'╜',
         
         (TOP_LEFT,     DOUBLE_BORDER, SINGLE_BORDER):'╒',
         (TOP_RIGHT,    DOUBLE_BORDER, SINGLE_BORDER):'╕',
         (BOTTOM_LEFT,  DOUBLE_BORDER, SINGLE_BORDER):'╘',
         (BOTTOM_RIGHT, DOUBLE_BORDER, SINGLE_BORDER):'╛',
        } 


#      (TYPE,   HORIZONTAL,    VERTICAL     ):'CAHR',
SIDES={(TOP,    SINGLE_BORDER, SINGLE_BORDER):'┬',
       (BOTTOM, SINGLE_BORDER, SINGLE_BORDER):'┴',
       (LEFT,   SINGLE_BORDER, SINGLE_BORDER):'├',
       (RIGHT,  SINGLE_BORDER, SINGLE_BORDER):'┤',
       
       (TOP,    DOUBLE_BORDER, DOUBLE_BORDER):'╦',
       (BOTTOM, DOUBLE_BORDER, DOUBLE_BORDER):'╩',
       (LEFT,   DOUBLE_BORDER, DOUBLE_BORDER):'╠',
       (RIGHT,  DOUBLE_BORDER, DOUBLE_BORDER):'╣',
       
       (TOP,    SINGLE_BORDER, DOUBLE_BORDER):'╥',
       (BOTTOM, SINGLE_BORDER, DOUBLE_BORDER):'╨',
       (LEFT,   SINGLE_BORDER, DOUBLE_BORDER):'╟',
       (RIGHT,  SINGLE_BORDER, DOUBLE_BORDER):'╢',
       
       (TOP,    DOUBLE_BORDER, SINGLE_BORDER):'╤',
       (BOTTOM, DOUBLE_BORDER, SINGLE_BORDER):'╧',
       (LEFT,   DOUBLE_BORDER, SINGLE_BORDER):'╞',
       (RIGHT,  DOUBLE_BORDER, SINGLE_BORDER):'╡',
      }


#          (HORIZONTAL,    VERTICAL     ):'CHAR',
JUNCTIONS={(SINGLE_BORDER, SINGLE_BORDER):'┼',
           (DOUBLE_BORDER, DOUBLE_BORDER):'╬',
           (SINGLE_BORDER, DOUBLE_BORDER):'╫',
           (DOUBLE_BORDER, SINGLE_BORDER):'╪',
          }
#      (TYPE,       BORDER       ):'CHAR',
EDGES={(HORIZONTAL, SINGLE_BORDER):'─',
       (VERTICAL,   SINGLE_BORDER):'│',
       (HORIZONTAL, DOUBLE_BORDER):'═',
       (VERTICAL,   DOUBLE_BORDER):'║',
      }

PADDING=' '

### Everything Else ###
class Grid:
    def __init__(self, rowBorders, colBorders, hAlignment=ALIGNED_LEFT, vAlignment=ALIGNED_TOP):
        self.rowBorders=rowBorders
        self.colBorders=colBorders
        self.hAlignment=hAlignment
        self.vAlignment=vAlignment
    
    
    def stringify(self, dataTable):
        stringTable=[]
        for dataRow in dataTable:
            stringRow=[]
            for cell in dataRow:
                stringRow.append(str(cell).splitlines())
            stringTable.append(stringRow)
        return stringTable
    
    
    def normalize(self, data):
        data=self.stringify(data)
        
        tempData=[]
        
        self.rowHeights=[]
        self.colLengths=[]
        
        
        for row in data:
            maxHeight=max(*row, key=lambda x: len(x))
            self.rowHeights.append(maxHeight)
            tempData.append(alignList(row, maxHeight, self.vAlignment))
        
        data=[]
        for col in zip(*tempData):
            maxLen=max(*itertools.chain(*col), key=lambda x: len(x))
            self.rowHeights.append(maxLen)
            newCol=[]
            for cell in col:
                newCell=cell  
                for string in cell:  #Each cell is a list of strings. Each string is one line.
                    newCell.append(alignstring(string, maxHeight, self.vAlignment))
                newCol.append(newCell)
            data.append(newCol)
        
        return [list(row) for row in zip(*data)] #we need to invert the table again as is was inverted when iterating over cols
        
    def draw(self, data):
        data=self.normalize(data)
        hBorders=itertools.repeat(self.rowBorders) #Using 'repeat' so borders can simply be entered as a pattern 
        vBorders=itertools.repeat(self.colBorders) #and so tables do not have to have a fixed size.
        output=[]
        
        #first, do the top line
        line=""
        hBord=next(hBorders)
        line+=CORNERS[TOP_LEFT, hBord, next(vBorders)]
        firstTime=True
        for length in self.colLengths:
            if not firstTime: #This block will be skipped on the first iteration of the loop
                firstTime=False
                line += SIDES[TOP, hBord, next(vBorders)]
            line += (EDGES[HORIZONTAL, hBord]) * length
        line += CORNERS[TOP_RIGHT, hBord, next(vBorders)]
        output.append(line)
        vBorders=itertools.repeat(self.colBorders) # reset vBorders to the beginning
        
        
        # then all the lines in between
        firstRow=True
        for row in data:
            if not firstRow: #this bock will be skipped on the first row
                line=""
                hBord=next(hBorders)
                line+=SIDES[LEFT, hBord, next(vBorders)]
                firstTime=True
                for length in self.colLengths:
                    if not firstTime: #This block will be skipped on the first iteration of the loop
                        firstTime=False
                        line += JUNCTIONS[TOP, hBord, next(vBorders)]
                    line += (EDGES[HORIZONTAL, hBord]) * length
                line += SIDES[RIGHT, hBord, next(vBorders)]
                output.append(line)
                vBorders=itertools.repeat(self.colBorders) # reset vBorders to the beginning
            
            for rowLine in zip(*row):
                line=""
                line+=EDGES[VERTICAL, next(vBorders)]
                firstTime=True
                for cellPart in rowLine:
                    if not firstTime: #This block will be skipped on the first iteration of the loop
                        firstTime=False
                        line += EDGES[VERTICAL, next(vBorders)]
                    line += cellPart
                line += EDGES[VERTICAL, next(vBorders)]
                output.append(line)
                vBorders=itertools.repeat(self.colBorders) # reset vBorders to the beginning
            
       #then the last line
        line=""
        hBord=next(hBorders)
        line+=CORNERS[BOTTOM_LEFT, hBord, next(vBorders)]
        firstTime=True
        for length in self.colLengths:
            if not firstTime: #This block will be skipped on the first iteration of the loop
                firstTime=False
                line += SIDES[TOP, hBord, next(vBorders)]
            line += (EDGES[HORIZONTAL, hBord]) * length
        line += CORNERS[BOTTOM_RIGHT, hBord, next(vBorders)]
        output.append(line)
        vBorders=itertools.repeat(self.colBorders) # reset vBorders to the beginning
            
def alignList(lines, length, alignment, padding=[""]):
    if len(lines) >= length:
        return lines
    else:
        if alignment == ALIGNED_TOP:
            return lines + (padding * (length - len(lines)))
        elif alignment == ALIGNED_BOTTOM:
            return (padding * (length - len(lines))) +lines
        elif alignment == ALIGNED_CENTER:
            length = (length - len(lines)) / 2
            lLen=math.floor(length)
            rLen=math.ceil(length)
            return (padding * lLen) + lines + (padding * rLen)


def alignString(string, length, alignment, padding=PADDING):
    if len(lines) >= length:
        return lines
    else:
        if alignment == ALIGNED_LEFT:
            return string.ljust(length, padding)
        elif alignment == ALIGNED_RIGHT:
            return string.rjust(length, padding)
        elif alignment == ALIGNED_CENTER:
            return string.center(length, padding)


            
if __name__=="__main__":
    testData=[["string",                         "another",              "multi\nliner"],
              [12,                               float("inf"),           11.3],
              [["a", "list", "of", "strings"],   {"dict":1, "data":6},   ("some", "stuff")]]
    
    table=Grid((DOUBLE_BORDER, SINGLE_BORDER, SINGLE_BORDER, DOUBLE_BORDER),
               (DOUBLE_BORDER, SINGLE_BORDER, SINGLE_BORDER, DOUBLE_BORDER))
    
    table.draw(testData)
