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
        
    generate_features(rEyeX, rEyeYinvert, lEyeX, lEyeYinvert, noseX, noseYinvert, mouthX, mouthYinvert, checksList)



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
    #if checksList[0] <= 20: #weighting for different a different eye shape
    rShapeCheck = random.randint(1,8)
    if rShapeCheck == 1:
        canvas.create_oval((rEyeX-9), (rEyeY+9), (rEyeX+9), (rEyeY-9)) #circle
        print("circle")
    if rShapeCheck == 2:
        canvas.create_polygon((rEyeX-9), (rEyeY+9), (rEyeX-9), (rEyeY-9), (rEyeX+9), (rEyeY-9), (rEyeX+9), (rEyeY+9), outline="black", fill="") #square
        print("square")
    if rShapeCheck == 3:
        canvas.create_polygon((rEyeX-12), (rEyeY+6), (rEyeX-12), (rEyeY-6), (rEyeX+12), (rEyeY-6), (rEyeX+12), (rEyeY+6), outline="black", fill="") #rectangle
        print("rectangle")
    if rShapeCheck == 4:
        #canvas.create_polygon() this'll be the heart when i can work out how to make one <3 heart
        print("heart")
        canvas.create_oval((rEyeX-12), (rEyeY+6), (rEyeX+12), (rEyeY-6))
    if rShapeCheck == 5:
        canvas.create_polygon(rEyeX, (rEyeY-9), (rEyeX+2), (rEyeY-3), (rEyeX+9), (rEyeY-3), (rEyeX+3), (rEyeY+1), (rEyeX+5), (rEyeY+7), rEyeX, (rEyeY+4), (rEyeX-5), (rEyeY+7), (rEyeX-3), (rEyeY+1), (rEyeX-9), (rEyeY-3), (rEyeX-2), (rEyeY-3), outline="black", fill="") #star
        print("star")
    if rShapeCheck == 6:
        canvas.create_arc((rEyeX-12), (rEyeY-12), (rEyeX+12), (rEyeY+12), start=0, extent=-180) #semi circle
        print("semi circle")
    if rShapeCheck == 7:
        canvas.create_line((rEyeX-10), rEyeY, (rEyeX+10), rEyeY) #line
        print("line")
    if rShapeCheck == 8:
        canvas.create_line((rEyeX-12), (rEyeY-6), rEyeX, (rEyeY+6), (rEyeX+12), (rEyeY-6), smooth=1) #curved line
        print("curved line")

    #canvas.create_oval((rEyeX-12), (rEyeY+6), (rEyeX+12), (rEyeY-6))
    canvas.create_oval((lEyeX-12), (lEyeY+6), (lEyeX+12), (lEyeY-6)) #create the eyes

    canvas.create_polygon(noseX, noseY, (noseX-6), (noseY+24), (noseX+6), (noseY+24), outline="black", fill="") #create the nose, 3 points just means this is a triangle

    canvas.create_arc((mouthX-16), mouthY, (mouthX+16), (mouthY+18), start=0, extent=-180) #create the mouth, a semi-circle 32 across and 18 down, -180 so the arc sweeps down and not up.



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