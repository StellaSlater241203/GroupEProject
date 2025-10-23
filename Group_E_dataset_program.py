import tkinter
import random
import math

rEyeX = 0 # defining these now so we don't have to do it in every function
rEyeY = 0
lEyeX = 0
lEyeY = 0
noseX = 0
noseY = 0
mouthX = 0
mouthY = 0

def allowed_positions(rEyeX, rEyeY, lEyeX, lEyeY, noseX, noseY, mouthX, mouthY):
    #acceptable region for eyes:
    rEyeCircle = 1025 #just to initiate the variables so the while loop works, will always fail the first time
    
    while rEyeCircle > 1024: #would be outside the circle part of the border
        rEyeX = random.randint(74, 106) #bottom edge border
        rEyeY = random.randint(134, 166) #inside edge border
        rEyeCircle = ((rEyeX-106)**2)+((rEyeY-134)**2) #equation of the circle that borders the acceptable region
    
    rEyeYinvert = 256 - rEyeY #0,0 in tkinter is the top left corner not the bottom left corner, made all the boundaries in desmos so they assume 0,0 is bottom left
    
    lEyeX = 256 - rEyeX + random.randint(-3,3)
    lEyeYinvert = rEyeYinvert + random.randint(-3,3) #acceptable region for left eye is symmetrical about the middle of the face +- 3 pixels left right up or down

    #acceptable region for nose
    noseX = random.randint(122, 134)
    noseY = random.randint(110, (rEyeY-10)) #acceptable region for the nose, under the right eye by 6 pixels (midpoint to bottom of right eye is 6 pixels, then another 6)
    noseYinvert = 256 - noseY #same 0,0 coordinate fix

    #acceptable region for mouth
    mouthX = random.randint(122,134)
    mouthY = random.randint(64, (noseY-32)) #acceptable region for the mouth, under the nose by 8 pixels (this coord is the top of the nose, and it's 24 pixels long)
    mouthYinvert = 256 - mouthY #same 0,0 coordinate fix

    checksList = []
    for i in range(0,10):
        check = random.randint(0,100)
        checksList.append(check)
        
    generate_features(rEyeX, rEyeYinvert, lEyeX, lEyeYinvert, noseX, noseYinvert, mouthX, mouthYinvert, checksList) #pass all the coordinates to the feature generation function along with the list of random checks for feature shapes



def create_random(rEyeX, rEyeY, lEyeX, lEyeY, noseX, noseY, mouthX, mouthY):
    #faceOval = (((x-128)**2)/(76**2)) + (((y-128)**2)/(96**2)), the orignal face equation
    while ((((rEyeX)-128)**2)/(60**2)) + ((((rEyeY)-128)**2)/(86**2)) >= 1:
        rEyeX = random.randint (52,204)
        rEyeY = random.randint (32,224) #keep generating coordinates while the eye is outside slighty shrunk version of the face, to ensure the entire eye makes it inside
    canvas.create_oval((rEyeX-12), (rEyeY+6), (rEyeX+12), (rEyeY-6)) #same creation instructions as the create_face function

    while ((((lEyeX)-128)**2)/(60**2)) + ((((lEyeY)-128)**2)/(86**2)) >= 1:
        lEyeX = random.randint (52,204)
        lEyeY = random.randint (32,224) #keep generating coordinates while the eye is outside slighty shrunk version of the face, to ensure the entire eye makes it inside
    canvas.create_oval((lEyeX-12), (lEyeY+6), (lEyeX+12), (lEyeY-6))

    while ((((noseX)-128)**2)/(66**2)) + ((((noseY+12)-128)**2)/(86**2)) >= 1:
        noseX = random.randint (52,204)
        noseY = random.randint (32,224) #keep generating coordinates while the nose is outside slighty more shrunk version of the face, to ensure the entire nose makes it inside
    canvas.create_polygon(noseX, noseY, (noseX-6), (noseY+24), (noseX+6), (noseY+24), outline="black", fill="")

    while ((((mouthX)-128)**2)/(56**2)) + ((((mouthY+9)-128)**2)/(76**2)) >= 1:
        mouthX = random.randint (52,204)
        mouthY = random.randint (32,224) #keep generating coordinates while the mouth is outside slighty more shrunk version of the face, to ensure the entire mouth makes it inside
    canvas.create_arc((mouthX-16), mouthY, (mouthX+16), (mouthY+18), start=0, extent=-180)



