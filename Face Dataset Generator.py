import tkinter
import pygame
from pygame import gfxdraw
import math
import random
from random import shuffle
import os
from math import pi
import time

'''BOUNDARY BOX NEEDS ITS SURFACE TO BE THE SAME SIZE AS IT OTHERWISE COLLISION DOESNT WORK'''

pygame.init() #initialise pygame window

CANVAS_W, CANVAS_H = 256, 256
FACE_LEFT, FACE_TOP, FACE_RIGHT, FACE_BOTTOM = 52, 32, 204, 224
CENTER = (128, 128)

#Colours
black = (0, 0, 0) 
white = (255, 255, 255)
green = (0, 255, 0)

# Define Canvas
canvas = pygame.display.set_mode((CANVAS_W, CANVAS_H))
#pygame.display.set_caption("Face Dataset Generator")
canvas.fill(white)
pygame.display.flip()


#Pregenerated face seeds:
    #decide how tf this is gonna work later, might be easier for this to be a function itself with all the pregen face data in it 

def decide_face_type():
    FACE_PROB = 0.5
    OVERLAP_PROB = 0.1

    prob = random.uniform(0.0,1.0)
    if prob < FACE_PROB:
        face = True
    else:
        face = False
    prob = random.uniform(0.0,1.0)
    if prob < OVERLAP_PROB:
        overlap = True
    else:
        overlap = False

    return(face, overlap)

def array_variable_generation():

    #Step 0: decide if face is true or false:
    face, overlap = decide_face_type()

    #Step 1: Decide how many features are going to be on the face:
    totalFeatureNumber = 0 #total number of features on the face
    featureNumbers = [] #will store 3 items, the number of each feature

    eyeIDs, featureNumbers, totalFeatureNumber = generate_number_of_features(face, totalFeatureNumber, featureNumbers, 0) #run the fucntion to determine the number of eyes and their IDs
    noseIDs, featureNumbers, totalFeatureNumber = generate_number_of_features(face, totalFeatureNumber, featureNumbers, 1) #run the function to determine the number of noses and their IDs
    mouthIDs, featureNumbers, totalFeatureNumber, allowedCopies = generate_number_of_features(face, totalFeatureNumber, featureNumbers, 2) #run the function to determine the number of noses and their IDs


    #Step 2: Decide which criteria these features will fulfill:
    eyeCheckVariable = 9
    noseCheckVariable = 4
    mouthCheckVariable = 4 #no. of checks in each category just incase these need checking at some point i cl i made these for a reason and then ate dinner and then forgot what the reason was so xxx
    EYE_CHECK_PROBS = [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]
    '''Probabilities to have an eye mirror/be the same as aspects of another:
    1. Size (with slight randomness), 50% chance
    2. Shape, 50% chance
    3. Rotation mirrored (with some randomness), 50% chance
    4. Rotation same (with some randomness), 50% chance
    5. Position (with some randomness), 50% chance (only one of 4 and 5 can be true)
    Probabilities that an eye will have allowed values of aspects (only checked if its equivalent mirror check is false):
    6. Size, 50% chance
    7. Shape, 50% chance
    8. Rotation, 50% chance
    9. Position, 50% chance'''
    NOSE_CHECK_PROBS = [0.5,0.5,0.5,0.5]
    '''Probabilities that a nose will have allowed values of aspects:
    1. Size, 50% chance
    2. Shape, 50% chance
    3. Rotation, 50% chance
    4. Position, 50% chance'''
    MOUTH_CHECK_PROBS = [0.5,0.5,0.5,0.5]
    '''Probabilities that a mouth will have allowed values of aspects:
    1. Size, 50% chance
    2. Shape, 50% chance
    3. Rotation, 50% chance
    4. Position, 50% chance'''

    eyeChecks = []
    noseChecks = []
    mouthChecks = [] #2D arrays that store the boolean check values for the features

    for ID in eyeIDs:
        eyeChecks.append(generate_feature_criteria(EYE_CHECK_PROBS, face, 0))
    for ID in noseIDs:
        noseChecks.append(generate_feature_criteria(NOSE_CHECK_PROBS, face, 1))
    for ID in mouthIDs:
        mouthChecks.append(generate_feature_criteria(MOUTH_CHECK_PROBS, face, 2)) #add a check list for every feature that will be on the face

    #Step 2.5: Decide what order the eyes will generate in as they have attributes that can depend on eachother
    eyeGenOrder = []
    eyeCopiesFrom = []
    eyeGenOrder, eyeCopiesFrom, eyeChecks = eye_order(eyeIDs, eyeChecks)

    #Decide whether you're still working with a non face
    eyeFaceCheck = False
    noseFaceCheck = False
    mouthFaceCheck = False

    if allowedCopies == True and face == False:
        if eyeChecks[0][:5] == [True, True, False, True, True] or eyeChecks[0][:5] == [True, True, True, False, True] and eyeChecks[1][5:9] == [True, True, True, True]:
            eyeFaceCheck = True
        if eyeChecks[1][:5] == [True, True, False, True, True] or eyeChecks[1][:5] == [True, True, True, False, True] and eyeChecks[0][5:9] == [True, True, True, True]: #check if it randomly generated the same eye criteria as an actual face
            eyeFaceCheck =True
        else:
            eyeFaceCheck = False
    if allowedCopies == True and face == False:
        if noseChecks == [] or noseChecks[0] == [True, True, True, True]: #check if it randomly generated the same nose criteria as a face
            noseFaceCheck = True
        else:
            noseFaceCheck = False

    if allowedCopies == True and face == False:
        if mouthChecks[0] == [True, True, True, True]: #check if it randomly generated the same mouth criteria as a face
            mouthFaceCheck = True
        else:
            mouthFaceCheck = False

    if eyeFaceCheck and noseFaceCheck and mouthFaceCheck and face == False: #if it randomly generated everything to match a face but it wasnt a face already, make it a face
        face = True

    #Step 2.75: Make similar lists for the noses and mouths to be able to pass into future functions, they don't actually really serve a purpose
    noseCopiesFrom = []
    mouthCopiesFrom = []
    for i in noseIDs:
        noseCopiesFrom.append(None)
    for i in mouthIDs:
        mouthCopiesFrom.append(None)


    #Step 3: Decide on the shapes of the features
    #note: these use the indexes of the shapes listed in the function, these lists are here so they can be passed into the function to decrease the amt of code i need to write
    eyeAllowedShapes = [0,1,4,5,6,8,9] #Shapes that are allowed for the eyes no matter what shapes the other features are
    eyeDisallowedShapes = [2,3,7,10,11,12,13,14,15,16,17,18,19] #Shapes that aren't allowed for the eyes
    eyeAllowedSameShapes = [[0,1],[2,3],[4,6,8],[9,11],[12],[],[]] #Shapes that are allowed for the eyes if the same/similar shapes are used for the other features (will include some crossovers!!)
    eyeDisallowedSameShapes = [[],[],[5,7],[10],[13,14],[15,16],[17,18,19]] #Shapes that aren't allowed for the eyes if same/similar shapes are used for other features
    noseAllowedShapes = [0,1,3,4,5,6,7,9,10,12,13,15]
    noseDisallowedShapes = [2,8,11,14,16,17,18,19]
    noseAllowedSameShapes = [[0,1],[2,3],[4,5,6,7],[9,10],[12,13],[15],[]]
    noseDisallowedSameShapes = [[],[],[8],[11],[14],[16],[17,18,19]]
    mouthAllowedShapes = [0,1,3,5,8,9,11,16]
    mouthDisallowedShapes = [2,4,6,7,10,12,13,14,15,17,18,19]
    mouthAllowedSameShapes = [[0,1],[2,3],[4,5,6,8],[9,11],[14],[16],[]]
    mouthDisallowedSameShapes = [[],[],[7],[10],[12,13],[15],[17,18,19]]
    SAME_SHAPE_ALL_PROB = 0.0 #probability to generate the same shape for all the features (allowed or not)
    #i did try and set this up so that there would be a chance all the features would be squares or rectangles, for example, but i just couldnt get it to work so its being ignored for now

    eyeShapes = []
    noseShapes = []
    mouthShapes = []

    prob = random.uniform(0.0,1.0)
    if prob < SAME_SHAPE_ALL_PROB:
        sameShapesID = random.randint(0, (len(eyeAllowedShapes)-1))

        if eyeChecks != []:
            eyeShapes, eyeChecks = decide_shapes(eyeChecks, eyeAllowedSameShapes, eyeDisallowedSameShapes, eyeGenOrder, eyeCopiesFrom, 0, sameShapesID)
        if noseChecks != []:
            noseShapes, noseChecks = decide_shapes(noseChecks, noseAllowedSameShapes, noseDisallowedSameShapes, noseIDs, noseCopiesFrom, 1, sameShapesID)
        if mouthChecks != []:
            mouthShapes, mouthChecks = decide_shapes(mouthChecks, mouthAllowedSameShapes, mouthDisallowedSameShapes, mouthIDs, mouthCopiesFrom, 2, sameShapesID)

    else:
        sameShapesID = None
        if eyeChecks != []:
            eyeShapes, eyeChecks = decide_shapes(eyeChecks, eyeAllowedShapes, eyeDisallowedShapes, eyeGenOrder, eyeCopiesFrom, 0, sameShapesID)
        if noseChecks != []:
            noseShapes, noseChecks = decide_shapes(noseChecks, noseAllowedShapes, noseDisallowedShapes, noseIDs, noseCopiesFrom, 1, sameShapesID)
        if mouthChecks != []:
            mouthShapes, mouthChecks = decide_shapes(mouthChecks, mouthAllowedShapes, mouthDisallowedShapes, mouthIDs, mouthCopiesFrom, 2, sameShapesID)

    #Step 4: Decide on the size multipliers for the features:
    eyeAllowedSizes = [0.8,1.5]
    noseAllowedSizes = [0.8,1.5]
    mouthAllowedSizes = [0.8,1.5]#can mess about with these later
    minSize = 0.15
    maxSize = 3.5 #limits for disallowed sizes, can be changed for different features later if need be, which is why ive kept this out the function

    eyeSizes = []
    noseSizes = []
    mouthSizes = []

    eyeSizes, eyeChecks = decide_size(face, eyeAllowedSizes, minSize, maxSize, eyeChecks, eyeGenOrder, eyeCopiesFrom, 0, [])
    noseSizes, noseChecks = decide_size(face, noseAllowedSizes, minSize, maxSize, noseChecks, noseIDs, noseCopiesFrom, 1, eyeSizes)
    mouthSizes, mouthChecks = decide_size(face, mouthAllowedSizes, minSize, maxSize, mouthChecks, mouthIDs, mouthCopiesFrom, 2, noseSizes)

    #Step 5: Decide on the rotations for the features:
    eyeRotations = []
    noseRotations = []
    mouthRotations = []

    eyeAllowedRotations = [[0,90], [0], [0,45], [0], [0], [0], [0,180], [0,180], [0,180], [0,180], [0,180], [0,180], [0,180], [0,180], [0,180], [0,180], [0,180], [0,180], [0], [0]]
    #indexes                oval  circle square rec  line lli  curline  dcurline wcurline scircle   vsoval   hsoval    etri     ltri     wtri    ltrap    wtrap    heart   star spiral
    noseAllowedRotations = [[90], [0], [0], [90], [90], [90], [0,180], [0,180], [0,180], [0,180], [0,180], [0,180], [0,180], [0,180], [0,180], [0,180], [0,180], [0,180], [0], [0]]
    #indexes                oval circ square rec  line   lli  curline  dcurline wcurline scircle   vsoval   hsoval    etri     ltri     wtri    ltrap    wtrap    heart   star spiral
    mouthAllowedRotations = [[0], [0], [0], [0], [0], [0], [0,180], [0,180], [0,180], [0,180], [0,180], [0,180], [0,180], [0,180], [0,180], [0,180], [0,180], [0,180], [0], [0]]
    #indexes                oval circ square rec line lli  curline  dcurline wcurline scircle   vsoval   hsoval    etri     ltri     wtri    ltrap    wtrap    heart   star spiral
    #obvs some of these shapes are not allowed for these features but this still allows us to have a disallowed shape with an allowed rotation, still wont be a face, also this makes it easier for pulling into fucntions and stuff cause whatever u send in is now the same length
    

    if eyeChecks != []:
        eyeRotations, eyeChecks = decide_rotation(face, eyeChecks, eyeShapes, eyeAllowedRotations, eyeGenOrder, eyeCopiesFrom, 0)
    if noseChecks != []:
        noseRotations, noseChecks = decide_rotation(face, noseChecks, noseShapes, noseAllowedRotations, noseIDs, noseCopiesFrom, 1)
    if mouthChecks != []:
        mouthRotations, mouthChecks = decide_rotation(face, mouthChecks, mouthShapes, mouthAllowedRotations, mouthIDs, mouthCopiesFrom, 2)

    #Step 6: decide on the generation order, sort this into a masterlist of the order every single feature is generated individually
    featureGenOrder, individualGenOrder = generation_order(featureNumbers, eyeGenOrder, noseIDs, mouthIDs)

    eyeSides, eyeChecks = left_or_right_eye(face, eyeGenOrder, eyeCopiesFrom, eyeChecks)
    
    #Step 7, 8 and 9: decide on positions, ensure there are no interfeature collisions, and draw the final face!
    face = draw_face(face, featureGenOrder, featureNumbers, individualGenOrder, eyeChecks, eyeCopiesFrom, eyeSides, noseChecks, mouthChecks, eyeShapes, noseShapes, mouthShapes, eyeSizes, noseSizes, mouthSizes, eyeRotations, noseRotations, mouthRotations)

    return(face)
