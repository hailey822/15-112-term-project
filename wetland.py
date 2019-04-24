import random 
from food import * 
from shapely.geometry import Polygon, Point

# CITATION: checking if the point is inside polygon 
# http://www.ariel.com.au/a/python-point-int-poly.html

# CITATION: calculating area of irregular polygon
# https://arachnoid.com/area_irregular_polygon/

# CITATION : generating random point inside polygon 
# https://gis.stackexchange.com/questions/6412/generate-points-that-lie-inside-polygon

class WetLand(object):
    
    def __init__(self):
        
        self.currentPoints = []
       
        self.lands = []
        self.center = []
        self.area = [] 
        self.type = []
        self.ages = []
    
    def update(self):
        if ( len(self.currentPoints) > 2 ) : 
            self.lands.append(self.currentPoints)
            self.type.append("Gen")
            self.ages.append(100)
            self.center.append(self.calCenter(self.currentPoints))
            self.area.append( self.calArea(self.currentPoints))
            self.currentPoints = []
                
    def add(self, x, y):
        self.currentPoints.append((x,y))
    
    def age(self):
        index = 0 
        newAges = []
        newTypes = [] 
        newLands = []
        newCenter = []
        newArea = []
        while ( index < len(self.ages)):
            self.ages[index] -= 1
            if ( self.ages[index] > 0 ): 
                newAges.append( self.ages[index])
                newTypes.append( self.type[index])
                newLands.append( self.lands[index])
                newCenter.append( self.center[index])
                newArea.append( self.area[index])
            index += 1
        self.ages = newAges
        self.type = newTypes
        self.lands = newLands
        self.center = newCenter
        self.area = newArea
    
    # Takes decimal number and convert to Hex
    @staticmethod
    def decimalToHex(decimal):
        result = ""
        if (decimal >= 255) : decimal = 255
        if (decimal <= 0  ) : decimal = 0  
        while ( decimal > 0 ):
            digit = decimal%16
            if ( digit>= 10): 
                result = chr(digit%10 + ord("A")) + result
            else : 
                result = str(digit) + result
            decimal //= 16
        return "{:0>2}".format(result)

            
    def draw(self, canvas):
        if len(self.lands)!=0:
            for i in range(len(self.lands)): 
                hex = self.decimalToHex(255 - self.ages[i]*5)  
                if ( self.type[i] == "Gen") : 
                    color = "#FFFF%s"%hex
                    canvas.create_polygon(self.lands[i], fill=color, width=0)
                else :  
                    color = "#FF%s%s"%(hex, hex)
                    canvas.create_polygon(self.lands[i], fill=color, width=0)
        if len(self.currentPoints)!=0:
            canvas.create_polygon(self.currentPoints, fill="#FFFF00", outline = "black")

    def contains(self, x, y):
        for index in range(len(self.lands)):   
            land = self.lands[index]
            n = len(land)
            inside =False        
            p1x,p1y = land[0]
            for i in range(n+1):
                p2x,p2y = land[i % n]
                if y > min(p1y,p2y):
                    if y <= max(p1y,p2y):
                        if x <= max(p1x,p2x):
                            if p1y != p2y: xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                            if p1x == p2x or x <= xinters: inside = not inside
                p1x,p1y = p2x,p2y
            if ( inside ) : 
                if ( self.type[index] == "Death" ) : self.type[index] = "Gen"
                else                               : self.type[index] = "Death"
                return True
        return False
            
    
    def deathTrap(self, x, y):
        for index in range(len(self.lands)):  
            if ( not self.type[index] == "Death") : continue
            land = self.lands[index]
            n = len(land)
            inside =False        
            p1x,p1y = land[0]
            for i in range(n+1):
                p2x,p2y = land[i % n]
                if y > min(p1y,p2y):
                    if y <= max(p1y,p2y):
                        if x <= max(p1x,p2x):
                            if p1y != p2y: xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                            if p1x == p2x or x <= xinters: inside = not inside
                p1x,p1y = p2x,p2y
            if ( inside ) : 
                return True
        return False
    
    def generateFood(self, data):
        for indexL in range(len(self.lands)):
            if ( not self.type[indexL] == "Gen") : continue
            center = self.center[indexL]
            area = self.area[indexL]
            landPolygon = Polygon( self.lands[indexL])
            points = self.generateRandomPoint(landPolygon, area//10000)
            for point in points: 
                data.foods.append( Food(point.x, point.y))
            
    def generateRandomPoint(self, poly, num):
        (minx, miny, maxx, maxy) = poly.bounds
        points = []
        while len(points) < num:
            p = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
            if poly.contains(p):
                points.append(p)
        return points
            
            
    def calCenter(self, land):
        x = 0 
        y = 0 
        for point in land : 
            x += point[0]
            y += point[1]
        return (int(x/len(land)), int(y/len(land)))
        
    def calArea(self, land):
        a = 0
        array = land + [land[0]]
        ox,oy = array[0]
        for x,y in array[1:]:
            a += (x*oy-y*ox)
            ox,oy = x,y
        return abs(a/2)
    

    
        