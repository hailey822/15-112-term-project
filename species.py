import random 
from food import *
from dna import * 
import copy

class Species(object):
    
    def __init__(self, xPos, yPos):
        
        self.DNA = DNA()
        
        self.xPos = xPos
        self.yPos = yPos
        self.dX = random.choice([-1, 1])
        self.dY = random.choice([-1, 1])
        
        # size and speed is inversely related 
        # bigger size has higher chance of eating food, but moves slow
        # smaller size has lower chance of eating food, but moves faster
        self.size = random.randint(5, 20)
        self.speed = random.randint(100//self.size, 150//self.size)
        
        self.energy = 125
        self.age = 0
        
        self.predators =  set()
        self.prey = set()

        
    def __hash__(self):
        return hash((self.genes))

    
    def move(self, width, height):
        self.xPos += self.dX*self.speed
        self.yPos += self.dY*self.speed
        if ( self.xPos >= width or self.xPos < 0) : self.dX *= -1
        if ( self.yPos >= height or self.yPos < 0) : self.dY *= -1
       
    @staticmethod
    def distance(x1, y1, x2, y2):
        return ( (x2-x1)**2 + (y2-y1)**2)**0.5
    
    def eatFood(self, food):
        if (Species.distance(self.xPos, self.yPos, food.xPos, food.yPos)< (self.size+food.energy) ) :
            self.energy += food.energy*2
            if ( self.energy >= 255) : self.energy = 255
            return True
        else : 
            return False

            
    def draw(self, canvas):
        color = "#FF%sFF"% (decimalToHexColor( 255 - self.energy))
        canvas.create_oval(self.xPos-self.size, self.yPos-self.size, self.xPos+self.size, self.yPos+self.size,fill =color, width=0)
        canvas.create_text(self.xPos, self.yPos, text = str(self.age))
        
    
    def reproduce(self):
        if ( random.random() < 0.01) : 
            child = Species(self.xPos, self.yPos)
            child.DNA = DNA()
            child.DNA.genes = copy.deepcopy(self.DNA.genes)
            child.DNA.mutate(random.random())
            child.size = self.size
            child.speed = self.speed 
            return child
        else : 
            return None
        
    
# Takes decimal number <= 255
# Returns Hex color
def decimalToHexColor(decimal):
    result = ""
    if (decimal >= 255) : decimal = 255
    while ( decimal > 0 ):
        digit = decimal%16
        if ( digit>= 10): 
            result = chr(digit%10 + ord("A")) + result
        else : 
            result = str(digit) + result
        decimal //= 16
    return "{:0>2}".format(result)