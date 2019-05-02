from species import *

### Inherited Species D
class D(Species):
    
    def __init__(self, xPos, yPos, colorValue = None):
        super().__init__(xPos, yPos, colorValue)
        self.colorIndex = {0, 2}
        self.prey.add("C")
        self.grownUp = 30
        self.maxAge =  50 * random.uniform(0.8, 1.2)
        # size and speed is inversely related 
        self.size = random.randint(2, 5)
        self.maxSpeed = random.uniform(20/self.size, 50/self.size)

    def reproduce(self):
        if ( random.random() < 0.07) : 
            child = D(self.pos[0], self.pos[1])
            child.DNA = DNA()
            child.DNA.mutate(random.random())
            child.size = self.size
            child.maxForce = self.maxForce
            child.maxSpeed = self.maxSpeed
            return child
        else : 
            return None