def rotate_shape(points, angleDeg, cx, cy): #rotation function, uses 2d rotation matrix, parameters taken in are the original points of the shape, the angle it needs to be rotated to, and the centre points of rotation
    a = math.radians(angleDeg) #inputted angle to radians
    cosa = math.cos(a)
    sina = math.sin(a) #sin and cos of the angle
    out = [] #creates a tuple to return
    for i in range(0, len(points), 2): #for loop to go through the original points, every 2 because the list goes x, y, x, y...
        x = points[i] - cx
        y = points[i+1] - cy #original point - point of rotation, rotation matrix works around the origin
        xr = x*cosa - y*sina + cx
        yr = x*sina + y*cosa + cy #2d rotation matrix performed, centre of rotation added back on
            #out.extend([xr, yr])
        out.append(xr)
        out.append(yr) #new coordinates appended to the tuple

    return out #basically the code from this forum https://www.daniweb.com/programming/software-development/threads/358903/rotating-canvas-item-tkinter



def generate_features(rEyeX, rEyeY, lEyeX, lEyeY, noseX, noseY, mouthX, mouthY, checksList):

    
    eyeCoords = [rEyeX, rEyeY, lEyeX, lEyeY] #list of eye coordinates to make looping easier, and to pass into the function
    generate_eye_shapes(eyeCoords, checksList)



    canvas.create_polygon(noseX, noseY, (noseX-6), (noseY+24), (noseX+6), (noseY+24), outline="black", fill="") #create the nose, 3 points just means this is a triangle

    canvas.create_arc((mouthX-16), mouthY, (mouthX+16), (mouthY+18), start=0, extent=-180) #create the mouth, a semi-circle 32 across and 18 down, -180 so the arc sweeps down and not up.



