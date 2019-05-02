from species import *

### Inherited Species C
class C(Species):
    
    def __init__(self, xPos, yPos, colorValue = None):
        super().__init__(xPos, yPos, colorValue)
        self.colorIndex = {2}
        self.prey.add("B")
        self.grownUp = 50
        self.maxAge = 100 * random.uniform(0.8, 1.2)
        # size and speed is inversely related 
        self.size = random.randint(4, 8)
        self.maxSpeed = random.uniform(30/self.size, 100/self.size)

    def reproduce(self):
        if ( random.random() < 0.05) : 
            child = C(self.pos[0], self.pos[1])
            child.DNA = DNA()
            child.DNA.mutate(random.random())
            child.size = self.size
            child.maxForce = self.maxForce
            child.maxSpeed = self.maxSpeed
            return child
        else : 
            return None
