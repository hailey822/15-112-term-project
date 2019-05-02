import random 


#### DNA : Unique information each entity holds
class DNA(object):
    
    def __init__(self, color = None):
        if ( color==None): self.gene = 0
        else : self.gene = color
        
    def __hash__(self):
        return self.gene
                    
    def mutate(self, mutationRate):
        if ( random.random() < 0.5) : 
            self.gene = int( random.randint(0, 200) )
        else : 
            self.gene = 0
                            