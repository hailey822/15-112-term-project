import random 
import numpy
import math 
import copy
from species import *

class Virus(Species):
    
    arrivalDistance = 20
    separationDistance = 10
    alignDistance = 10
    cohesionDistance = 10
    
    def __init__(self, xPos, yPos):      
        self.initialPos = (xPos, yPos)
        self.pos = numpy.array([xPos, yPos])
        self.vel = numpy.array([random.randint(-20, 20), random.randint(-20, 20)])
        self.acc = numpy.array([0, 0])
        self.size = random.randint(5, 10)

        self.age = 0
        self.maxAge = 300
        
        self.prey = set()
        
        self.maxSpeed = random.uniform(20.0, 40.0)
        self.maxForce = random.uniform(5.0, 10.0)
    
    def closetTarget(self, data):
        minDis = data.width
        minPos = None
        targetGroup = None
        if ( data.virusTargetIndex == 0 ) : targetGroup = data.A
        if ( data.virusTargetIndex == 1 ) : targetGroup = data.B
        if ( data.virusTargetIndex == 2 ) : targetGroup = data.C
        if ( data.virusTargetIndex == 3 ) : targetGroup = data.D
    
        for a in targetGroup : 
            dis = self.distance(self.pos[0], self.pos[1], a.pos[0], a.pos[1])
            if ( dis < minDis) : 
                minDis = dis
                minPos = a.pos
        return minPos
        
    def seekTarget(self, target):
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
        steer = self.limit2DVector( steer, self.maxForce/100)
        self.applyForce(steer)
        
    
    def __hash__(self):
        return hash((self.initialPos, self.maxForce, self.maxSpeed))
    
    def eatPrey(self, other):
        speciesType = other.className()
        if ( speciesType in self.prey) : 
            if (self.distance(self.pos[0], self.pos[1],  other.pos[0], other.pos[1])< (self.size+other.size) ):
                other.energy = 0
                self.age = self.maxAge 
                return True
        return False
        
    def draw(self, canvas):
        canvas.create_oval(self.pos[0]-self.size, self.pos[1] - self.size,
                            self.pos[0]+ self.size, self.pos[1] + self.size,
                            fill="red", width=0)