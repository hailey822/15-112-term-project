# The main file, __init__.py
# This file runs the whole app "Aritificial Ecostem"

# CITATION: I got the initial tkinter code from 
# https://www.cs.cmu.edu/~112/notes/notes-graphics.html

from tkinter import *
from species import *
from speciesA import *
from speciesB import *
from food import *
from wetland import *
import numpy 
import random

def init(data):
    data.animals = []
    data.A = set()
    data.B = set()
    data.foods = []
    data.counter = 0
    data.wetland = WetLand()
    
    for i in range(30):
            xPos = random.randint(0, data.width)
            yPos = random.randint(0, data.height)
            data.foods.append( Food(xPos, yPos) )

    for i in range(20):
        xPos = random.randint(0, data.width)
        yPos = random.randint(0, data.height)
        organism = A(xPos, yPos, 0)
        data.A.add(organism)
        data.animals.append( organism)
    
    for i in range(100):
        xPos = random.randint(0, data.width)
        yPos = random.randint(0, data.height)
        organism = B(xPos, yPos, 0)
        data.B.add(organism)
        data.animals.append( organism)


def keyPressed(event, data):
    if ( event.keysym == "Return"):
        data.wetland.update()

def redrawAll(canvas, data):
    data.wetland.draw(canvas)
    for food  in data.foods: food.draw(canvas)
    for animal in data.animals: 
        animal.draw(canvas)
        

def mousePressed(event, data): 
    if ( not data.wetland.contains(event.x, event.y)) : 
        data.wetland.add(event.x, event.y)


def timerFired(data): 
    groupBehavior(data, data.A)
    groupBehavior(data, data.B)
    data.wetland.age()
    data.counter += 1
    if ( data.counter %3 == 0):    
        xPos = random.randint(0, data.width)
        yPos = random.randint(0, data.height)
        data.foods.append( Food(xPos, yPos) )
        
    # Animal : Move, EatFood, energy reduction
    aIndex = 0
    
    newAnimals = []
    while ( aIndex < len(data.animals) ):
        
        # Animals move
        data.animals[aIndex].move(data.width, data.height)
        
        
        # Animals age
        data.animals[aIndex].age += 1
        # Reproduce after certain age
        if ( data.animals[aIndex].age > 100 ): 
            child = data.animals[aIndex].reproduce()
            if ( child != None) : 
                data.animals.append(child)
                if ( child.className() == "A"): data.A.add(child)
                if ( child.className() == "B"): data.B.add(child)
        
        # Loop through existing foods and eat 
        fIndex = 0
        newFoods = []
        while ( fIndex < len(data.foods) ):
            if ( not data.animals[aIndex].eatFood(data.foods[fIndex]) ) : 
                newFoods.append( data.foods[fIndex] )
            fIndex += 1
        data.foods = newFoods
        
        # Energy is reduced
        # remove animals without energy -> spawn food on dead places
        # Entered Death Trap
        enteredTrap = data.wetland.deathTrap(data.animals[aIndex].pos[0], data.animals[aIndex].pos[1])
        data.animals[aIndex].energy -= 1
        if (data.animals[aIndex].energy >= 0 and data.animals[aIndex].age < 200 and not enteredTrap ) : 
            newAnimals.append(data.animals[aIndex])
        else  :
            death(data, aIndex)
            data.foods.append( Food(data.animals[aIndex].pos[0], data.animals[aIndex].pos[1]))
            
        # Eat pray
        for i in range(aIndex+1, len(data.animals) ):
            if ( data.animals[aIndex].eatPrey(data.animals[i]) ) : 
                death(data, i)
                data.animals.pop(i)
                break
        aIndex += 1
    
    data.animals = newAnimals

def death(data, index):
    target = data.animals[index]
    if ( target.className() == "A"): 
        data.A.remove(target)
    if ( target.className() == "B"): 
        data.B.remove(target)
        
def groupBehavior(data, group):
    for animal in group : 
        #animal.seek(data.target)
        animal.cohere(group)
        animal.align(group)
        animal.separate(group)
        animal.move(data.width, data.height)
        animal.acc = numpy.array([0, 0])

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 50 # milliseconds
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(1000, 700)