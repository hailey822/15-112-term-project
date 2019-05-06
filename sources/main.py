####################################
# Main Mode
####################################

from tkinter import *
from tkinter.font import Font


from PIL import Image
from PIL import ImageTk

from species import *
from speciesA import *
from speciesB import *
from speciesC import * 
from speciesD import *
from virus import*
 
from food import *
from wetland import *

from gridSystem import*

import numpy 
import random
from graph import *

def MainKeyPressed(event, data):
    if ( event.keysym == "p"):  data.paused = not data.paused
    if ( data.emergency ): return     
    if ( event.keysym == "Return"): data.wetland.update()
   
def MainRedrawAll(canvas, data):
    # Ecosystem 
    if (data.emergency) : 
        canvas.create_rectangle(0, 0, data.width, data.height, fill="pink", width=0)
    data.wetland.draw(canvas)
    for food  in data.foods: food.draw(canvas)
    for animal in data.animals: 
        animal.draw(canvas, data.paused)
    if (data.emergency) : 
        for virus in data.virus: virus.draw(canvas)
    
    # UI compoment 
    graphWrapper(canvas, data)
    pause(canvas, data)
    canvas.create_rectangle(data.width*0.925, 10, data.width*0.985, 35, fill="white")
    canvas.create_text(data.width*0.955, 13, text="guideline", anchor="n")
    

def MainMousePressed(event, data):
    
    # Change data mode to guideline
    if (  (data.width*0.925 <= event.x <= data.width*0.985) and ( 10 <= event.y <= 35) ):
        data.mode = "guideline"
        data.paused = True
        return

    # Graph selector
    newGraphIndex = clickGraphSelector(event.x, event.y, data.width*0.805, data.width*0.965, data.height*0.97)
    if ( newGraphIndex != -1 ) : 
        data.graphIndex = newGraphIndex 
    
    if ( data.paused or data.emergency): return 
    
    # Add wetland 
    if ( event.x > data.width*0.75 and event.y > data.height*0.74) : return  
    if ( not data.wetland.contains(event.x, event.y)) : 
        data.wetland.add(event.x, event.y)
        
        
def MainTimerFired(data): 

    if ( data.paused ): return 
    
    # Emergency starts
    if ( len(data.animals) > 180) : 
        data.emergency = True
        if (not data.spawned) : spawnVirus(data)
    # Emergency ends
    if ( len(data.virus) == 0 ):
        data.emergency = False
        data.spawned = False
        data.virusTarget = None
        data.virusTargetIndex = None
        data.newLife = []
    
    # Graph Information
    graphCalculation(data)
    
    # Emergency situation
    if ( data.emergency) : 
        emergency(data)
        return 
    
    # Species Group Behavior 
    groupBehavior(data, data.A)
    groupBehavior(data, data.B)
    groupBehavior(data, data.C)
    groupBehavior(data, data.D)
    
    # Wetland 
    data.wetland.age()
    data.wetland.generateFood(data)
        
    # Animal : Move, EatFood, energy reduction
    aIndex = 0
    
    newAnimals = []
    while ( aIndex < len(data.animals) ):
        
        # grid system is used to improve collision check 
        # only check other species and food in the zone 
        zone = data.animals[aIndex].zone
        
        # Animals age
        data.animals[aIndex].age += 1
        
        # Animals reproduce after certain age
        if ( data.animals[aIndex].age > data.animals[aIndex].grownUp ): 
            child = data.animals[aIndex].reproduce()
            if ( child != None) : 
                child.zone = data.gs.add(child, child.pos[0], child.pos[1])
                if ( child.className() == "A"): data.A.add(child)
                if ( child.className() == "B"): data.B.add(child)
                if ( child.className() == "C"): data.C.add(child)
                if ( child.className() == "D"): data.D.add(child)
                data.animals.append(child)
                
        
        # Animals eat food
        newContainer = set()
        for object in zone.container:
            if ( data.animals[aIndex].eatFood(object) ) :
                data.foods.remove(object)
            else : 
                newContainer.add(object)
        zone.container = newContainer
        

        # Animals run out of energy as it moves 
        data.animals[aIndex].energy -= 1
        # Die when entered Death Trap
        enteredTrap = data.wetland.deathTrap(data.animals[aIndex].pos[0], 
                                            data.animals[aIndex].pos[1])
        # Die without energy -> spawn food on dead places
        # Die over certain age
        if (data.animals[aIndex].energy >= 0 and 
            data.animals[aIndex].age < data.animals[aIndex].maxAge 
            and not enteredTrap ) : 
            newAnimals.append(data.animals[aIndex])
        else  :
            death(data, aIndex)
            food =  Food(data.animals[aIndex].pos[0], data.animals[aIndex].pos[1])
            food.zone = data.gs.add( food, data.animals[aIndex].pos[0], data.animals[aIndex].pos[1])
            data.foods.append(food )

                    
        # Animals eat pray -> reduce lifestime of the eaten organism 
        for object in zone.container:
            data.animals[aIndex].eatPrey(object)
            
        aIndex += 1

        
    data.animals = newAnimals

