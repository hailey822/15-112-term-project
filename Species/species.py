class Species(object):
#   function move
#   function eat
#   function attack
#   functino reproduce
    
    def __init__(self, width, height):
        self.DNA = DNA()
        self.genes = self.DNA.genes
        self.xPos = random(0, width)
        self.yPos = random(0, height)
        self.predators = set()
        self.prey = set()
        self.age = 0

    def move(self):
        pass
    
    def eat(self, other):
        pass
        
    def draw(self, canvas):
        canvas.create_oval(self.xPos-10, self.yPos-10, self.xPos+10, self.yPos+10,fill = "red")
    
    def reproduce(self):
        
        
    