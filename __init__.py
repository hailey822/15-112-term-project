# The main file, __init__.py
# This file runs the whole app "Aritificial Ecostem"

# CITATION: I got the initial tkinter code from 
# https://www.cs.cmu.edu/~112/notes/notes-graphics.html

from tkinter import *
from species import *
from food import *
import random

def init(data):
    data.animals = []
    data.foods = []
    
    for i in range(30):
        data.animals.append( Species(data.width, data.height) )
        
    for i in range(10):
        xPos = random.randint(0, data.width)
        yPos = random.randint(0, data.height)
        data.foods.append( Food(xPos, yPos) )

def keyPressed(event, data):
    pass

def redrawAll(canvas, data):
    for food  in data.foods: food.draw(canvas)
    for animal in data.animals: animal.draw(canvas)

def mousePressed(event, data): 
    data.foods.append( Food(event.x, event.y) )

def timerFired(data): 
    # Animal : Move, EatFood, energy reduction
    aIndex = 0
    newAnimals = []
    while ( aIndex < len(data.animals) ):
        
        # Animals move
        data.animals[aIndex].move(data.width, data.height)
        
        # Animals age
        data.animals[aIndex].age += 1
        
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
        data.animals[aIndex].energy -= 1
        if (data.animals[aIndex].energy > 0) : 
            newAnimals.append(data.animals[aIndex])
        else  :
            data.foods.append( Food(data.animals[aIndex].xPos, data.animals[aIndex].yPos))
            
        aIndex += 1
    
    data.animals = newAnimals
        
        

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
    data.timerDelay = 100 # milliseconds
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

run(500, 500)