# Initialize the first population 
def populate(data):
    for i in range(40):
        xPos = random.randint(0, data.width)
        yPos = random.randint(0, data.height)
        food =  Food(xPos, yPos)
        food.zone = data.gs.add( food, xPos, yPos)
        data.foods.append(food )

    for i in range(40):
        xPos = random.randint(0, data.width)
        yPos = random.randint(0, data.height)
        organism = A(xPos, yPos, 0)
        organism.zone = data.gs.add(organism, xPos, yPos)
        data.A.add(organism)
        data.animals.append( organism)

    for i in range(40):
        xPos = random.randint(0, data.width)
        yPos = random.randint(0, data.height)
        organism = B(xPos, yPos, 0)
        organism.zone = data.gs.add(organism, xPos, yPos)
        data.B.add(organism)
        data.animals.append( organism)
    
    for i in range(30):
        xPos = random.randint(0, data.width)
        yPos = random.randint(0, data.height)
        organism = C(xPos, yPos, 0)
        organism.zone = data.gs.add(organism, xPos, yPos)
        data.C.add(organism)
        data.animals.append( organism)

    for i in range(30):
        xPos = random.randint(0, data.width)
        yPos = random.randint(0, data.height)
        organism = D(xPos, yPos, 0)
        organism.zone = data.gs.add(organism, xPos, yPos)
        data.D.add(organism)
        data.animals.append( organism)

# Remove dead entities        
def death(data, index):
    target = data.animals[index]
    zone = target.zone
    if ( target.className() == "A"):  data.A.remove(target)
    if ( target.className() == "B"):  data.B.remove(target)
    if ( target.className() == "C"):  data.C.remove(target)
    if ( target.className() == "D"):  data.D.remove(target) 
    zone.remove(target)

# Each Species have group behavior s
def groupBehavior(data, group):
    for animal in group : 
        animal.cohere(group)
        animal.align(group)
        animal.separate(group)
        animal.move(data.width, data.height)
        data.gs.update(animal, animal.pos[0], animal.pos[1])
        animal.acc = numpy.array([0, 0])

# Pause Button 
def pause(canvas, data):
    canvas.create_oval( 10, 10, 40, 40, fill="white")
    if ( data.paused) : 
        canvas.create_polygon( 20, 15, 20, 35, 35, 25, fill="black")
    else : 
        canvas.create_rectangle( 17, 18, 22, 32, fill="black")
        canvas.create_rectangle( 27, 18, 32, 32, fill="black")
    canvas.create_text( 100, 25, text="press \"p\" to \npause/resume", anchor = "center")


# Starts emergency situation by spawning virus
def spawnVirus(data):
    # choose the most over-populated species 
    pop = [ len(data.A), len(data.B), len(data.C), len(data.D)]
    index = pop.index( max(pop))
    data.virusTargetIndex = index
    if ( index ==0 ): data.virusTarget = data.A
    if ( index ==1 ): data.virusTarget = data.B
    if ( index ==2 ): data.virusTarget = data.C
    if ( index ==3 ): data.virusTarget = data.D
    print(pop)
    print("target is " + str(index))
    
    # choose the least-populated species 
    least = pop.index( min(pop))
    data.newLife.append(least)
    for i in range(4):
        if ( pop[i] == 0 ): data.newLife.append(i)
    print(data.newLife)
    for i in range( pop[index]//3):
        xPos = random.randint(0, data.width)
        yPos = random.randint(0, data.height)
        organism = Virus(xPos, yPos)
        if ( index ==0 ): organism.prey.add("A")
        if ( index ==1 ): organism.prey.add("B")
        if ( index ==2 ): organism.prey.add("C")
        if ( index ==3 ): organism.prey.add("D")
        data.virus.add(organism)    
    data.spawned = True
    print("emergency started")

# Runs viruses and their behavior 
# Kill target species
# Become least populated species after mission 
def emergency(data):
    newVirus = set()
    for virus in data.virus:
        virus.seekTarget( virus.closetTarget(data))
        virus.move(data.width, data.height)
        newAnimals = []
        for index in range(len(data.animals)):
            if ( not virus.eatPrey(data.animals[index]) ): newAnimals.append(data.animals[index])
            else  :
                death(data, index)
                if ( random.random() > 0.5) : 
                    new = random.choice(data.newLife)
                    xPos = data.animals[index].pos[0]
                    yPos = data.animals[index].pos[1]
                    organism = None
                    if ( new == 0 ): 
                        organism = A(xPos, yPos, 0)
                        data.A.add(organism)
                    if ( new == 1 ): 
                        organism = B(xPos, yPos, 0)
                        data.B.add(organism)
                    if ( new ==2 ): 
                        organism = C(xPos, yPos, 0)
                        data.C.add(organism)
                    if ( new ==3 ): 
                        organism = D(xPos, yPos, 0)
                        data.D.add(organism)
                    newAnimals.append( organism)
                    organism.zone = data.gs.add(organism, xPos, yPos)
        data.animals = newAnimals
        
        if ( virus.age < virus.maxAge) : 
            newVirus.add(virus)
    data.virus = newVirus
