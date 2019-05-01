from species import *

class A(Species):

    def __init__(self, xPos, yPos, colorValue = None):
        super().__init__(xPos, yPos, colorValue)
        self.prey.add("B")
        self.prey.add("C")
        self.prey.add("D")
        self.colorIndex = {0, 1}
        self.grownUp = 100
        self.maxAge = 200 * random.uniform(0.8, 1.2)
        
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


        
        