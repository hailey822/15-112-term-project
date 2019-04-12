import random 

class DNA(object):
    
    def __init__(self):
        self.genes = [random.randint(65, 123) for i in range(0, 10)]
        
    def crossOver(self, other): 
        child = DNA()
        if (not isinstance(other, DNA) ) : 
            return None
        midpoint = random.randint(0, len(self.genes));
        for i in range( len(self.genes)): 
            if ( i > midpoint) : child.genes[i] = self.genes[i];
            else               : child.genes[i] = other.genes[i];
        return child
            
    
    def mutate(self, mutationRate):
        for i in range( len(self.genes) ): 
            if (random.random() < mutationRate):
                self.genes[i] = random.randint(65, 123)
            
                