def generate_eye_shapes(eyeCoords, checksList):

    j = 0 #to know which iteration is the second eye (to check if they should match)
    eyeCheck = random.randint(0,100) #chance that the eyes will match
    previousShape = 0 #to store the shape of the previous eye if they are to match
    eShapeCheck = 0 #current eye shape to be used in if statements

    sizes = []
    size_check = random.randint(0,100)
    if size_check <= 40:
        size = random.uniform(0.4,2.5)
        sizes.append(size)
        sizes.append(size + random.uniform(-0.2,0.2)) #40% chance of similar sized eyes
    else:
        sizes.append(random.uniform(0.4,2.5))
        sizes.append(random.uniform(0.4,2.5))  

    for i in range(0,3,2): #loop through the eye coordinates list, every 2 to get x and y pairs
        if checksList[j] <= 70: #70% chance to get a non-oval eye shape
            eShapeCheck = random.randint(1,8) #randomly choose eye shape
            if j == 1 and eyeCheck <= 80: 
                eShapeCheck = previousShape #second eye has an 80% chance to match the first eye


            if eShapeCheck == 0:
                canvas.create_oval((eyeCoords[i]-(12*sizes[j])), (eyeCoords[i+1]+(6*sizes[j])), (eyeCoords[i]+(12*sizes[j])), (eyeCoords[i+1]-(6*sizes[j]))) #oval (runs if eShapeCheck is 0, happens when )
            if eShapeCheck == 1:
                canvas.create_oval((eyeCoords[i]-(9*sizes[j])), (eyeCoords[i+1]+(9*sizes[j])), (eyeCoords[i]+(9*sizes[j])), (eyeCoords[i+1]-(9*sizes[j]))) #circle
            if eShapeCheck == 2:
                canvas.create_polygon((eyeCoords[i]-(9*sizes[j])), (eyeCoords[i+1]+(9*sizes[j])), (eyeCoords[i]-(9*sizes[j])), (eyeCoords[i+1]-(9*sizes[j])), (eyeCoords[i]+(9*sizes[j])), (eyeCoords[i+1]-(9*sizes[j])), (eyeCoords[i]+(9*sizes[j])), (eyeCoords[i+1]+(9*sizes[j])), outline="black", fill="") #square
            if eShapeCheck == 3:
                canvas.create_polygon((eyeCoords[i]-(12*sizes[j])), (eyeCoords[i+1]+(6*sizes[j])), (eyeCoords[i]-(12*sizes[j])), (eyeCoords[i+1]-(6*sizes[j])), (eyeCoords[i]+(12*sizes[j])), (eyeCoords[i+1]-(6*sizes[j])), (eyeCoords[i]+(12*sizes[j])), (eyeCoords[i+1]+(6*sizes[j])), outline="black", fill="") #rectangle
            if eShapeCheck == 4:
                canvas.create_line((eyeCoords[i]-(8*sizes[j])), eyeCoords[i+1], (eyeCoords[i]-(9*sizes[j])), (eyeCoords[i+1]-(4*sizes[j])), (eyeCoords[i]-(5*sizes[j])), (eyeCoords[i+1]-(9*sizes[j])), eyeCoords[i], (eyeCoords[i+1]-(5*sizes[j])), smooth=1)
                canvas.create_line((eyeCoords[i]+(8*sizes[j])), eyeCoords[i+1], (eyeCoords[i]+(9*sizes[j])), (eyeCoords[i+1]-(4*sizes[j])), (eyeCoords[i]+(5*sizes[j])), (eyeCoords[i+1]-(9*sizes[j])), eyeCoords[i], (eyeCoords[i+1]-(5*sizes[j])), smooth=1)
                canvas.create_line((eyeCoords[i]-(8*sizes[j])), eyeCoords[i+1], eyeCoords[i], (eyeCoords[i+1]+(9*sizes[j])), (eyeCoords[i]+(8*sizes[j])), eyeCoords[i+1]) #heart shape made of 3 lines
            if eShapeCheck == 5:
                canvas.create_polygon(eyeCoords[i], (eyeCoords[i+1]-(9*sizes[j])), (eyeCoords[i]+(2*sizes[j])), (eyeCoords[i+1]-(3*sizes[j])), (eyeCoords[i]+(9*sizes[j])), (eyeCoords[i+1]-(3*sizes[j])), (eyeCoords[i]+(3*sizes[j])), (eyeCoords[i+1]+(1*sizes[j])), (eyeCoords[i]+(5*sizes[j])), (eyeCoords[i+1]+(7*sizes[j])), eyeCoords[i], (eyeCoords[i+1]+(4*sizes[j])), (eyeCoords[i]-(5*sizes[j])), (eyeCoords[i+1]+(7*sizes[j])), (eyeCoords[i]-(3*sizes[j])), (eyeCoords[i+1]+(1*sizes[j])), (eyeCoords[i]-(9*sizes[j])), (eyeCoords[i+1]-(3*sizes[j])), (eyeCoords[i]-(2*sizes[j])), (eyeCoords[i+1]-(3*sizes[j])), outline="black", fill="") #star
            if eShapeCheck == 6:
                canvas.create_arc((eyeCoords[i]-(12*sizes[j])), (eyeCoords[i+1]-(12*sizes[j])), (eyeCoords[i]+(12*sizes[j])), (eyeCoords[i+1]+(12*sizes[j])), start=0, extent=-180) #semi circle
            if eShapeCheck == 7:
                canvas.create_line((eyeCoords[i]-(10*sizes[j])), eyeCoords[i+1], (eyeCoords[i]+(10*sizes[j])), eyeCoords[i+1]) #line
            if eShapeCheck == 8:
                canvas.create_line((eyeCoords[i]-(12*sizes[j])), (eyeCoords[i+1]-(6*sizes[j])), eyeCoords[i], (eyeCoords[i+1]+(6*sizes[j])), (eyeCoords[i]+(12*sizes[j])), (eyeCoords[i+1]-(6*sizes[j])), smooth=1) #curved line
        else:
            canvas.create_oval((eyeCoords[i]-(12*sizes[j])), (eyeCoords[i+1]+(6*sizes[j])), (eyeCoords[i]+(12*sizes[j])), (eyeCoords[i+1]-(6*sizes[j]))) #oval

        j += 1
        previousShape = eShapeCheck #store the shape of the current eye for matching purposes




for i in range (0,20):
    root = tkinter.Tk() #initialise tkinter window
    canvas = tkinter.Canvas(root, bg="white", height=256, width=256) #create canvas, 256*256
    canvas.create_oval(52, 32, 204, 224) #the face, an oval confined to the box 52,32 and 204,224
    #faceEq = (((x-128)**2)/(76**2)) + (((y-128)**2)/(96**2)) = 1 equation of an ellipse, centre point 128,128, major axis 129 (height of face), minor axis 152 (width of face)
    #for future use
    
    j = random.randint(0,20)
    if j <= 10: #just to get each type to generate 50% of the time, only for testing !!
        allowed_positions(rEyeX, rEyeY, lEyeX, lEyeY, noseX, noseY, mouthX, mouthY)  
    else:
        create_random(rEyeX, rEyeY, lEyeX, lEyeY, noseX, noseY, mouthX, mouthY)
        
    canvas.pack() #add canvas to window and show
    root.mainloop()
