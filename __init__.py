# The main file, __init__.py
# This file runs the whole app "Aritificial Ecostem"

# CITATION: I got the initial tkinter code from 
# https://www.cs.cmu.edu/~112/notes/notes-graphics.html

from tkinter import *
from PIL import Image
from PIL import ImageTk

from species import *
from speciesA import *
from speciesB import *
from speciesC import * 
from speciesD import *

from graph import *
 
from food import *
from wetland import *

import numpy 
import random


    
def init(data):
    imageIO(data)
    data.animals = []
    data.A = set()
    data.B = set()
    data.C = set()
    data.D = set()
    data.foods = []
    populate(data)
    
    data.wetland = WetLand()

    data.counter = 0
    data.paused = False
    
    data.graphIndex = 0
    data.popList = [ [], [], [], [], [] ]
    data.mutList = [ [], [], [], [], [] ]

def keyPressed(event, data):
    if ( event.keysym == "Return"):
        data.wetland.update()
    if ( event.keysym == "p"):
        data.paused = not data.paused

def redrawAll(canvas, data):
    data.wetland.draw(canvas)
    for food  in data.foods: food.draw(canvas)
    for animal in data.animals: 
        animal.draw(canvas)
    graphWrapper(canvas, data)
    pause(canvas, data)
    
    #canvas.create_image(data.width//2, data.height//2, image = data.guide[3], anchor = "center")
    
        
def mousePressed(event, data):

    newGraphIndex = clickGraphSelector(event.x, event.y, data.width*0.805, data.width*0.965, data.height*0.97)
    if ( newGraphIndex != -1 ) : 
        data.graphIndex = newGraphIndex 
    if ( event.x > data.width*0.75 and event.y > data.height*0.74) : return  
    if ( not data.wetland.contains(event.x, event.y)) : 
        data.wetland.add(event.x, event.y)
    

def timerFired(data): 
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
    

def imageIO(data):
    fileName= "ae_start.jpg"
    start_image = Image.open(fileName)
    guide_images = []
    for i in range(4):
        fileName = "ae_guidline%s.jpg"%str(i+1)
        guide_images.append( Image.open(fileName) )
    
    ratio = start_image.size[1]/start_image.size[0] 
    start_img = start_image.resize(( int(data.width*0.9), int(data.width*0.9*ratio)), Image.ANTIALIAS)
    
    data.start = ImageTk.PhotoImage(start_img)
    data.guide = []
    for i in range(4):
        ratio = guide_images[i].size[1]/guide_images[i].size[0] 
        guide = guide_images[i].resize(( int(data.width*0.9), int(data.width*0.9*ratio)), Image.ANTIALIAS)
        data.guide.append( ImageTk.PhotoImage(guide) )

def death(data, index):
    target = data.animals[index]
    if ( target.className() == "A"):  data.A.remove(target)
    if ( target.className() == "B"):  data.B.remove(target)
    if ( target.className() == "C"):  data.C.remove(target)
    if ( target.className() == "D"):  data.D.remove(target)
        
def populate(data):
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
    
    for i in range(20):
        xPos = random.randint(0, data.width)
        yPos = random.randint(0, data.height)
        organism = B(xPos, yPos, 0)
        data.B.add(organism)
        data.animals.append( organism)
    
    for i in range(30):
        xPos = random.randint(0, data.width)
        yPos = random.randint(0, data.height)
        organism = C(xPos, yPos, 0)
        data.C.add(organism)
        data.animals.append( organism)

    for i in range(30):
        xPos = random.randint(0, data.width)
        yPos = random.randint(0, data.height)
        organism = D(xPos, yPos, 0)
        data.D.add(organism)
        data.animals.append( organism)
        

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
    data.timerDelay = 1 # milliseconds
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

run(1400, 800)