#decide on pregen design would be defined and called here probably xx

def generate_number_of_features(face, totalFeatureNumber, featureNumbers, currentFeature):
    maxGenCopies = [8,5,5] #generate a maximum of 8 eyes, 5 noses and 5 mouths
    defaultGenCopies = [2,1,1] #to check whether a random copy generation has the number of copies of a face
    noNoseGenCopies = [2,0,1] #other allowed copies generation
    NO_NOSE_GEN_PROB = 0.1
    DEFAULT_COPIES_PROB = 0.4

    IDs = [] #temp for this call of IDs, will be turned into the featureIDs array of whatever feature is currently being generated for

    #DECIDE ON THE NUMBER OF FEATURES
    if face == True:
        prob = random.uniform(0.0,1.0)
        if prob < NO_NOSE_GEN_PROB:
            number = noNoseGenCopies[currentFeature] #if prob less than no nose prob a face without a nose is generated
        else:
            number = defaultGenCopies[currentFeature] #face with a nose is generated
        featureNumbers.append(int(number)) #append the normal face amount of the feature currently running
        allowedCopies = True
        totalFeatureNumber += defaultGenCopies[currentFeature] #increment the total number of features by this amount

    else:  #face = False
        prob = random.uniform(0.0,1.0)
        if prob < DEFAULT_COPIES_PROB:
            number = defaultGenCopies[currentFeature] #decided on the default number of features (2 eyes, a nose and a mouth)
            totalFeatureNumber += number
        else:
            number = random.randint(0,maxGenCopies[currentFeature]) #decided on a random number of features
            totalFeatureNumber += number
        featureNumbers.append(int(number))

        if currentFeature == 2 and featureNumbers == defaultGenCopies or currentFeature == 2 and featureNumbers == noNoseGenCopies: #if it managed to generate the normal number of features for a face (this will only work properly on the 3rd call when featureNumbers is complete!!)
            allowedCopies = True #to check whether a face has been randomly generated later
        else: #if it didnt generate the normal number of features for a face
            allowedCopies = False

    #FILL IN FEATURE Ids
    for i in range(number):
        IDs.append(i)

    if currentFeature == 2:
        return(IDs, featureNumbers, totalFeatureNumber, allowedCopies)
    else:
        return(IDs, featureNumbers, totalFeatureNumber)

