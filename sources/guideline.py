####################################
# Guideline Mode 
####################################

from tkinter import *

from PIL import Image
from PIL import ImageTk



def GuidelineKeyPressed(event, data):
    pass

def GuidelineRedrawAll(canvas, data):
    # background image
    canvas.create_image(data.width//2, data.height//2, image = data.guide[data.guideIndex], anchor = "center")
    
    # Change data mode to main
    canvas.create_rectangle(data.width*0.025, 10, data.width*0.085, 35, fill="white")
    canvas.create_text(data.width*0.055, 13, text="start", anchor="n")
    
    # left button 
    if ( data.guideIndex == 0):  leftColor = "gray"
    else :  leftColor = "black"
    canvas.create_oval( 10, data.height//2 - 30, 70, data.height//2 + 30, fill="white")
    canvas.create_polygon( 20 , data.height//2, 50, data.height//2 + 15, 50, data.height//2 - 15, fill=leftColor)
    
    # right button
    if ( data.guideIndex == len(data.guide)-1 ) : rightColor ="gray"
    else : rightColor = "black"
    canvas.create_oval( data.width - 70, data.height//2 - 30, data.width - 10, data.height//2 + 30, fill="white")
    canvas.create_polygon( data.width - 20 , data.height//2, data.width - 50, 
                            data.height//2 + 15, data.width -50, data.height//2 - 15, fill=rightColor)
    


def GuidelineMousePressed(event, data):

    # Change data mode to guideline
    if (  (data.width*0.025 <= event.x <= data.width*0.085) and ( 10 <= event.y <= 35) ):
        data.mode = "main"
        data.guideIndex = 0
        data.paused = False
        
    # left button click
    if (  ( 10 <= event.x <= 70) and ( data.height//2 - 30 <= event.y <= data.height//2 + 30) ):
        data.guideIndex = (data.guideIndex-1)%len(data.guide)
    
    # right button click
    if (  ( data.width - 70  <= event.x <= data.width - 10) and  ( data.height//2 - 30 <= event.y <= data.height//2 + 30) ):
        data.guideIndex = (data.guideIndex+1)%len(data.guide)
    
    
def GuidelineTimerFired(data): 
    pass