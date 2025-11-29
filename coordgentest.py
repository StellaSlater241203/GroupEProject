import random
import math

def check_inside_face(x,y):
    rsq = (((x-128)**2)/(76**2)) + (((y-128)**2)/(96**2))
    if rsq < 1:
        return True
    else:
        return False

def check_inside_left_eye_region(x,y,xex,yex):
    xok = False
    yok = False
    if 68 < x < xex:
        xok = True
    if 74 < y < yex:
        yok = True
    rsq = ((x-116)**2)+((y-122)**2)
    if xok == True and yok == True and rsq < 2304:
        return True
    else:
        return False 
    
def check_inside_right_eye_region(x,y,xex,yex):
    xok = False
    yok = False
    if xex < x < 188:
        xok = True
    if 74 < y < yex:
        yok = True
    rsq = ((x-140)**2)+((y-122)**2)
    if xok == True and yok == True and rsq < 2304:
        return True
    else:
        return False 

def check_inside_nose_region(x,y,xleft,xright,ytop,ybot):
    xok = False
    yok = False
    if xleft<x<xright:
        xok = True
    if ytop<y<ybot:
        yok = True
    if yok and xok:
        return True
    else:
        return False

def check_inside_mouth_region(x,y,ytop):
    xok = False
    yok = False
    if 84<x<172:
        xok = True
    if ytop<y<198:
        yok = True
    if yok and xok:
        return True
    else:
        return False



face = True
eyeChecks = [[False,True], [True,True]]
noseChecks = [[True]]
mouthChecks = [[True]]
eyeSides = ["right","left"]
eyeCentreCoords = []
noseCentreCoords = []
mouthCentreCoords = []
eyeShapes = [0,0]
noseShapes = [13]
mouthShapes = [16]
eyeSizes = [2.0,1.8]
noseSizes = [1.5]
mouthSizes = [1.8]
eyeGenOrder = [0,1]
eyeCopiesFrom = [None,0]
noseGenOrder = [0]
mouthGenOrder = [0]
alreadyY = False

for i in eyeGenOrder:
    eyeCentreCoords.append(None)

for i in eyeGenOrder:
    if eyeChecks[i][0] == True:
        copiesFromID = eyeCopiesFrom[i]
        y = eyeCentreCoords[copiesFromID][1]
        alreadyY = True
        eyeCentreCoords[i] = decide_positions(face,eyeCentreCoords,noseCentreCoords,mouthCentreCoords,eyeShapes,eyeSides[i],noseShapes,mouthShapes,eyeSizes,noseSizes,mouthSizes,0,eyeChecks[i][1],alreadyY,y)
    else:
        eyeCentreCoords[i] = decide_positions(face,eyeCentreCoords,noseCentreCoords,mouthCentreCoords,eyeShapes,eyeSides[i],noseShapes,mouthShapes,eyeSizes,noseSizes,mouthSizes,0,eyeChecks[i][1],alreadyY)

for i in noseGenOrder:
    noseCentreCoords.append(None)

for i in noseGenOrder:
    noseCentreCoords[i] = decide_positions(face,eyeCentreCoords,noseCentreCoords,mouthCentreCoords,eyeShapes,eyeSides[i],noseShapes,mouthShapes,eyeSizes,noseSizes,mouthSizes,1,eyeChecks[i][1],alreadyY)

for i in mouthGenOrder:
    mouthCentreCoords.append(None)

for i in mouthGenOrder:
    mouthCentreCoords[i] = decide_positions(face,eyeCentreCoords,noseCentreCoords,mouthCentreCoords,eyeShapes,eyeSides[i],noseShapes,mouthShapes,eyeSizes,noseSizes,mouthSizes,2,eyeChecks[i][1],alreadyY)

print(eyeCentreCoords, noseCentreCoords, mouthCentreCoords)