def generate_feature_criteria (checkList, face, currentFeature): 
    '''basically this function just decides whether some aspects of the features are going to be true or false, eg.
    will a nose be in its allowed position? Will an eye be the same shape as another eye? Just yes or no questions for now.
    all the checks will be stored in a 2D array, an array for every feature on the face we determined in the previous function.'''
    checks = []
    if face == True:
        if currentFeature == 0:
            checks = [True, True, True, True, True, True, True, True, True] #eyes
        if currentFeature == 1:
            checks = [True, True, True, True] #same for noses
        if currentFeature == 2:
            checks = [True, True, True, True] #same for mouths

    else: #face = False
        for i in checkList:
            prob = random.uniform(0.0,1.0)
            if prob < i:
                checks.append(True)
            else:
                checks.append(False) #randomly decide whether a criteria is true or false
    
    return(checks)

def eye_order(IDs, checks):
    ROTATION_MIRROR_VS_SAME_PROB = 0.5

    order = random.sample(IDs, len(IDs))
    counter = 0
    falseList = [False, False, False, False, False]
    copiesFrom = []
    for i in order:
        copiesFrom.append(None)

    for i in order:
        if counter == 0 and any(checks[i][0:5]):
            temp = falseList
            temp.extend(checks[i][5:9])
            checks[i] = temp
            copiesFrom[i] = None
        if counter > 0:
            if any(checks[i][0:5]):
                if checks[i][2] and checks[i][3]:
                    prob = random.uniform(0.0,1.0)
                    if prob < ROTATION_MIRROR_VS_SAME_PROB:
                        checks[i][2] = True
                        checks[i][3] = False
                    else:
                        checks[i][2] = False
                        checks[i][3] = True
                copiesFromID = random.sample(order[:counter], 1)
                copiesFrom[i] = copiesFromID[0]
            else:
                copiesFrom[i] = None
        if counter == 0 and not any(checks[i][0:5]):
            copiesFrom[i] = None
        
        counter += 1
    
    return(order, copiesFrom, checks)
    #if culling of the checks needs to be done do it here! might not need to though cause the matching checks can just be done first and the rest ignored if need be
        
def decide_shapes(checks, allowedShapes, disallowedShapes, genOrder, copiesFrom, currentFeature, sameShapesID):
    shapes = ["oval", "circle", "square", "rectangle", "line", "lline" "curvedline", "dcurvedline", "wcurvedline", "semicircle", "vsemioval", "hsemioval", "etriangle", "ltriangle", "wtriangle", "ltrapezium", "wtrapezium", "heart", "star", "spiral"]
    #indexes    0        1         2           3          4       5          6             7              8             9            10            11           12          13            14           15            16         17       18       19
    shapeList = [] #list to put the decided shapes in

    for i in range(len(genOrder)):
        shapeList.append(None) #makes a list as long as the number of features of None so that indexes can be properly attained later for features where features are generated out of order of their starting IDs (i.e, eyes)

    if genOrder == []:
        return([],[])
    else:
        for i in genOrder:

            if copiesFrom[i] == None or copiesFrom[i] != None and checks[i][1] == False: #if the feature doesnt copy anything from another or it does (an eye) but doesnt copy the shape:
                if currentFeature == 0 and checks[i][6] == True or currentFeature == 1 and checks[i][1] == True or currentFeature == 2 and checks [i][1] == True: #if the feature has an allowed shape
                    if sameShapesID != None and len(allowedShapes[sameShapesID]) != 0: #if the face has similar shapes for all features and this set of shapes has allowed shapes for this feature (some of them dont have shapes in the allowed as these shapes are never allowed for that feature)
                        shape = random.sample(allowedShapes[sameShapesID], 1)
                        print(shape[0], "shape chosen from function 1", currentFeature)
                        shapeList[i] = shape[0]
                        print("shapelist i func 1", shapeList[i])
                    elif sameShapesID != None and len(allowedShapes[sameShapesID]) == 0: #if the face has similar shapes for all features but none of this set of shapes are allowed for this feature
                        shape = random.sample(disallowedShapes[sameShapesID], 1) #add a disallowed one instead
                        print(shape[0], "shape chosen from function 2", currentFeature)
                        shapeList[i] = shape[0]
                        print("shapelist i func 2", shapeList[i])
                        if currentFeature == 0: #and make sure to change the checks to know this shape is disallowed now, this will be checked after the function calls to make sure the face is still a face
                            checks[i][6] = False
                        else:
                            checks[i][1] = False
                    else: #if the face has any allowed shapes for the features
                        shape = random.sample(allowedShapes, 1)
                        shapeList[i] = shape[0]

                elif currentFeature == 0 and checks[i][6] == False or currentFeature == 1 and checks[i][1] == False or currentFeature == 2 and checks [i][1] == False: #if the feature has a disallowed shape
                    if sameShapesID != None and len(disallowedShapes[sameShapesID]) != 0: #if the face has similar shapes for all features and this set of shapes has disallowed shapes for this feature (some of them dont have shapes in the adisllowed as these shapes are never disallowed for that feature)
                        shape = random.sample(disallowedShapes[sameShapesID], 1)
                        print(shape[0], "shape chosen from function 3", currentFeature)
                        shapeList[i] = shape[0]
                        print("shapelist i func 3", shapeList[i])
                    elif sameShapesID != None and len(disallowedShapes[sameShapesID]) == 0: #if the face has similar shapes for all features but none of this set of shapes are disallowed for this feature
                        shape = random.sample(allowedShapes[sameShapesID], 1) #add an sallowed one instead
                        print(shape[0], "shape chosen from fucntion 4", currentFeature)
                        shapeList[i] = shape[0]
                        print("shapelist i func 4", shapeList[i])
                        if currentFeature == 0: #and make sure to change the checks to know this shape is allowed now, this will be checked after the function calls to make sure the face is still a face
                            checks[i][6] = True
                        else:
                            checks[i][1] = True
                    else: #if the face has any disallowed shapes for the features
                        shape = random.sample(disallowedShapes, 1)
                        shapeList[i] = shape[0] #optimisation of this bit is awful, shouldve just had the function call with different parameters depending on what the value of checks for the shape was T^T

            elif copiesFrom[i] != None and checks[i][1] == True: #if the feature does copy from another and it copies the shape:
                copiesFromID = copiesFrom[i] #get the index of the feature this one copies the shape of
                shape = shapeList[copiesFromID] #get the shapeID of the feature this one copies the shape of
                if shape == None:
                    print("shape was none when copied")
                shapeList[i] = shape

                if sameShapesID != None: #check whether this shape was allowed or not and update the rules for the current feature (eye)
                    checks[i][6] = False
                    for j in range(len(allowedShapes)):
                        for k in allowedShapes[j]:
                            if k == shape:
                                checks[i][6] = True
                else:
                    checks[i][6] = False
                    for j in allowedShapes:
                        if j == shape:
                            checks[i][6] = True
            #else: #just in case it doesnt pass anything else (it shouldnt)
    
        return(shapeList, checks)

def decide_size(face, allowedSizes, minSize, maxSize, checks, genOrder, copiesFrom, currentFeature, prevSizes):
    fluctuation = 0.05 #fluctuation for sizes, so they have a chance to not be exactly the same size
    TOO_SMALL_PROB = 0.5#chance a feature will be too small if disallowed (therefore 1-this = chance to be too big)

    sizeList = []
    for i in genOrder:
        sizeList.append(None) #fills up with nones for indexing purposes

    for i in genOrder:
        if currentFeature == 0 and checks[i][0] == True: #if we're looking at eyes and it copies the size of another eye
            copiesFromID = copiesFrom[i]
            size = sizeList[copiesFromID]
            newSize = size + random.uniform((-fluctuation), fluctuation)
            if newSize < minSize:
                newSize = minSize
            sizeList[i] = newSize
            if size >= allowedSizes[0] or size <= allowedSizes[1]:
                checks[i][5] = True
            else:
                checks[i][5] = False #updating the size allowed criteria in the current eye based on what the size was it copied. Size used and not newSize cuz theres a possibilty newSize could be an unallowed/allowed size, as opposed to actual size, but that will make everythihng too complicated and i dont care cl
        
        elif face == True and currentFeature == 2 and len(prevSizes) != 0: #if its a face and we're generating a size for the mouth and a nose has been generated for this face
            mouthSizeMin = prevSizes[0] #ensure the mouth is not smaller than the nose for a face
            size = random.uniform(mouthSizeMin, allowedSizes[1])
            sizeList[i] = size

        elif currentFeature == 0 and checks[i][0] == False and checks[i][5] == True or currentFeature == 1 and checks[i][0] == True or currentFeature == 2 and checks[i][0] == True: #if its any other type of feature and has an allowed size
            size = random.uniform(allowedSizes[0], allowedSizes[1])
            sizeList[i] = size
        
        elif currentFeature == 0 and checks[i][0] == False and checks[i][5] == False or currentFeature == 1 and checks [i][0] == False or currentFeature == 2 and checks[i][0] == False: #if its none of the others then its a feature with a disallowed size
            prob = random.uniform(0.0,1.0)
            if prob < TOO_SMALL_PROB: #if its less than 0.5, feature is smaller than allowed
                size = random.uniform(minSize, allowedSizes[0])
                sizeList[i] = size
            else: #if its more than 0.5, feature is larger than allowed
                size = random.uniform(allowedSizes[1], maxSize)
                sizeList[i] = size

        else: #for the ones that dont pass any of these for some reason
            print("else ran") #this was just for testing, dont think this else runs anymore anyway but im too scared to delete it incase it destroys the whole program :D

    return(sizeList, checks)

