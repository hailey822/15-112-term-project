####################################
# Start Mode
####################################


from tkinter import *

from PIL import Image
from PIL import ImageTk

def StartKeyPressed(event, data):
    pass

def StartRedrawAll(canvas, data):
    canvas.create_image(data.width//2, data.height//2, image = data.start, anchor = "center")

def StartMousePressed(event, data):
    if (  (data.width*0.18357 <= event.x <= data.width*0.43142) and ( data.height*0.71125 <= event.y <= data.height*0.88125) ):
        data.mode = "guideline"
    if (  (data.width*0.57928 <= event.x <= data.width*0.795) and ( data.height*0.71125 <= event.y <= data.height*0.88125) ):
        data.mode = "main"

    
def StartTimerFired(data): 
    pass