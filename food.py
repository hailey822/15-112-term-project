import random 

class Food(object):
   
   def __init__(self, xPos, yPos):
      self.xPos = xPos
      self.yPos = yPos
      self.energy = random.randint(5, 10)
   
   def draw(self, canvas):   
      canvas.create_rectangle(self.xPos-self.energy//2, self.yPos-self.energy//2, 
                              self.xPos+self.energy//2, self.yPos+self.energy//2,
                              fill = "green", width = 0)