def decide_rotation(face, checks, shapes, allowedRotations, genOrder, copiesFrom, currentFeature):
    fluctuation = 5 #allowed 10 degrees either way and still be allowed, obvs can be changed later

    rotationList = []
    for i in genOrder:
        rotationList.append(None) #fills up for indexing purposes blah blah blah been there done that fwnjkhjuwrfjnjlikwfrh

    for i in genOrder:
        if currentFeature == 0 and checks[i][2] == True: #looking at eyes and rotation is mirrored from another eye
            copiesFromID = copiesFrom[i]
            rotation = rotationList[copiesFromID]
            mirrorRot = 360 - rotation #360 - og rotation give its mirror the other side of 0
            newMirrorRot = mirrorRot + random.randint((-fluctuation), fluctuation)
            if newMirrorRot >= 360:
                newMirrorRot = newMirrorRot - 360 #make sure its never larger than 360
            rotationList[i] = newMirrorRot

            checks[i][7] = False #by default, if the rotation is allowed then this will be set to true later
            rotationIndex = shapes[i] #now to check if this rotation is allowed for this shape or not
            for j in allowedRotations[rotationIndex]:
                clockwise = j + 10
                if clockwise >= 360: #pretty sure it never will be but anyway
                    clockwise = clockwise - 360
                anticlockwise = j - 10
                if anticlockwise < 0:
                    anticlockwise = anticlockwise + 360
                if clockwise > anticlockwise:
                    if newMirrorRot <= clockwise and newMirrorRot >= anticlockwise: #between the 2 extreme allowed angles
                        checks[i][7] == True
                else:
                    if newMirrorRot >= anticlockwise or newMirrorRot <= clockwise: #between anticlockwise and 360 or between clockwise and 0
                        checks[i][7]

                

        elif currentFeature == 0 and checks[i][3] == True: #looking at eyes and rotation is copied off another eye
            copiesFromID = copiesFrom[i]
            rotation = rotationList[copiesFromID]
            newRot = rotation + random.randint((-fluctuation), fluctuation)
            if newRot >= 360:
                newRot = newRot - 360 #make sure its never larger than 360
            rotationList[i] = newRot

            checks[i][7] = False #by default, if the rotation is allowed then this will be set to true later
            rotationIndex = shapes[i] #now to check if this rotation is allowed for this shape or not
            for j in allowedRotations[rotationIndex]:
                clockwise = j + 10
                if clockwise >= 360: #pretty sure it never will be but anyway
                    clockwise = clockwise - 360
                anticlockwise = j - 10
                if anticlockwise < 0:
                    anticlockwise = anticlockwise + 360
                if clockwise > anticlockwise:
                    if newRot <= clockwise and newRot >= anticlockwise: #between the 2 extreme allowed angles
                        checks[i][7] = True
                else:
                    if newRot >= anticlockwise or newRot <= clockwise: #between anticlockwise and 360 or between clockwise and 0
                        checks[i][7] = True

        elif currentFeature == 0 and checks[i][2] == False and checks[i][3] == False and checks[i][7] == True or currentFeature == 1 and checks[i][2] == True or currentFeature == 2 and checks[i][2] == True: #if any feature that doesnt copy has an allowed rotation
            shapeIndex = shapes[i]
            rotations = allowedRotations[shapeIndex] #get all the allowed rotations for this shape
            rotation = random.sample(rotations, 1) #choose one of the allowed rotations for this shape
            flucRot = rotation[0] + random.randint((-fluctuation), fluctuation) #add random fluctuation to the allowed rotation
            if flucRot < 0:
                flucRot = flucRot + 360
            rotationList[i] = flucRot

        elif currentFeature == 0 and checks[i][2] == False and checks[i][3] == False and checks[i][7] == False or currentFeature == 1 and checks[i][2] == False or currentFeature == 2 and checks[i][2] == False: #if any feature that doesnt copy has a disallowed rotation
            shapeIndex = shapes[i]
            rotations = allowedRotations[shapeIndex] #get all allowed rotations for this shape
            disallowedRotationsLow = []
            disallowedRotationsUp = []
            for j in rotations:
                disallowedRotationsLow.append(None)
                disallowedRotationsUp.append(None) #for swapping at indexes in a minute
            counter = 0
            for j in rotations: #for every allowed rotation for this shape
                upperBound = j - fluctuation #lowerbound of allowed rotation, but upperbound of disallowed rotation
                if counter == 0:
                    if upperBound < 0:
                        upperBound = upperBound + 360
                    disallowedRotationsUp[len(disallowedRotationsUp)-1] = upperBound -1 # always moves to the end due to the moving every upperbound down one rule thingy
                else:
                    disallowedRotationsUp[counter-1] = upperBound -1 #need to move them all down one to be at the same index as their lowerbound counterpart
                lowerBound = j + fluctuation #upperbound of allowed rotation, but lowerbound of disallowed rotation
                disallowedRotationsLow[counter] = lowerBound +1
                counter += 1
            index = random.randint(0,(len(rotations)-1))
            if index == (len(disallowedRotationsLow)-1) and rotations[0] != 0: #if its the last disallowed region and the region around 0 and 360 is disallowed:
                prob = random.uniform(0.0,1.0)
                if prob < 0.5:
                    rotation = random.randint(disallowedRotationsLow[index],359) #clockwise side of 0
                else:
                    rotation = random.randint(0,disallowedRotationsUp[index]) #anticlockwise side of 0, these are both technically in the same disallowed region btw
            else:
                rotation = random.randint(disallowedRotationsLow[index], disallowedRotationsUp[index]) #any angle in the disallowed regions
            rotationList[i] = rotation

    return(rotationList, checks)

def generation_order(featureNumbers, eyeGen, noseGen, mouthGen): #to randomise the order of which the feautures are generated, to make sure every face that has loads of eyes isnt filled up with only eyes, as nothing has space to generate after them. Thought it might introduce a bit more of a spread
    featureIDs = [0,1,2]
    genOrder = random.sample(featureIDs, 3)
    individualGenOrder = []
    for i in genOrder:
        if i == 0:
            for j in eyeGen:
                individualGenOrder.append([j,0]) #append the eyes as the order they generate, and add a tag to show they are eyes, to the master order of generation list, should be a 2d array
        elif i == 1:
            for j in noseGen:
                individualGenOrder.append([j,1]) #same with noses
        else:
            for j in mouthGen:
                individualGenOrder.append([j,2]) #same with mouths

    return genOrder, individualGenOrder

def left_or_right_eye(face, genOrder, copiesFrom, checks):
    leftOrRight = []
    for i in genOrder:
        leftOrRight.append(None)

    for i in genOrder:
        if checks[i][4] == True:
            copiesFromID = copiesFrom[i]
            side = leftOrRight[copiesFromID]
            if side == "left":
                leftOrRight[i] = "right"
                checks[i][8] = True #if it copies another eye in an allowed position, set its allowed position to true, IMPORTANT LATER FOR DECIDE_POSITIONS!!!
            elif side == "right":
                leftOrRight[i] = "left"
                checks[i][8] = True
            else:
                leftOrRight[i] = None
                checks[i][8] = False #if it copies another eye in a non allowed position set its allowed position to false, ALSO IMPORTANT LATER FOR DECIDE_POSITIONS!!!

        elif checks[i][4] == False and checks[i][8] == True:
            side = random.sample(["left","right"], 1)
            #print(side[0])
            leftOrRight[i] = side[0]

        else:
            leftOrRight[i] = None

    return (leftOrRight, checks)

