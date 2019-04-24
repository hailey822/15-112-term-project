####################################
# Main Mode
####################################

from tkinter import *
from PIL import Image
from PIL import ImageTk

from species import *
from speciesA import *
from speciesB import *
from speciesC import * 
from speciesD import *
 
from food import *
from wetland import *

import numpy 
import random
from graph import *

def MainKeyPressed(event, data):
    if ( event.keysym == "Return"):
        data.wetland.update()
    if ( event.keysym == "p"):
        data.paused = not data.paused

def MainRedrawAll(canvas, data):
    data.wetland.draw(canvas)
    for food  in data.foods: food.draw(canvas)
    for animal in data.animals: 
        animal.draw(canvas)
    graphWrapper(canvas, data)
    pause(canvas, data)
    canvas.create_image(data.width*0.9, 0, image = data.guidebutton, anchor="nw")
    

def MainMousePressed(event, data):
    newGraphIndex = clickGraphSelector(event.x, event.y, data.width*0.805, data.width*0.965, data.height*0.97)
    if ( newGraphIndex != -1 ) : 
        data.graphIndex = newGraphIndex 
    if ( event.x > data.width*0.75 and event.y > data.height*0.74) : return  
    if ( not data.wetland.contains(event.x, event.y)) : 
        data.wetland.add(event.x, event.y)
        
    if (  (data.width*0.9 <= event.x <= data.width) and ( 0 <= event.y <=  data.height*0.1) ):
        data.mode = "guideline"
        data.paused = True
        
def MainTimerFired(data): 
    if ( data.paused ): return 
    
    data.counter += 1
    
    # Graph Information
    graphCalculation(data)
    
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
        
        # Animals move
        data.animals[aIndex].move(data.width, data.height)
        
        # Animals age
        data.animals[aIndex].age += 1
        
        # Animals reproduce after certain age
        if ( data.animals[aIndex].age > data.animals[aIndex].grownUp ): 
            child = data.animals[aIndex].reproduce()
            if ( child != None) : 
                data.animals.append(child)
                if ( child.className() == "A"): data.A.add(child)
                if ( child.className() == "B"): data.B.add(child)
                if ( child.className() == "C"): data.C.add(child)
                if ( child.className() == "D"): data.D.add(child)
        
        # Animals eat food 
        fIndex = 0
        newFoods = []
        while ( fIndex < len(data.foods) ):
            if ( not data.animals[aIndex].eatFood(data.foods[fIndex]) ) : 
                newFoods.append( data.foods[fIndex] )
            fIndex += 1
        data.foods = newFoods
        
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
            data.foods.append( Food(data.animals[aIndex].pos[0], data.animals[aIndex].pos[1]))
            
        # Animals eat pray -> reduce lifestime of the eaten organism 
        for i in range(aIndex+1, len(data.animals) ):
            data.animals[aIndex].eatPrey(data.animals[i])
        aIndex += 1
    data.animals = newAnimals


def death(data, index):
    target = data.animals[index]
    if ( target.className() == "A"):  data.A.remove(target)
    if ( target.className() == "B"):  data.B.remove(target)
    if ( target.className() == "C"):  data.C.remove(target)
    if ( target.className() == "D"):  data.D.remove(target)    

def groupBehavior(data, group):
    for animal in group : 
        animal.cohere(group)
        animal.align(group)
        animal.separate(group)
        animal.move(data.width, data.height)
        animal.acc = numpy.array([0, 0])

def pause(canvas, data):
    
    canvas.create_rectangle(0, 0, 150, 50, fill="white", width=0)
    canvas.create_oval( 10, 10, 40, 40, fill="white")
    if ( data.paused) : 
        canvas.create_polygon( 20, 15, 20, 35, 35, 25, fill="black")
    else : 
        canvas.create_rectangle( 17, 18, 22, 32, fill="black")
        canvas.create_rectangle( 27, 18, 32, 32, fill="black")
    canvas.create_text( 100, 25, text="press \"p\" to \npause/resume", anchor = "center")