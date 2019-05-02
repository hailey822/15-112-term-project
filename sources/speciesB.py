from species import *

### Inherited Species B
class B(Species):
    
    def __init__(self, xPos, yPos, colorValue = None):
        super().__init__(xPos, yPos, colorValue)
        self.colorIndex = {1}
        self.prey.add("C")
        self.prey.add("D")
        self.grownUp = 80
        self.maxAge = 150 * random.uniform(0.8, 1.2)

    def reproduce(self):
        if ( random.random() < 0.05) : 
            child = B(self.pos[0], self.pos[1])
            child.DNA = DNA()
            child.DNA.mutate(random.random())
            child.size = self.size
            child.maxForce = self.maxForce
            child.maxSpeed = self.maxSpeed
            return child
        else : 
            return None
