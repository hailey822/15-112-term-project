
from species import *
from speciesA import *
from speciesB import *
from speciesC import * 
from speciesD import *
from virus import*
 
from food import *

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
        return "grid(%d, %d) : %s" % (self.row, self.col, str(self.container))
    
    def add(self, object):
        self.container.add(object)
    
    def remove(self, object):
        self.container.remove(object)
    
    def contains(self, x, y) :
        if ( (self.x1 <= x <= self.x2 ) and (self.y1 <= y <= self.y2) ) : return True
        else : return False