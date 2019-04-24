# The main file, __init__.py
# This file runs the whole app "Aritificial Ecostem"

# CITATION: I got the initial tkinter code from 
# https://www.cs.cmu.edu/~112/notes/notes-graphics.html

from tkinter import *

from PIL import Image
from PIL import ImageTk

from main import *
from start import *
from guideline import *

def init(data):
    imageIO(data)
    
    data.mode = "start"
    
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
    
    data.guideIndex = 0

def keyPressed(event, data):
    if ( data.mode == "main")  :  MainKeyPressed(event, data)
    if ( data.mode == "start") :  StartKeyPressed(event, data)
    if ( data.mode == "guideline") : GuidelineKeyPressed(event, data)
    
def redrawAll(canvas, data):
    if ( data.mode == "main") : MainRedrawAll(canvas, data)
    if ( data.mode == "start") : StartRedrawAll(canvas, data)
    if ( data.mode == "guideline") : GuidelineRedrawAll(canvas, data)
    
def mousePressed(event, data):
    if ( data.mode == "main")  : MainMousePressed(event, data)
    if ( data.mode == "start") : StartMousePressed(event, data)
    if ( data.mode == "guideline") : GuidelineMousePressed(event, data)
    
def timerFired(data): 
    if ( data.mode == "main")  : MainTimerFired(data)
    if ( data.mode == "start") : StartTimerFired(data)
    if ( data.mode == "guideline") : GuidelineTimerFired(data)
    
    
def imageIO(data):
    
    fileName= "ae_start.jpg"
    start_image = Image.open(fileName)
    ratio = start_image.size[1]/start_image.size[0] 
    start_img = start_image.resize(( int(data.width*0.9), int(data.width*0.9*ratio)), Image.ANTIALIAS)
    data.start = ImageTk.PhotoImage(start_img)
    
    guide_images = []
    for i in range(4):
        fileName = "ae_guidline%s.jpg"%str(i+1)
        guide_images.append( Image.open(fileName) )

    data.guide = []
    for i in range(4):
        ratio = guide_images[i].size[1]/guide_images[i].size[0] 
        guide = guide_images[i].resize(( int(data.width*0.9), int(data.width*0.9*ratio)), Image.ANTIALIAS)
        data.guide.append( ImageTk.PhotoImage(guide) )
        
    fileName= "ae_startbutton.jpg"
    button_image = Image.open(fileName)
    ratio = button_image.size[1]/button_image.size[0] 
    button_img = button_image.resize(( int(data.width*0.1), int(data.width*0.1*ratio)), Image.ANTIALIAS)
    data.startbutton = ImageTk.PhotoImage(button_img)
    
    fileName= "ae_guidebutton.jpg"
    button_image = Image.open(fileName)
    ratio = button_image.size[1]/button_image.size[0] 
    button_img = button_image.resize(( int(data.width*0.1), int(data.width*0.1*ratio)), Image.ANTIALIAS)
    data.guidebutton = ImageTk.PhotoImage(button_img)
    
        
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

run(1200, 800)