def draw_face(face, featureGenOrder, featureNumbers, genOrder, eyeChecks, eyeCopiesFrom, 
            eyeSides, noseChecks, mouthChecks, eyeShapes, noseShapes, mouthShapes, eyeSizes, 
            noseSizes, mouthSizes, eyeRotations, noseRotations, mouthRotations):
    largestRadius = [12,9,13,14,12,18,10,9,13,10,9,13,11,10,15,14,14,14,10,12]
    fluctuation = 5 #fluctuation in position mirrored features can be at
    eyeCentreCoords = []
    noseCentreCoords = []
    mouthCentreCoords = []
    eyeWasGenerated = []
    noseWasGenerated = []
    mouthWasGenerated = []
    generatedShapes = []

    for i in range(featureNumbers[0]):
        eyeCentreCoords.append(None)
        eyeWasGenerated.append(None)
    for i in range(featureNumbers[1]):
        noseCentreCoords.append(None)
        noseWasGenerated.append(None)
    for i in range(featureNumbers[2]):
        mouthCentreCoords.append(None)
        mouthWasGenerated.append(None)

    eyesDone = False
    noseDone = False
    mouthDone = False

    globalIndex = 0
    for feature in genOrder: #for every feature on the face in the order they generate
        collision = True
        tries = 0
        while collision == True and tries < 100:
            if feature[1] == 0: #the second item in each list is the index of the feature it is (eg 0 is an eye)
                if eyeChecks[feature[0]][4] == True: #if this eye mirrors the position of another
                    copiesFromID = eyeCopiesFrom[feature[0]] #get index of eye it mirrors
                    if eyeCentreCoords[copiesFromID] != None:
                        positionY = eyeCentreCoords[copiesFromID][1] + random.randint((-fluctuation), fluctuation) #get y coord of eye it mirrors
                        eyeCentreCoords[feature[0]], leftEyeRegionSide, rightEyeRegionSide, eyeRegionBottom, eyeSuccess = decide_positions(face, eyeShapes[feature[0]], eyeSizes[feature[0]], featureGenOrder, eyeCentreCoords, noseCentreCoords, mouthCentreCoords, eyeShapes, eyeSides[feature[0]], noseShapes, mouthShapes, eyeSizes, noseSizes, mouthSizes, 0, eyeChecks[feature[0]][8], genOrder, True, eyesDone, noseDone, mouthDone, positionY)
                    else: #the eye this one copies from didnt end up generating, so its coords are still None, and therefore cannot be copied from
                        eyeChecks[feature[0]][4] = False
                        eyeCentreCoords[feature[0]], leftEyeRegionSide, rightEyeRegionSide, eyeRegionBottom, eyeSuccess = decide_positions(face, eyeShapes[feature[0]], eyeSizes[feature[0]], featureGenOrder, eyeCentreCoords, noseCentreCoords, mouthCentreCoords, eyeShapes, eyeSides[feature[0]], noseShapes, mouthShapes, eyeSizes, noseSizes, mouthSizes, 0, eyeChecks[feature[0]][8], genOrder, False, eyesDone, noseDone, mouthDone)
                else:
                    eyeCentreCoords[feature[0]], leftEyeRegionSide, rightEyeRegionSide, eyeRegionBottom, eyeSuccess = decide_positions(face, eyeShapes[feature[0]], eyeSizes[feature[0]], featureGenOrder, eyeCentreCoords, noseCentreCoords, mouthCentreCoords, eyeShapes, eyeSides[feature[0]], noseShapes, mouthShapes, eyeSizes, noseSizes, mouthSizes, 0, eyeChecks[feature[0]][8], genOrder, False, eyesDone, noseDone, mouthDone)
                shapeInfo, rectInfo = shape_gen_info(eyeCentreCoords[feature[0]], eyeSizes[feature[0]], eyeShapes[feature[0]])
                collision, generatedShapes = draw_shape(eyeCentreCoords[feature[0]], generatedShapes, eyeShapes[feature[0]], largestRadius[eyeShapes[feature[0]]], eyeSizes[feature[0]], shapeInfo, rectInfo, 0, eyeRotations[feature[0]], [leftEyeRegionSide, rightEyeRegionSide, eyeRegionBottom], eyeSides[feature[0]])
                eyesDone = True #technically runs when the first eye is done but nothing else will run from here until all the eyes are done anyway, and this variable doesnt matter while the eyes are running
                if eyeSuccess == False:
                    eyeWasGenerated[feature[0]] = False

            elif feature[1] == 1:
                noseCentreCoords[feature[0]], noseRegionLeft, noseRegionRight, noseRegionTop, noseRegionBottom, noseSuccess = decide_positions(face, noseShapes[feature[0]], noseSizes[feature[0]], featureGenOrder, eyeCentreCoords, noseCentreCoords, mouthCentreCoords, eyeShapes, "", noseShapes, mouthShapes, eyeSizes, noseSizes, mouthSizes, 1, noseChecks[feature[0]][3], genOrder, False, eyesDone, noseDone, mouthDone)
                shapeInfo, rectInfo = shape_gen_info(noseCentreCoords[feature[0]], noseSizes[feature[0]], noseShapes[feature[0]])
                print("nose boundaries", noseRegionLeft, noseRegionRight, noseRegionTop, noseRegionBottom)
                collision, generatedShapes = draw_shape(noseCentreCoords[feature[0]], generatedShapes, noseShapes[feature[0]], largestRadius[noseShapes[feature[0]]], noseSizes[feature[0]], shapeInfo, rectInfo, 1, noseRotations[feature[0]], [noseRegionLeft, noseRegionRight, noseRegionTop, noseRegionBottom])
                noseDone = True
                if noseSuccess == False:
                    noseWasGenerated[feature[0]] = False
            else: 
                mouthCentreCoords[feature[0]], mouthRegionTop, mouthSuccess = decide_positions(face, mouthShapes[feature[0]], mouthSizes[feature[0]], featureGenOrder, eyeCentreCoords, noseCentreCoords, mouthCentreCoords, eyeShapes, "", noseShapes, mouthShapes, eyeSizes, noseSizes, mouthSizes, 2, mouthChecks[feature[0]][3], genOrder, False, eyesDone, noseDone, mouthDone)
                shapeInfo, rectInfo = shape_gen_info(mouthCentreCoords[feature[0]], mouthSizes[feature[0]], mouthShapes[feature[0]])
                collision, generatedShapes = draw_shape(mouthCentreCoords[feature[0]], generatedShapes, mouthShapes[feature[0]], 
                                                        largestRadius[mouthShapes[feature[0]]], mouthSizes[feature[0]], shapeInfo, rectInfo, 
                                                        2, mouthRotations[feature[0]], [mouthRegionTop])
                mouthDone = True
                if mouthSuccess == False:
                    mouthWasGenerated[feature[0]] = False

            tries += 1

        if tries >= 100:
            if feature[1] == 0:
                eyeCentreCoords[feature[0]] = None
                eyeWasGenerated[feature[0]] = False
            elif feature[1] == 1:
                noseCentreCoords[feature[0]] = None
                noseWasGenerated[feature[0]] = False
            elif feature[1] == 2:
                mouthCentreCoords[feature[0]] = None
                mouthWasGenerated[feature[0]] = False
        else:
            if feature[1] == 0:
                eyeWasGenerated[feature[0]] = True
            elif feature[1] == 1:
                noseWasGenerated[feature[0]] = True
            elif feature[1] == 2:
                mouthWasGenerated[feature[0]] = True

    for i in eyeWasGenerated:
        if i == False:
            face = False
    for i in mouthWasGenerated:
        if i == False:
            face = False
                

    return(face)


