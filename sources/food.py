import random 

### Food Class 
### provide source of energy to sustain life for entities
class Food(object):
   
   def __init__(self, xPos, yPos):
      self.xPos = xPos
      self.yPos = yPos
      self.energy = random.randint(5, 10)
      self.zone = None
   
   def __hash__(self):
      return hash((self.xPos, self.yPos, self.energy))
      
   def __repr__(self):
      return "food(%d, %d)"%(self.xPos, self.yPos)
   
   def draw(self, canvas):   
      canvas.create_oval(self.xPos-self.energy//3, self.yPos-self.energy//3, 
                              self.xPos+self.energy//3, self.yPos+self.energy//3,
                              fill="dark green", width=0) 