from grid import *
from food  import *

class GridSystem(object):
    
    def __init__(self, size, width, height):
        self.gridSystem = [ [ Grid(size, row, col) for col in range(width//size)] for row in range(height//size)]
        self.rows = height//size
        self.cols = width//size
    
    def print(self):
        for r in range(self.rows):
            for c in range(self.cols):
                print(self.gridSystem[r][c])
    
    def currentZone(self, object, xPos, yPos):
        for r in range(self.rows):
            for c in range(self.cols):
                if ( self.gridSystem[r][c].contains(xPos, yPos)) : 
                    return self.gridSystem[r][c]
            
    def add(self, object, xPos, yPos):
        zone = self.currentZone(object, xPos, yPos)
        zone.add(object)
        return zone
    
    def update(self, object, xPos, yPos):
        zone = object.zone
        new = self.currentZone(object, xPos, yPos)
        if ( zone != new): 
            #print("%s : %s --> %s" %(object, zone, new))
            zone.remove(object)
            object.zone = self.add( object, xPos, yPos)
                