def shape_gen_info(centreCoords, size, shape):
    coordList = [[1,1,24,12],[1,1,18,18],[1,1,18,18],[1,1,24,12],[1,1,25,1],[1,1,33,1],[1,1,18,18],[1,1,12,24],[1,1,24,12],[1,1,18,18,1,10,19,10],[1,1,12,24,1,13,13,13],
                [1,1,24,12,1,7,25,7],[1,17,19,17,10,1],[1,25,13,25,7,1],[1,11,29,11,15,1],[3,1,11,1,13,25,1,25],[5,1,21,1,25,13,1,13],[1,1,12,12,11,1,12,12,4,12,12,19,20,12,12,19],[10,2,12,8,19,8,13,12,15,18,10,15,5,18,7,12,1,8,8,8],[9,9,4,4,5,7,8,8,5,5,12,12,1,3,16,16,1,1,20,20,-3,-1,24,24]]
    rectList = [[-13,-7,26,14],[-10,-10,20,20],[-10,-10,20,20],[-13,-7,26,14],[-13,-1,26,3],[-17,-1,34,3],[-10,-5.5,20,20],[-7,-7,14,14],[-13,-4,26,8],[-10,-5.5,20,12],[-7,-7,14,15],[-13,-4,26,9],[-10,-9,21,19],[-7,-13,15,27],[-15,-6,31,13],[-7,-13,15,27],[-13,-7,27,15],[-12,-10,24,21],[-10,-10,21,21],[-11,-11,22,20]]
    x = centreCoords[0]
    y = centreCoords[1]
    coords = []

    for i in coordList[shape]:
        coord = round(i*size)
        coords.append(coord)

    #coords = [coords[i] + (x if i % 2 == 0 else y) for i in range(len(coords))]

    print(x, y, x + math.ceil(rectList[shape][0]*size), y + math.ceil(rectList[shape][1]*size), math.ceil(rectList[shape][2]*size), math.ceil(rectList[shape][3]*size))
    rectCoords = [x + math.ceil(rectList[shape][0]*size), y + math.ceil(rectList[shape][1]*size), math.ceil(rectList[shape][2]*size), math.ceil(rectList[shape][3]*size)]
    return coords, rectCoords




def draw_shape(centreCoords, generatedShapes, shapeID, largestRadius, size, shapeInfo, rectInfo, currentFeature, rotationAngle, allowedRegionInfo = [], side = None):
    faceRect = pygame.Rect(52, 32, 152, 192) # compute bounding rectangle for the ellipse
    faceSurface = pygame.Surface(faceRect.size, pygame.SRCALPHA)
    pygame.draw.ellipse(faceSurface, black, (0, 0, *faceRect.size), 1) # draw the ellipse outline
    faceSurf = [faceSurface, faceRect]
    
    thickness = 1
    x, y = centreCoords
    extent = largestRadius * size
    shapeSurfRect = pygame.Rect(rectInfo)
    print(shapeSurfRect.size)
    shapeSurf = pygame.Surface(shapeSurfRect.size, pygame.SRCALPHA)
    
    boundaryBoxSurfRect = pygame.Rect(0, 0, 256, 256)
    boundaryBoxSurf = pygame.Surface(boundaryBoxSurfRect.size, pygame.SRCALPHA)
    
    if shapeID == 0 or shapeID == 1: # ovals and circles
        pygame.draw.ellipse(shapeSurf, black, shapeInfo, thickness)
    elif shapeID == 2 or shapeID == 3: # squares and rectangles
        pygame.draw.rect(shapeSurf, black, shapeInfo, thickness)
    elif shapeID == 4 or shapeID == 5: # lines and longer lines
        pygame.draw.line(shapeSurf, black, shapeInfo[0:2], shapeInfo[2:4], thickness)
    elif shapeID == 6 or shapeID == 7 or shapeID == 8: # curved, deep curved and wide curved lines
        pygame.draw.arc(shapeSurf, black, shapeInfo, 0, pi, thickness)
    elif shapeID == 9 or shapeID == 10 or shapeID == 11: # semi circle, vertical and horizontal semi oval
        pygame.draw.arc(shapeSurf, black, shapeInfo[0:4], 0, pi, thickness)
        pygame.draw.line(shapeSurf, black, shapeInfo[4:6], shapeInfo[6:8], thickness)
    elif shapeID == 12 or shapeID == 13 or shapeID == 14:# triangles
        pygame.draw.polygon(shapeSurf, black, (shapeInfo[0:2], shapeInfo[2:4], shapeInfo[4:6]), thickness)
    elif shapeID == 15 or shapeID == 16: # trapeziums
        pygame.draw.polygon(shapeSurf, black, (shapeInfo[0:2], shapeInfo[2:4], shapeInfo[4:6], shapeInfo[6:8]), thickness)
    elif shapeID == 18:# star
        pygame.draw.polygon(shapeSurf, black, (shapeInfo[0:2], shapeInfo[2:4], shapeInfo[4:6], shapeInfo[6:8], shapeInfo[8:10],shapeInfo[10:12], shapeInfo[12:14], shapeInfo[14:16], shapeInfo[16:18], shapeInfo[18:20]), thickness)
    elif shapeID == 17: # heart
        pygame.draw.arc(shapeSurf, black, shapeInfo[0:4], (pi/4), (5*pi/4), thickness)
        pygame.draw.arc(shapeSurf, black, shapeInfo[4:8], (7*pi/4), (3*pi/4), thickness)
        pygame.draw.line(shapeSurf, black, shapeInfo[8:10], shapeInfo[10:12], thickness)
        pygame.draw.line(shapeSurf, black, shapeInfo[12:14], shapeInfo[14:16], thickness)
    elif shapeID == 19: # spiral
        pygame.draw.arc(shapeSurf, black, shapeInfo[0:4], 0, pi, thickness)
        pygame.draw.arc(shapeSurf, black, shapeInfo[4:8], pi, 2*pi, thickness)
        pygame.draw.arc(shapeSurf, black, shapeInfo[8:12], 0, pi, thickness)
        pygame.draw.arc(shapeSurf, black, shapeInfo[12:16], pi, 2*pi, thickness)
        pygame.draw.arc(shapeSurf, black, shapeInfo[16:20], 0, pi, thickness)

    rotatedSurf = pygame.transform.rotate(shapeSurf, rotationAngle)
    print("rot surf:", rotatedSurf)
    rotatedSurfRect = rotatedSurf.get_rect(center=shapeSurfRect.center)    
    print("rot surf rect:", rotatedSurfRect)
    rotatedSurfListForCollision = [rotatedSurf, rotatedSurfRect]

    # would have ensured all features were inside their correct boxes completely, but sometimes it was causing a right eye to not generate so commenting this out for now and seeing how much it actually affects the faces.
    '''if currentFeature == 0:
        leftEyeRegionSide, rightEyeRegionSide, eyeRegionBottom = allowedRegionInfo
        if side == "left":
            EyeBoundaryBox = left_eye_boundary_box(xRight = leftEyeRegionSide, yBottom = eyeRegionBottom, surface = boundaryBoxSurf)
            if collision_detection(rotatedSurfListForCollision, EyeBoundaryBox):
                return True, generatedShapes
            else:
                pass
        elif side == "right":
            EyeBoundaryBox = right_eye_boundary_box(xLeft = rightEyeRegionSide, yBottom = eyeRegionBottom, surface = boundaryBoxSurf)
            if collision_detection(rotatedSurfListForCollision, EyeBoundaryBox):
                return True, generatedShapes
            else:
                pass
        else:
            pass
    elif currentFeature == 1:
        noseRegionLeft, noseRegionRight, noseRegionTop, noseRegionBottom = allowedRegionInfo
        NoseBoundaryBox = nose_boundary_box(xLeft = noseRegionLeft, xRight = noseRegionRight, yTop = noseRegionTop, yBottom = noseRegionBottom, surface = boundaryBoxSurf)
        if collision_detection(rotatedSurfListForCollision, NoseBoundaryBox): 
            return True, generatedShapes
        else:
            pass
    else:
        mouthRegionTop = allowedRegionInfo[0]
        MouthBoundaryBox = mouth_boundary_box(yTop = mouthRegionTop, surface = boundaryBoxSurf)
        if collision_detection(rotatedSurfListForCollision, MouthBoundaryBox):
            return True, generatedShapes
        else:
            pass'''
    

    for prevGenShape in generatedShapes:
        if collision_detection(prevGenShape, rotatedSurfListForCollision):
            return True, generatedShapes
        else:
            pass
    if collision_detection(rotatedSurfListForCollision, faceSurf):
        return True, generatedShapes
    else:
        canvas.blit(rotatedSurf, rotatedSurf.get_rect(center = rotatedSurfRect.center))
        generatedShapes.append(rotatedSurfListForCollision)
        return False, generatedShapes








