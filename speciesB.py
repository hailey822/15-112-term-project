from species import *

class B(Species):
    
    def __init__(self, xPos, yPos, colorValue = None):
        super().__init__(xPos, yPos, colorValue)
        self.colorIndex = 1
        #self.size = random.randint(3, 7)
        #self.maxSpeed = random.uniform(100/self.size, 200/self.size)

    def reproduce(self):
        if ( random.random() < 0.04) : 
            child = B(self.pos[0], self.pos[1])
            child.DNA = DNA()
            child.DNA.mutate(random.random())
            child.size = self.size
            child.maxForce = self.maxForce
            child.maxSpeed = self.maxSpeed
            return child
        else : 
            return None
    
    def draw(self, canvas):
        canvas.create_oval(self.pos[0]-self.size, self.pos[1]-self.size, self.pos[0]+self.size, self.pos[1]+self.size,fill=self.generateColor(), outline="red")
        canvas.create_text(self.pos[0], self.pos[1], text = str(self.DNA.gene))