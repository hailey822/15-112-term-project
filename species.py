import random 
from food import *
from dna import * 

class Species(object):
    
    def __init__(self, width, height):
        
        self.DNA = DNA()
        self.genes = self.DNA.genes
        self.xPos = random.randint(0, width)
        self.yPos = random.randint(0, height)
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
        canvas.create_text(self.xPos, self.yPos, text = str(self.energy))
        
    
    def reproduce(self, other):
        pass
        
    
#Takes decimal number <= 255
# Returns Hex color
def decimalToHexColor(decimal):
    result = ""
    while ( decimal > 0 ):
        digit = decimal%16
        if ( digit>= 10): 
            result = chr(digit%10 + ord("A")) + result
        else : 
            result = str(digit) + result
        decimal //= 16
    return "{:0>2}".format(result)