# ----------- Allowed Region checks to return True or False if a coordinate is inside them -------------

def check_inside_face(x,y):
    rsq = (((x-128)**2)/(76**2)) + (((y-128)**2)/(96**2))
    if rsq < 1:
        return True
    else:
        return False

def check_inside_left_eye_region(x,y,xex=116,yex=122):
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

def check_inside_right_eye_region(x,y,xex=140,yex=122):
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

def check_inside_nose_region(x,y,xleft=100,xright=156,ytop=96,ybot=146):
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

def check_inside_mouth_region(x,y,ytop=132): 
    xok = False
    yok = False
    if 100<x<156:
        xok = True
    if ytop<y<198:
        yok = True
    if yok and xok:
        return True
    else:
        return False

# ---------------- END ------------------

# --------------- Allowed Regions as tangible shapes on their own surfaces --------------- 

def left_eye_boundary_box(xLeft = 68, xRight = 116, yTop = 74, yBottom = 122, surface = canvas):
    width = xRight - xLeft #find size of surface based on passed in size of allowed region
    height = yBottom - yTop

    lEyeBoundaryRect = pygame.Rect(xLeft - 1, yTop - 1, width+2, height+2) #create a rectangle big enough to encompass boundary box
    lEyeSurface = pygame.Surface(lEyeBoundaryRect.size, pygame.SRCALPHA) #create a surface with the size of the rectangle

    pygame.draw.line(lEyeSurface, green, (1, height-1), (width+1, height+1), 1)  # horizontal line
    pygame.draw.line(lEyeSurface, green, (width+1, height+1), (width+1, 1), 1) # vertical line
    pygame.draw.arc(lEyeSurface, green, (1, 1, 2*(48), 2*(48)), math.pi/2, math.pi, 1) # arc

    canvas.blit(lEyeSurface, lEyeSurface.get_rect(center = lEyeBoundaryRect.center))
    return [lEyeSurface, lEyeBoundaryRect]

def right_eye_boundary_box(xLeft = 140, xRight = 188, yTop = 74, yBottom = 122, surface = canvas):
    width = xRight - xLeft #find size of surface based on passed in size of allowed region
    height = yBottom - yTop
    
    rEyeBoundaryRect = pygame.Rect(xLeft - 1, yTop - 1, width+2, height+2) #create a rectangle big enough to encompass boundary box
    rEyeSurface = pygame.Surface(rEyeBoundaryRect.size, pygame.SRCALPHA) #create a surface with the size of the rectangle
    
    pygame.draw.line(rEyeSurface, green, (1, height+1), (width+1, height+1), 1)  # horizontal line
    pygame.draw.line(rEyeSurface, green, (1, height+1), (1, 1), 1) # vertical line
    pygame.draw.arc(rEyeSurface, green, (-47, 1, 2*(48), 2*(48)), math.pi, (math.pi/2), 1) # arc
    
    canvas.blit(rEyeSurface, rEyeSurface.get_rect(center = rEyeBoundaryRect.center))
    return [rEyeSurface, rEyeBoundaryRect]

def nose_boundary_box(xLeft = 100, xRight = 156, yTop = 96, yBottom = 146, surface = canvas):
    width = xRight - xLeft
    height = yBottom - yTop
    
    if width <= 0 or height <= 0:
        print("width or height is invalid. w:", width, " H:", height)
        #width = max(1, width)
        #height = max(1, height)
    noseBoundaryRect = pygame.Rect(xLeft, yTop, width, height)
    noseSurface = pygame.Surface(noseBoundaryRect.size, pygame.SRCALPHA)
    
    pygame.draw.rect(noseSurface, green, (0, 0, width, height), 1)
    
    canvas.blit(noseSurface, noseSurface.get_rect(center = noseBoundaryRect.center))
    return [noseSurface, noseBoundaryRect]

def mouth_boundary_box(xLeft = 84, xRight = 172, yTop = 132, yBottom = 198, surface = canvas):
    width = xRight - xLeft
    height = yBottom - yTop
    
    mouthBoundaryRect = pygame.Rect(xLeft, yTop, width, height)
    mouthSurface = pygame.Surface(mouthBoundaryRect.size, pygame.SRCALPHA)
    
    pygame.draw.rect(mouthSurface, green, (0, 0, width, height), 1)
    
    canvas.blit(mouthSurface, mouthSurface.get_rect(center = mouthBoundaryRect.center))
    return [mouthSurface, mouthBoundaryRect]

# --------------- END --------------- 

def collision_detection(shape1, shape2):
    surface1, pos1 = shape1
    surface2, pos2 = shape2
    mask1 = pygame.mask.from_surface(surface1)
    mask2 = pygame.mask.from_surface(surface2)
    offset_x = pos2[0] - pos1[0]
    offset_y = pos2[1] - pos1[1]
    if mask1.overlap(mask2, (offset_x, offset_y)):
        return True
    return False

