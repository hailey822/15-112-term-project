import random 

class DNA(object):
    
    def __init__(self, color = None):
        if ( color==None):
            self.gene = random.randint(0, 156) + 100
        else :
            self.gene = color
        
    def __hash__(self):
        return self.gene
                    
    def mutate(self, mutationRate):
        if ( random.random() < 0.5) : 
            self.gene = int( 155 * mutationRate) + 100
        else : 
            self.gene = 0
                            