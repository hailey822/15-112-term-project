from species import *

class A(Species):
    
    def __init__(self, xPos, yPos, colorValue = None):
        super().__init__(xPos, yPos, colorValue)
        self.prey.add("B")
        self.colorIndex = 0
        #self.size = random.randint(5, 15)
        #self.maxSpeed = random.uniform(100/self.size, 150/self.size)
        
    def reproduce(self):
        if ( random.random() < 0.01) : 
            child = A(self.pos[0], self.pos[1])
            child.DNA = DNA()
            child.DNA.mutate(random.random())
            child.maxForce = self.maxForce
            child.maxSpeed = self.maxSpeed
            return child
        else : 
            return None
        
    def draw(self, canvas):
        canvas.create_oval(self.pos[0]-self.size, self.pos[1]-self.size, self.pos[0]+self.size, self.pos[1]+self.size,fill=self.generateColor(), outline="blue")
        canvas.create_text(self.pos[0], self.pos[1], text = str(self.DNA.gene))
        
            
        