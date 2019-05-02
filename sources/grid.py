from species import *
from speciesA import *
from speciesB import *
from speciesC import * 
from speciesD import *
from virus import*
 
from food import *

### Grid Class
### Part of 2D Grid System 
### holds food and entities that fits into the grid

class Grid(object):
    
    def __init__(self,size, row, col):
        self.size = size
        self.container = set()
        self.row = row
        self.col = col
        self.x1 = col*size
        self.x2 = (col+1)*size
        self.y1 = row*size
        self.y2 = (row+1)*size 
    
    def __hash__(self):
        return (self.x1, self.x2, self.y1, self.y2)
    
    def __repr__(self):
        return "(%d, %d)" % (self.row, self.col)
    
    def add(self, object):
        self.container.add(object)
    
    def remove(self, object):
        self.container.remove(object)
    
    def contains(self, x, y) :
        if ( (self.x1 <= x <= self.x2 ) and (self.y1 <= y <= self.y2) ) : return True
        else : return False
    
    def draw(self, canvas):
        canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill="white")
        canvas.create_text( (self.x1+self.x2)//2, (self.y1+self.y2)//2, text="(%d, %d)" % (self.row, self.col), anchor ="center")