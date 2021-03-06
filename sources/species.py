import numpy
import math 
import copy

from food import *
from dna import *

# CITATION: Species Class was modelled after autonomous agents 
# https://natureofcode.com/book/chapter-6-autonomous-agents/

class Species(object):

    # variables controlling group behavior
    arrivalDistance = 50
    separationDistance = 10
    alignDistance = 100
    cohesionDistance = 50
    
    def __init__(self, xPos, yPos, colorValue = None):
        if ( colorValue==None):
            self.DNA = DNA()
        else :
            self.DNA = DNA(colorValue)
        
        self.pos = numpy.array([xPos, yPos])
        self.vel = numpy.array([random.randint(-20, 20), random.randint(-20, 20)])
        self.acc = numpy.array([0, 0])

        # size and speed is inversely related 
        self.size = random.randint(5, 10)
        self.maxForce = 0.5 + random.random()/2
        self.maxSpeed = random.uniform(100/self.size, 200/self.size)
        
        self.colorIndex = set()
        self.points = []   
        for i in range(10):
            r = random.randint(self.size//2, self.size)
            x = self.pos[0] + r * math.cos(math.pi*2*i/10)
            y = self.pos[1] + r * math.sin(math.pi*2*i/10)
            self.points.append( (x, y) )  

        self.energy = 125
        self.age = 0
        self.grownUp = 100
        self.maxAge = 200
        
        self.prey = set()
        
        self.zone = None
        
    def __hash__(self):
        return hash((self.DNA.gene, self.size, self.maxForce, self.maxSpeed))
        
    def __repr__(self):
        return "%s(%d, %d)"%(self.className(), self.pos[0], self.pos[1])
   
    # Move using positoin, velocity, and acceleration 
    def move(self, width, height):
        self.vel = numpy.add(self.vel, self.acc)
        self.vel = self.limit2DVector(self.vel, self.maxSpeed)
        self.pos = numpy.add(self.pos, self.vel)
        # check edges
        if ( self.pos[0] > width) : 
            self.pos[0] = width
            self.vel[0] *= -1
        if ( self.pos[0] < 0) : 
            self.pos[0] = 0
            self.vel[0] *= -1
        if ( self.pos[1] >= height ) : 
            self.pos[1] = height
            self.vel[1] *= -1
        if (self.pos[1] < 0) : 
            self.pos[1] = 0 
            self.vel[1] *= -1
        self.acc =  numpy.array([0, 0])
        
        
    def className(self):
        longName = str(type(self))
        actualName = longName.split(".")[-1].split('\'')[0]
        return actualName
       
    @staticmethod
    def distance(x1, y1, x2, y2):
        return ( (x2-x1)**2 + (y2-y1)**2)**0.5
    
    @staticmethod
    def limit2DVector(target, max):
        mag = numpy.linalg.norm(target)
        if ( mag > max):
            ratio =  max/mag
            return numpy.array([target[0] * ratio, target[1] * ratio] )
        else : 
            return target

    @staticmethod
    def map( actual,low1, high1, low2, high2):
        return actual*(high2-low2)/(high1-low1)
     
    # apply force to acceleration
    def applyForce(self, force):
        f = force* self.size
        self.acc = numpy.add(self.acc, f)
      
    # Keep certain distance with the neighbors
    def separate(self, group):
        steer = numpy.array([0, 0])
        count = 0
        for one in group : 
            distance=  self.distance(self.pos[0], self.pos[1], one.pos[0], one.pos[1])
            if ( distance>0 and distance < self.separationDistance) : 
                diff = numpy.subtract( self.pos, one.pos)
                diff = self.limit2DVector(diff, 1)
                diff = numpy.true_divide(diff, distance)
                steer = numpy.add(steer, diff)
                count += 1
        if (count>0):
            steer = numpy.true_divide(steer, count)
            steer = self.limit2DVector(steer, 1)
            steer *= self.maxSpeed
            steer = numpy.subtract(steer, self.vel)
            steer = self.limit2DVector(steer, self.maxForce)
            self.applyForce(steer)
      
    # Head to the same direction with the group
    def align(self, group):
        steer = numpy.array([0, 0])
        count = 0
        for one in group : 
            distance=  self.distance(self.pos[0], self.pos[1], one.pos[0], one.pos[1])
            if ( distance>0 and distance < self.alignDistance) : 
                steer = numpy.add(steer, one.vel)
                count += 1
        if (count>0):
            steer = numpy.true_divide(steer, count)
            steer = self.limit2DVector(steer, 1)
            steer *= self.maxSpeed
            steer = numpy.subtract(steer, self.vel)
            steer = self.limit2DVector(steer, self.maxForce)
            self.applyForce(steer)
    
    # Try to be in a group        
    def cohere(self, group):
        steer = numpy.array([0, 0])
        count = 0
        for one in group : 
            distance=  self.distance(self.pos[0], self.pos[1], one.pos[0], one.pos[1])
            if ( distance>0 and distance < self.cohesionDistance) : 
                steer = numpy.add(steer, one.vel)
                count += 1
        if (count>0):
            steer = numpy.true_divide(steer, count)
            self.seek(numpy.add(self.pos, steer))
                                            
    def seek(self, target):
        # target comes as numpy array
        if ( not isinstance(target, numpy.ndarray)): 
            return 
        desired = numpy.subtract( target, self.pos)
        desired = self.limit2DVector( desired,1)  # normalize
        distance = self.distance(self.pos[0], self.pos[1], target[0], target[1])
        if (distance < self.arrivalDistance):
            desired *= self.map(distance, 0, self.arrivalDistance, 0, self.maxSpeed)
        else : 
            desired *= self.maxSpeed
        steer = numpy.subtract( desired, self.vel)
        steer = self.limit2DVector( steer, self.maxForce)
        self.applyForce(steer)
    
    # Eat Food 
    def eatFood(self, food):
        if ( not isinstance(food, Food) ) : return 
        if (self.distance(self.pos[0], self.pos[1], food.xPos, food.yPos)< (self.size+food.energy) ) :
            self.energy += food.energy*2
            if ( self.energy >= 255) : self.energy = 255
            return True
        else : 
            return False
            
    # Eat entities that are prey
    # Reduce the energy of eaten entity
    def eatPrey(self, other):
        if ( not isinstance(other, Species) ) : return 
        speciesType = other.className()
        if ( speciesType in self.prey) : 
            if (self.distance(self.pos[0], self.pos[1],  other.pos[0], other.pos[1])< (self.size+other.size) ):
                self.energy += int(other.energy/5)
                if ( self.energy >= 255) : self.energy = 255
                other.maxAge *= 0.5
        
            
    # Draw life-like organic shape using spline ( smooth )       
    def draw(self, canvas, paused):
        if (not paused) :
            self.points = []
            for i in range(10):
                r = random.randint(self.size//2, self.size)
                x = self.pos[0] + r * math.cos(math.pi*2*i/10)
                y = self.pos[1] + r * math.sin(math.pi*2*i/10)
                self.points.append( (x, y) )
        canvas.create_polygon(self.points, smooth="true", fill=self.generateColor())
    
    # Reproduce with certain possibiity 
    # Each species give birth to child 
    # Each species have their own inheritance
    def reproduce(self):
        pass
        
    
    # Takes decimal number and convert to Hex
    @staticmethod
    def decimalToHex(decimal):
        result = ""
        if (decimal >= 255) : decimal = 255
        while ( decimal > 0 ):
            digit = decimal%16
            if ( digit>= 10): 
                result = chr(digit%10 + ord("A")) + result
            else : 
                result = str(digit) + result
            decimal //= 16
        return "{:0>2}".format(result)
    
    # Use gene information to display its unique appearance
    def generateColor(self):
        color = "#"
        for i in range(3):
            if i in self.colorIndex : 
                color += str( Species.decimalToHex(self.DNA.gene) )
            else : 
                color += "FF"
        return color
                