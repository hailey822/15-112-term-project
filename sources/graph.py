### This file takes care of real-time graph of population distribution 

# current graph 
def graphWrapper(canvas, data):
    if   (data.graphIndex == 0): label = "total population"
    elif (data.graphIndex == 1): label = "species A"
    elif (data.graphIndex == 2): label = "species B"
    elif (data.graphIndex == 3): label = "species C"
    elif (data.graphIndex == 4): label = "species D"
    drawGraph(canvas, data.width, data.height, data.popList[data.graphIndex], data.mutList[data.graphIndex], label)
 
# Wraps graph elements
def drawGraph(canvas, width, height, population, mutation, label):
    canvas.create_rectangle( width*0.79, height*0.78, width*0.96, height*0.94, fill="white")
    canvas.create_text( width*0.875, height*0.77, anchor ="s", text =label)

    minW = width*0.79
    minH = height*0.78
    maxW = width*0.96
    maxH = height*0.94   
    
    canvas.create_text( width*0.785, minH,        text = "200", anchor = "e", fill="red")
    canvas.create_text( width*0.785, height*0.82, text = "150", anchor = "e", fill="red")
    canvas.create_line( minW, height*0.82 , maxW, height*0.82, fill="gainsboro")
    canvas.create_text( width*0.785, height*0.86, text = "100", anchor = "e", fill="red")
    canvas.create_line( minW, height*0.86 , maxW, height*0.86, fill="gainsboro")
    canvas.create_text( width*0.785, height*0.90, text = "50",  anchor = "e", fill="red")
    canvas.create_line( minW, height*0.90 , maxW, height*0.90, fill="gainsboro")
    canvas.create_text( width*0.785, height*0.965,text = "pop\nsize", anchor = "e", fill="red")

    canvas.create_text( width*0.965, minH,        text = "1", anchor = "w", fill="blue")
    canvas.create_text( width*0.975, height*0.965,text = "mutation\nrate", anchor = "center", fill="blue")
    
    drawGraphSelector(canvas, width*0.805, width*0.965, height*0.97)
    
    if ( len(population) <= 0) : return 
    drawPopGraph(canvas, population, minW, minH, maxW, maxH)
    drawMutationGraph(canvas, mutation, minW, minH, maxW, maxH)
    
# Graph Selector
def clickGraphSelector(x, y, minW, maxW, maxH):
    size = 10
    stepX = (maxW - minW)/5
    for i in range(5):
        pX = minW + i*stepX
        pY = maxH
        if ( distance(x, y, pX, pY) < size ) : 
            return i
    return -1

def distance(x1, y1, x2, y2):
    return ((x2-x1)**2 + (y2-y1)**2)**0.5
        
# Graph Selector UI
def drawGraphSelector(canvas, minW, maxW, maxH):
    stepX = (maxW - minW)/5
    colorList = ["grey", "#0000FF", "#FF00FF", "#FFFF00", "#00FF00"]
    size = 12
    for i in range(5):
        pX = minW + i*stepX
        pY = maxH
        color = colorList[i]
        canvas.create_oval(pX-size, pY-size, pX+size, pY+size, fill=color, width=0)

# Mutation ratio information     
def drawMutationGraph(canvas, mutation, minW, minH, maxW, maxH):  
    maxPop = 1
    minPop = 0
    stepX = (maxW - minW)/len(mutation)
    pX = 0.5*stepX + minW
    pY = maxH - mutation[0]*(maxH-minH)
    canvas.create_oval(pX-1, pY-1, pX+1, pY+1, fill="blue", width=0)
    
    for i in range(1, len(mutation)):
        # current point
        pX = 0.5*stepX + minW + i*stepX
        pY = maxH - mutation[i]*(maxH-minH)
        # previous point 
        pX0 = 0.5*stepX + minW + (i-1)*stepX
        pY0 = maxH - mutation[i-1]*(maxH-minH)
        canvas.create_oval(pX-1, pY-1, pX+1, pY+1, fill="blue", width=0)
        canvas.create_line(pX, pY, pX0, pY0, fill="blue")

# Population changes information 
def drawPopGraph(canvas, population, minW, minH, maxW, maxH):  
    maxPop = 200
    minPop = 0
    stepX = (maxW - minW)/len(population)
    pX = 0.5*stepX + minW
    ratio = (population[0]/maxPop)
    if ( ratio > 1.0) : ratio = 1.0
    pY = maxH - (population[0]/maxPop)*(maxH-minH)
    canvas.create_oval(pX-1, pY-1, pX+1, pY+1, fill="red", width=0)
    
    for i in range(1, len(population)):
        # current point
        pX = 0.5*stepX + minW + i*stepX
        ratio = (population[i]/maxPop)
        if ( ratio > 1.0) : ratio = 1.0
        pY = maxH - ratio*(maxH-minH)
        # previous point 
        pX0 = 0.5*stepX + minW + (i-1)*stepX
        ratio0 = (population[i-1]/maxPop)
        if ( ratio > 1.0) : ratio = 1.0
        pY0 = maxH - ratio0*(maxH-minH)
        canvas.create_oval(pX-1, pY-1, pX+1, pY+1, fill="red", width=0)
        canvas.create_line(pX, pY, pX0, pY0, fill="red")
        
def calMutationRate(species):
    if ( len(species) == 0 ) : return 0
    animals = set(species)
    count = 0
    for animal in animals:
        if ( animal.DNA.gene != 0): 
            count += 1
    return count/len(animals)

def graphCalculation(data):
    data.popList[0].append( len(data.animals))
    data.mutList[0].append( calMutationRate(data.animals))
    data.popList[1].append( len(data.A))
    data.mutList[1].append( calMutationRate(data.A))
    data.popList[2].append( len(data.B))
    data.mutList[2].append( calMutationRate(data.B))
    data.popList[3].append( len(data.C))
    data.mutList[3].append( calMutationRate(data.C))
    data.popList[4].append( len(data.D))
    data.mutList[4].append( calMutationRate(data.D))    
    for i in range( len(data.popList)):
        if ( len(data.popList[i]) > 50) : 
            data.popList[i].pop(0)
            data.mutList[i].pop(0)
            