def decide_positions(face, currentShape, currentSize, featureGenOrder, eyeCentreCoords, noseCentreCoords, mouthCentreCoords, eyeShapes, side, noseShapes, 
    mouthShapes, eyeSizes, noseSizes, mouthSizes, currentFeature, check, individualGenOrder, alreadyY, eyesDone, noseDone, 
    mouthDone, positionY=0):
    largestRadius = [12,9,13,14,12,18,10,9,13,10,9,13,11,10,15,14,14,14,10,12]

    #initial allowed region parameters so theyre never not defined cuz that was happening more often than id like to admit
    leftEyeSide = 116
    rightEyeSide = 140
    eyeBottom = 122
    noseTop = 96
    noseLeft = 100
    noseRight = 156
    noseBottom = 146
    mouthTop = 132
    successful = True

    if currentFeature == 0: #eye passed in
        if face == True and noseDone == True and noseCentreCoords != [] and noseCentreCoords[0] != None: #the only conditions that will change the shape of the eye allowed regions
            shapeindex = noseShapes[0] # get nose shape
            size = noseSizes[0] # and its size
            noselradius = largestRadius[shapeindex]*size # calc radius of bounding box for furthest away point from centre of the nose multiplied by size mult
            leftestPoint = math.ceil(noseCentreCoords[0][0] - noselradius) #leftmost x coord of nose
            rightestPoint = math.ceil(noseCentreCoords[0][0] + noselradius) #rightmost x coord of nose
            highestPoint = math.ceil(noseCentreCoords[0][1] - noselradius) #topmost point of nose (y=0 at top left not bottom left)
            
            if leftestPoint < leftEyeSide: #if the nose encroaches sideways into the left eye allowed region
                leftEyeSide = leftestPoint
            
            if rightEyeSide < rightestPoint: #if the nose encroaches sideways into the right eye allowed region
                rightEyeSide = rightestPoint

            if eyeBottom > highestPoint: #if the nose encroaches upwards into the eye allowed regions
                eyeBottom = highestPoint
                
        leftEyeSide -= math.ceil(largestRadius[currentShape]*currentSize)
        rightEyeSide += math.ceil(largestRadius[currentShape]*currentSize)
        eyeBottom -= math.ceil(largestRadius[currentShape]*currentSize)
            
        if check == True: #if eye is in an allowed position
            if alreadyY == True: 
                y = positionY #if y pos was copied from the function before this
            else:
                if eyeBottom <= 74:
                    y = 74
                else:
                    y = random.randint(74,eyeBottom) #y coord the same for both allowed regions, set it first
                    
            if side == "left": #if eye in left allowed position
                if leftEyeSide <= 68:
                    x = 68
                else:
                    x = random.randint(68,leftEyeSide)
                loopCount = 0
                regionCheck = check_inside_left_eye_region(x,y,leftEyeSide,eyeBottom)
                while regionCheck == False and loopCount < 100:
                    if leftEyeSide <= 68:
                        x = 68
                    else:
                        x = random.randint(68,leftEyeSide)
                    if alreadyY == True:
                        y = positionY
                    else:
                        if eyeBottom <= 74:
                            y = 74
                        else:
                            y = random.randint(74,eyeBottom)
                    loopCount +=1
                    print("stuck in loop for ", loopCount, " iterations")
                    regionCheck = check_inside_left_eye_region(x,y,leftEyeSide,eyeBottom)
                if loopCount >= 100:
                    successful = False
            
            elif side == "right": #if eye in right allowed position
                if rightEyeSide >= 188:
                    x = 188
                else:
                    x = random.randint(rightEyeSide, 188)
                loopCount = 0
                regionCheck = check_inside_right_eye_region(x,y,rightEyeSide,eyeBottom)
                while regionCheck == False and loopCount < 100:
                    if rightEyeSide >= 188:
                        x = 188
                    else:
                        x = random.randint(rightEyeSide, 188)
                    if alreadyY == True:
                        y = positionY
                    else:
                        if eyeBottom <= 74:
                            y = 74
                        else:
                            y = random.randint(74,eyeBottom)
                    loopCount +=1
                    print("stuck in loop for ", loopCount, " iterations")
                    regionCheck = check_inside_right_eye_region(x, y, rightEyeSide, eyeBottom)
                if loopCount >= 100:
                    successful = False

        else: #not in an allowed position
            if alreadyY == True:
                y = positionY
            else:
                y = random.randint(32,224)
            x = random.randint(52,204)
            loopCount = 0
            while check_inside_face(x,y) == False or check_inside_left_eye_region(x,y,leftEyeSide,eyeBottom) == True or check_inside_right_eye_region(x,y,rightEyeSide,eyeBottom) == True:
                x = random.randint(52,204)
                if alreadyY == True:
                    y = positionY
                else:
                    y = random.randint(32,224)
                loopCount += 1
            if loopCount >= 100:
                successful = False

    elif currentFeature == 1: #nose passed in
        if face == True and eyesDone == True and eyeCentreCoords[0] != None and eyeCentreCoords[1] != None:
            lowestPoints = []
            for i in range(0,len(eyeCentreCoords)): # for each eye
                ycoord = eyeCentreCoords[i][1] # get y coord of eye
                xcoord = eyeCentreCoords[i][0] # get x coord of eye
                shapeindex = eyeShapes[i] # get its shape
                size = eyeSizes[i] # and its size
                lradius = largestRadius[shapeindex]*size # calc radius of bounding box for furthest away point from centre of the eye multiplied by size mult
                lowestPoint = math.ceil(ycoord + lradius) # calc the lowest possible point of the eye
                lowestPoints.append(lowestPoint)
                if xcoord < 128:
                    leftestPoint = math.ceil(xcoord + lradius) #rightmost point of left eye (left side of nose region though)
                elif xcoord >= 128:
                    rightestPoint = math.ceil(xcoord - lradius) #leftmost point of right eye (right side of nose region though)
            
            for point in lowestPoints: #there are 2 lowest points, need to find the lowest one
                if noseTop < point: #if lowest point of the eyes encroaches into the nose allowed region
                    noseTop = point
            if noseLeft < leftestPoint: #if the rightmost point of the left eye encroaches into the nose region
                noseLeft = leftestPoint
            if noseRight > rightestPoint: #if the leftmost point of the right eye encroaches into the nose region
                noseRight = rightestPoint

        if face == True and mouthDone == True and mouthCentreCoords[0] != None:
            shapeindex = mouthShapes[0] # get mouth shape
            size = mouthSizes[0] # and its size
            lradius = largestRadius[shapeindex]*size # calc radius of bounding box for furthest away point from centre of the mouth multiplied by size mult
            highestPoint = math.ceil(mouthCentreCoords[0][1] - lradius) #topmost point of mouth (y=0 at top left not bottom left)

            if noseBottom > highestPoint: #if mouth encroaches in nose allowed region from the top
                noseBottom = highestPoint

        noseLeft += math.ceil(largestRadius[currentShape]*currentSize)
        noseRight -= math.ceil(largestRadius[currentShape]*currentSize)
        noseTop += math.ceil(largestRadius[currentShape]*currentSize)
        noseBottom -= math.ceil(largestRadius[currentShape]*currentSize)
        
        if check == True:
            if noseLeft < noseRight: #should never not be the case as collision is involved afterwards as well
                x = random.randint(noseLeft,noseRight)
            elif noseLeft == noseRight:
                x = noseLeft
            else:
                x = random.randint(noseRight,noseLeft)
                
            if noseTop < noseBottom:
                y = random.randint(noseTop,noseBottom)
            elif noseTop == noseBottom:
                y = noseTop
            else:
                y = random.randint(noseBottom,noseTop) #just incase it is, in which case we're not working with a face anyway so not too fussed where the nose goes
        
        else:
            x = random.randint(52,204)
            y = random.randint(32,224)
            while check_inside_face(x,y) == False or check_inside_nose_region(x,y,noseLeft,noseRight,noseTop,noseBottom) == True:
                x = random.randint(52,204)
                y = random.randint(32,224) #anywhere in face as long as its not in the nose allowed region

    else: #mouth passed in
        if face == True and noseDone == True and noseCentreCoords != [] and noseCentreCoords[0] != None:
            shapeindex = noseShapes[0] # get nose shape
            size = noseSizes[0] # and its size
            lradius = largestRadius[shapeindex]*size # calc radius of bounding box for furthest away point from centre of the nose multiplied by size mult
            lowestPoint = math.ceil(noseCentreCoords[0][1] + lradius) #bottommost point of nose (y=0 at top left not bottom left)

            if mouthTop < lowestPoint: #if nose encroaches into mouth allowed region
                mouthTop = lowestPoint
                
        mouthTop += math.ceil(largestRadius[currentShape]*currentSize)

        if check == True: #if in allowed region
            x = random.randint(100,156)
            print("mouth top:", mouthTop)
            if mouthTop >= 198:
                y = 98
            else:
                y = random.randint(mouthTop, 198)
        
        else: #if not in allowed region
            x = random.randint(52,204)
            y = random.randint(32,224)
            while check_inside_face(x,y) == False or check_inside_mouth_region(x,y,mouthTop) == True:
                x = random.randint(52,204)
                y = random.randint(32,224) #anywhere in face as long as its not in the mouth allowed region

    if currentFeature == 0:
        return([x,y], leftEyeSide, rightEyeSide, eyeBottom, successful)
    elif currentFeature == 1:
        return([x,y], noseLeft, noseRight, noseTop, noseBottom, successful)
    else:
        return([x,y], mouthTop, successful)


#Draw face outline
def face_outline(surface):
    faceRect = pygame.Rect(52, 32, 152, 192) # compute bounding rectangle for the ellipse
    faceSurface = pygame.Surface(faceRect.size, pygame.SRCALPHA)
    pygame.draw.ellipse(faceSurface, black, (0, 0, *faceRect.size), 1) # draw the ellipse outline
    surface.blit(faceSurface, faceSurface.get_rect(center = faceRect.center))


'''def generate_batch(canvases):
    for cv in canvases:
        cv.delete("all")
        decide_face_type()

for i in range(1): #LITERALLY ONLY FOR TESTING, JUST TO GENERATE 1 BATCH FOR EASE
    root = tkinter.Tk()
    container = tkinter.Frame(root)
    container.pack(padx=8, pady=8)
    canvases = []
    for r in range(3):
        for c in range(5):
            cv = tkinter.Canvas(container, width=CANVAS_W, height=CANVAS_H, bg="white")
            cv.grid(row=r, column=c, padx=4, pady=4)
            canvases.append(cv)

    generate_batch(canvases)
    #root.mainloop()'''

fileCounter= 0
for i in range (15):
    canvas.fill(white)
    face_outline(canvas)
    face = array_variable_generation()
    if face:
        faceString = "Face"
    else:
        faceString = "Not Face"
    pygame.display.set_caption(f"{faceString} - {i}") #this is just for testing
    pygame.display.flip()
    time.sleep(1.5)
    '''filename = str(fileCounter)+".png"
    if face == True:
        filepath = os.path.join(os.getcwd(),"face",str(filename))
    else:
        filepath = os.path.join(os.getcwd(),"non_face",str(filename))
    pygame.image.save(canvas, filepath)
    fileCounter += 1  
    time.sleep(3)
print("done")


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    pygame.display.flip()


pygame.quit()