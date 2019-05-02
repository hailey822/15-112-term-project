####################################
# Start Mode
####################################


from tkinter import *

from PIL import Image
from PIL import ImageTk

def StartKeyPressed(event, data):
    pass

def StartRedrawAll(canvas, data):
    # background image
    canvas.create_image(data.width//2, data.height//2, image = data.start, anchor = "center")
    
    # heading 
    textSize = data.width // 20
    canvas.create_text(data.width/2, data.height/4, text="ARTIFICIAL ECOSYSTEM",
                            font="Roboto " + str(textSize) + " bold italic")
    
    # name 
    textSize = data.width // 40
    canvas.create_text(data.width/2, data.height/4 + 100, text="by Hailey Kim",
                            font="Roboto " + str(textSize) + " bold italic")
            
    # guideline button
    canvas.create_text(data.width*0.38357, data.height*0.71125, text="guideline",
                            font="Roboto " + str(textSize) + " bold italic")
    # guideline button
    canvas.create_text(data.width*0.58928, data.height*0.71125, text="start",
                            font="Roboto " + str(textSize) + " bold italic")

def StartMousePressed(event, data):
    # guidline
    if (  (data.width*0.31642 <= event.x <= data.width*0.44785) and ( data.height*0.68 <= event.y <= data.height*0.75375) ):
        data.mode = "guideline"
    # start
    if (  (data.width*0.5514 <= event.x <= data.width*0.6264) and ( data.height*0.6875 <= event.y <= data.height*0.745) ):
        data.mode = "main"

    
def StartTimerFired(data): 
    pass