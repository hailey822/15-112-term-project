from grid import *
from food  import *

### Grid System Class
### Divides the whole ecosystem into small grids 

class GridSystem(object):
    
    def __init__(self, size, width, height):
        self.gridSystem = [ [ Grid(size, row, col) for col in range(width//size)] 
                            for row in range(height//size)]
        self.rows = height//size
        self.cols = width//size

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
            zone.remove(object)
            object.zone = self.add( object, xPos, yPos)
            
    def draw(self, canvas):
        for r in range(self.rows):
            for c in range(self.cols):
                self.gridSystem[r][c].draw(canvas)
                

#########################################################
# Algorithmic plan for Grid System
#########################################################

# First : Initialize Gridsystem 
# 	- Grid System holds grids divided into the size of the grid given. 
#
# Second : Initialize what grid holds
#	- As the initial population is added
#   - each food and species holds zone information 
#   - each zone also contains the information of entities belonging to the zone
#
# Third : Update grid system
#	- update grid information as the entities move 
#   - situations to consider
#   - : eaten food, eaten species, new species born
#   - : new food spawned from wetland
#   - : new food born as species die
#
# Fourth : Utilize grid system 
#   - optimize collision detection by only checking entities in the zone

#########################################################
