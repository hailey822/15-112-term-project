import random 
import numpy
import math 
import copy

from food import *
from dna import *

# CITATION: The structure of Species was modelled after autonomous agents 
# https://natureofcode.com/book/chapter-6-autonomous-agents/

class Species(object):

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
        # self.dX = random.choice([-1, 1])
        # self.dY = random.choice([-1, 1])

        # size and speed is inversely related 
        # bigger size has higher chance of eating food, but moves slow
        # smaller size has lower chance of eating food, but moves faster
        self.size = random.randint(5, 10)
        self.maxForce = 0.5 + random.random()/2
        self.maxSpeed = random.uniform(100/self.size, 200/self.size)
        
        self.colorIndex = -1
        
        self.energy = 125
        self.age = 0
        
        self.prey = set()
        
    def __hash__(self):
        return hash((self.DNA.gene, self.size, self.maxForce, self.maxSpeed))
        
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
        
    def applyForce(self, force):
        f = force* self.size
        self.acc = numpy.add(self.acc, f)
        
    
    def separate(self, group):
        steer = numpy.array([0, 0])
        count = 0
        for one in group : 
            distance=  self.distance(self.pos[0], self.pos[1], one.pos[0], one.pos[1])
            if ( distance>0 and distance < self.separationDistance) : 
                diff = numpy.subtract( self.pos, one.pos)
                diff = self.limit2DVector(diff, 1)
                diff /= distance
                steer = numpy.add(steer, diff)
                count += 1
        if (count>0):
            steer = numpy.true_divide(steer, count)
            steer = self.limit2DVector(steer, 1)
            steer *= self.maxSpeed
            steer = numpy.subtract(steer, self.vel)
            steer = self.limit2DVector(steer, self.maxForce)
            self.applyForce(steer)
                
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
            print("Target is not vectors")
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
    
    def eatFood(self, food):
        if (self.distance(self.pos[0], self.pos[1], food.xPos, food.yPos)< (self.size+food.energy) ) :
            self.energy += food.energy*2
            if ( self.energy >= 255) : self.energy = 255
            return True
        else : 
            return False
        
    def eatPrey(self, other):
        speciesType = other.className()
        if ( speciesType in self.prey) : 
            if (self.distance(self.pos[0], self.pos[1],  other.pos[0], other.pos[1])< (self.size+other.size) ):
                self.energy += other.energy
                if ( self.energy >= 255) : self.energy = 255
                return True
            else : 
                return False
        else : 
            return False
            
            
    def draw(self, canvas):
        canvas.create_oval(self.pos[0]-self.size, self.pos[1]-self.size, self.pos[0]+self.size, self.pos[1]+self.size,fill=self.generateColor())
        canvas.create_text(self.pos[0], self.pos[1], text = str(self.DNA.gene))
        
    
    def reproduce(self):
        if ( random.random() < 0.01) : 
            print("reproduce")
            child = Species(self.pos[0], self.pos[1])
            child.DNA = DNA()
            child.DNA.gene = self.DNA.gene
            child.DNA.mutate(random.random())
            child.size = self.size
            child.maxForce = self.maxForce
            child.maxSpeed = self.maxSpeed
            return child
        else : 
            return None
        
    
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
    

    def generateColor(self):
        color = "#"
        for i in range(3):
            if i==self.colorIndex : 
                color += str( Species.decimalToHex(self.DNA.gene) )
            else : 
                color += "FF"
        return color
                
        
        
    