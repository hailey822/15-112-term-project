# The main file, __init__.py
# This file runs the whole app "Aritificial Ecostem"

# CITATION: I got the initial tkinter code from 
# https://www.cs.cmu.edu/~112/notes/notes-graphics.html

### import 
from tkinter import *
from tkinter.font import Font

from PIL import Image
from PIL import ImageTk

sys.path.insert(0, './sources')

from main import *
from start import *
from guideline import *
###

def init(data):
    # Image IO
    imageIO(data)
    
    # Initial mode
    data.mode = "start"
    data.paused = False
    data.background = "white"
    
    # Grid System
    data.size = 100
    data.gs = GridSystem(data.size, data.width, data.height)
    
    # Ecosystem 
    #---Animals---# 
    data.animals = []
    data.A = set()
    data.B = set()
    data.C = set()
    data.D = set()
    #---Animals---# 
    data.foods = []
    #-- Virus---# E
    data.virus = set()
    populate(data)
    #---Wetland---# 
    data.wetland = WetLand()

    #---Emergency---# 
    data.spawned = False
    data.emergency = False
    data.virusTarget = None
    data.virusTargetIndex = None
    data.newLife = []
    
    #---Graph---# 
    data.graphIndex = 0
    data.popList = [ [], [], [], [], [] ]
    data.mutList = [ [], [], [], [], [] ]
    #---Guideline---# 
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
    

# Importing Images 
def imageIO(data):
    fileName= "images/ae_start.png"
    start_image = Image.open(fileName)
    ratio = start_image.size[1]/start_image.size[0] 
    start_img = start_image.resize( (data.width, int(data.width*ratio)), Image.ANTIALIAS)
    data.start = ImageTk.PhotoImage(start_img)
    
    guide_images = []
    for i in range(5):
        fileName = "images/ae_guidline%s.jpg"%str(i+1)
        guide_images.append( Image.open(fileName) )

    data.guide = []
    for i in range(5):
        ratio = guide_images[i].size[1]/guide_images[i].size[0] 
        guide = guide_images[i].resize(( int(data.width*0.8), int(data.width*0.8*ratio)), Image.ANTIALIAS)
        data.guide.append( ImageTk.PhotoImage(guide) )
    
    

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height, fill="white", width=0)
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
    data.timerDelay = 1# milliseconds
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    #root.attributes("-fullscreen", True)
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Escape>", lambda event:root.destroy())
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(1400, 800)