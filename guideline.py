####################################
# Guideline Mode
####################################

from tkinter import *

from PIL import Image
from PIL import ImageTk

def GuidelineKeyPressed(event, data):
    pass

def GuidelineRedrawAll(canvas, data):
    canvas.create_image(data.width//2, data.height//2, image = data.guide[data.guideIndex], anchor = "center")
    canvas.create_image(0, 0, image = data.startbutton, anchor = "nw")
    
    # left button 
    if ( data.guideIndex == 0):  leftColor = "gray"
    else :  leftColor = "black"
    canvas.create_oval( 10, data.height//2 - 30, 70, data.height//2 + 30, fill="white")
    canvas.create_polygon( 15 , data.height//2, 55, data.height//2 + 20, 55, data.height//2 - 20, fill=leftColor)
    
    # right button
    if ( data.guideIndex == len(data.guide)-1 ) : rightColor ="gray"
    else : rightColor = "black"
    canvas.create_oval( data.width - 70, data.height//2 - 30, data.width - 10, data.height//2 + 30, fill="white")
    canvas.create_polygon( data.width - 15 , data.height//2, data.width - 55, 
                            data.height//2 + 20, data.width -55, data.height//2 - 20, fill=rightColor)
    
def GuidelineMousePressed(event, data):
    
    if (  (0 <= event.x <= data.startbutton.width()) and (0 <= event.y <= data.startbutton.height()) ):
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