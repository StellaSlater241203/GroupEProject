import tkinter
import pygame
import math
import random
from random import shuffle
import os

pygame.init() #initialise pygame window

CANVAS_W, CANVAS_H = 256, 256
FACE_LEFT, FACE_TOP, FACE_RIGHT, FACE_BOTTOM = 52, 32, 204, 224
CENTER = (128, 128)

#Colours
black = (0, 0, 0) 
white = (255, 255, 255)

# Define Canvas
canvas = pygame.display.set_mode((CANVAS_W, CANVAS_H))
pygame.display.set_caption("Face Dataset Generator")
canvas.fill(white)


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
    
    array_variable_generation(face, overlap)

def array_variable_generation(face, overlap):

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
    eyeAllowedSizes = [0.8,3.0]
    noseAllowedSizes = [0.8,3.0]
    mouthAllowedSizes = [0.8,3.0]#can mess about with these later
    minSize = 0.005
    maxSize = 5.0 #limits for disallowed sizes, can be changed for different features later if need be, which is why ive kept this out the function

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
    
    eyePos, nosePos, mouthPos = positions(face, featureGenOrder, featureNumbers, individualGenOrder, eyeChecks, eyeCopiesFrom, eyeSides, noseChecks, mouthChecks, eyeShapes, noseShapes, mouthShapes, eyeSizes, noseSizes, mouthSizes, eyeRotations, noseRotations, mouthRotations)



#decide on pregen design would be defined and called here probably xx

def generate_number_of_features(face, totalFeatureNumber, featureNumbers, currentFeature):
    maxGenCopies = [8,5,5] #generate a maximum of 8 eyes, 5 noses and 5 mouths
    defaultGenCopies = [2,1,1] #to check whether a random copy generation has the number of copies of a face
    noNoseGenCopies = [2,0,1] #other allowed copies generation
    NO_NOSE_GEN_PROB = 0.3
    DEFAULT_COPIES_PROB = 0.3

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
                        print(shapeList[i])
                    elif sameShapesID != None and len(allowedShapes[sameShapesID]) == 0: #if the face has similar shapes for all features but none of this set of shapes are allowed for this feature
                        shape = random.sample(disallowedShapes[sameShapesID], 1) #add a disallowed one instead
                        print(shape[0], "shape chosen from function 2", currentFeature)
                        shapeList[i] = shape[0]
                        print(shapeList[i])
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
                        print(shapeList[i])
                    elif sameShapesID != None and len(disallowedShapes[sameShapesID]) == 0: #if the face has similar shapes for all features but none of this set of shapes are disallowed for this feature
                        shape = random.sample(allowedShapes[sameShapesID], 1) #add an sallowed one instead
                        print(shape[0], "shape chosen from fucntion 4", currentFeature)
                        shapeList[i] = shape[0]
                        print(shapeList[i])
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
    fluctuation = 0.2 #fluctuation for sizes, so they have a chance to not be exactly the same size

    sizeList = []
    for i in genOrder:
        sizeList.append(None) #fills up with nones for indexing purposes

    for i in genOrder:
        if currentFeature == 0 and checks[i][0] == True: #if we're looking at eyes and it copies the size of another eye
            copiesFromID = copiesFrom[i]
            size = sizeList[copiesFromID]
            newSize = size + random.uniform((-fluctuation), fluctuation)
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
            if prob < 0.5: #if its less than 0.5, feature is smaller than allowed
                size = random.uniform(minSize, allowedSizes[0])
                sizeList[i] = size
            else: #if its more than 0.5, feature is larger than allowed
                size = random.uniform(allowedSizes[1], maxSize)
                sizeList[i] = size

        else: #for the ones that dont pass any of these for some reason
            print("else ran") #this was just for testing, dont think this else runs anymore anyway but im too scared to delete it incase it destroys the whole program

    return(sizeList, checks)

def decide_rotation(face, checks, shapes, allowedRotations, genOrder, copiesFrom, currentFeature):
    fluctuation = 10 #allowed 10 degrees either way and still be allowed, obvs can be changed later

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
        
def positions(face, featureGenOrder, featureNumbers, genOrder, eyeChecks, eyeCopiesFrom, 
            eyeSides, noseChecks, mouthChecks, eyeShapes, noseShapes, mouthShapes, eyeSizes, 
            noseSizes, mouthSizes, eyeRotations, noseRotations, mouthRotations):
    fluctuation = 5 #fluctuation mirrored features can be at
    eyeCentreCoords = []
    noseCentreCoords = []
    mouthCentreCoords = []
    wasGenerated = []

    for i in range(featureNumbers[0]):
        eyeCentreCoords.append(None)
    for i in range(featureNumbers[1]):
        noseCentreCoords.append(None)
    for i in range(featureNumbers[2]):
        mouthCentreCoords.append(None)

    globalIndex = 0
    for feature in genOrder: #for every feature on the face in the order they generate
        if feature[1] == 0: #the second item in each list is the index of the feature it is (eg 0 is an eye)
            index = feature[0] #first item is the ID of this feature
            if eyeChecks[index][4] == True: #if this eye mirrors the position of another
                copiesFromID = eyeCopiesFrom[index]
                positiony = eyeCentreCoords[copiesFromID][1] + random.randint((-fluctuation), fluctuation)
                alreadyY = True
                
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

def check_inside_mouth_region(x,y,ytop=132): #identical to the nose version, leaving it separate incase any changes need to be made to it xx
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

# --------------- Allowed Regions as tangible shapes on their own surfaces --------------- 

def left_eye_boundary_box(xLeft = 68, xRight = 116, yTop = 74, yBottom = 122, surface = canvas):
    width = xRight - xLeft + 2#find size of surface based on passed in size of allowed region
    height = yBottom - yTop + 2

    lEyeBoundaryRect = pygame.Rect(xLeft - 1, yTop - 1, width, height) #create a rectangle big enough to encompass boundary box
    lEyeSurface = pygame.Surface(lEyeBoundaryRect.size, pygame.SRCALPHA) #create a surface with the size of the rectangle

    pygame.draw.line(lEyeSurface, black, (1, height-1), (width-1, height-1), 1)  # horizontal line
    pygame.draw.line(lEyeSurface, black, (width-1, height-1), (width-1, 1), 1) # vertical line
    pygame.draw.arc(lEyeSurface, black, (1, 1, 2*(width - 2), 2*(height - 2)), math.pi/2, math.pi, 1) # arc

    surface.blit(lEyeSurface, lEyeBoundaryRect)
    return [lEyeSurface, lEyeBoundaryRect]

def right_eye_boundary_box(xLeft = 140, xRight = 188, yTop = 74, yBottom = 122, surface = canvas):
    width = xRight - xLeft + 2 #find size of surface based on passed in size of allowed region
    height = yBottom - yTop + 2
    
    rEyeBoundaryRect = pygame.Rect(xLeft - 1, yTop - 1, width, height) #create a rectangle big enough to encompass boundary box
    rEyeSurface = pygame.Surface(rEyeBoundaryRect.size, pygame.SRCALPHA) #create a surface with the size of the rectangle
    
    pygame.draw.line(rEyeSurface, black, (1, height-1), (width-1, height-1), 1)  # horizontal line
    pygame.draw.line(rEyeSurface, black, (0, height-1), (1, 1), 1) # vertical line
    pygame.draw.arc(rEyeSurface, black, (-48, 0, 2*(width - 2), 2*(height - 2)), math.pi, (math.pi/2), 1) # arc
    
    surface.blit(rEyeSurface, rEyeBoundaryRect)
    return [rEyeSurface, rEyeBoundaryRect]

def nose_boundary_box(xLeft = 100, xRight = 156, yTop = 96, yBottom = 146, surface = canvas):
    width = xRight - xLeft
    height = yBottom - yTop
    
    noseBoundaryRect = pygame.Rect(xLeft, yTop, width, height)
    noseSurface = pygame.Surface(noseBoundaryRect.size, pygame.SRCALPHA)
    
    pygame.draw.rect(noseSurface, black, (0, 0, width, height), 1)
    
    surface.blit(noseSurface, noseBoundaryRect)
    return [noseSurface, noseBoundaryRect]

def mouth_boundary_box(xLeft = 100, xRight = 156, yTop = 132, yBottom = 198, surface = canvas):
    width = xRight - xLeft
    height = yBottom - yTop
    
    mouthBoundaryRect = pygame.Rect(xLeft, yTop, width, height)
    mouthSurface = pygame.Surface(mouthBoundaryRect.size, pygame.SRCALPHA)
    
    pygame.draw.rect(mouthSurface, black, (0, 0, width, height), 1)
    
    surface.blit(mouthSurface, mouthBoundaryRect)
    return [mouthSurface, mouthBoundaryRect]

# --------------- END --------------- 

def collision_detection():
    print("help me")



def decide_positions(face, featureGenOrder, eyeCentreCoords, noseCentreCoords, mouthCentreCoords, eyeShapes, side, noseShapes, 
    mouthShapes, eyeSizes, noseSizes, mouthSizes, currentFeature, check, individualGenOrder, alreadyY, positionY):
    largestRadius = [12,9,13,14,6,18,10,9,13,10,9,13,11,10,15,14,14,14,10,12]
    surfs_and_rects = []

    if currentFeature == featureGenOrder[0]: #if first feature type to have been generated

        if currentFeature == 0: #if dealing with eyes
            if check == True and side != None: #if eye in allowed position and it has a side to generate in
                if side == "left": #generate pos in left side
                    x = random.randint(68,116)
                    if alreadyY == True:
                        y = positionY #if an eye copied from another the y coord was passed in so that doesnt change
                    else:
                        y = random.randint(74,122)
                    while check_inside_left_eye_region(x,y) == False:
                        x = random.randint(68,116)
                        if alreadyY == True:
                            y = positionY
                        else:
                            y = random.randint(74,122)
                elif side == "right": #generate pos in right side
                    x = random.randint(140,188)
                    if alreadyY == True:
                        y = positionY #if an eye copied from another the y coord was passed in so that doesnt change
                    else:
                        y = random.randint(74,122)
                    while check_inside_right_eye_region(x,y) == False:
                        x = random.randint(140,188)
                        if alreadyY == True:
                            y = positionY
                        else:
                            y = random.randint(74,122)
            else: #if its in a disallowed position
                if alreadyY == True: #if copied blah blah blah blah
                    y = positionY
                else:
                    y = random.randint(32,224)
                x = random.randint(52,204)
                while check_inside_face(x,y) == False or check_inside_left_eye_region(x,y) == True or check_inside_right_eye_region(x,y) == True:
                    x = random.randint(52,204)
                    if alreadyY == True:
                        y = positionY
                    else:
                        y = random.randint(32,224)
        
        elif currentFeature == 1: #nose
            if check == True: #in allowed pos
                x = random.randint(100,156)
                y = random.randint(96,146)
            elif check == False: #disallowed pos
                x = random.randint(52,204)
                y = random.randint(32,224)
                while check_inside_face(x,y) == False or check_inside_nose_region(x,y) == True:
                    x = random.randint(52,204)
                    y = random.randint(32,224)
                
        else: #mouth
            if check == True: #in allowed pos
                x = random.randint(100,156)
                y = random.randint(132,198)
            elif check == False: #disallowed pos
                x = random.randint(52,204)
                y = random.randint(32,224)
                while check_inside_face(x,y) == False or check_inside_mouth_region(x,y) == True:
                    x = random.randint(52,204)
                    y = random.randint(32,224)

    elif currentFeature == featureGenOrder[1] and featureGenOrder[0] == 0: # if current type of feature is the second type to be generated and the first to be generated were the eyes
        if face == True:
            if currentFeature == 1: #nose, eyes done first
                yList = [] # list of y coordinates of already generated eyes
                for i in range(0,len(eyeCentreCoords)): # for each eye
                    ycoord = eyeCentreCoords[i][1] # get y coord of eye
                    shapeindex = eyeShapes[i] # get its shape
                    size = eyeSizes[i] # and its size
                    lradius = largestRadius[shapeindex]*size # calc radius of bounding box for furthest away point from centre of the eye multiplied by size mult
                    ylowest = lradius+ycoord # calc the lowest possible point of the eye
                    yList.append(ylowest) #add the lowest point to a list
                
                currentlowest = 96 # top of the nose allowed region
                for i in yList: # for each eye's lowest coordinates 
                    if i > currentlowest: # if the eye's lowest point is lower than either the lowest eye's lowest point so far or the top of the boundary box if there have yet to be any eyes that pass it
                        currentlowest = i # set a new lowest point
                if currentlowest != 96: # if an eye has been generated with its lowest point below the top of the default allowed region
                    currentlowest = currentlowest + 5 # make the heighest point of the nose allowed region box 5 pixels lower than the lowest point of the lowest eye
                
                xLeftList = []
                xRightList = []
                for i in range(0,len(eyeCentreCoords)):
                    xcoord = eyeCentreCoords[i][0]
                    shapeindex = eyeShapes[i]
                    size = eyeSizes[i]
                    lradius = largestRadius[shapeindex]*size
                    if xcoord < 128:
                        xRightmost = xcoord + lradius
                        xLeftList.append(xRightmost)
                    else:
                        xLeftmost = xcoord - lradius
                        xRightList.append(xLeftmost)
                    
                currentFurthestR = 100
                currentFurthestL = 156
                for i in xLeftList:
                    if i > currentFurthestR:
                        currentFurthestR = i
                for i in xRightList:
                    if i < currentFurthestL:
                        currentFurthestL = i

                if currentFurthestR != 100:
                    currentFurthestR + 5
                if currentFurthestL != 156:
                    currentFurthestL - 5

                if check == True:
                    x = random.randint(currentFurthestR,currentFurthestL)
                    y = random.randint(currentlowest,146)
                
                if check == False:
                    x = random.randint(52,204)
                    y = random.randint(32,224)
                    while check_inside_face(x,y) == False or check_inside_nose_region(x,y,currentFurthestR,currentFurthestL,currentlowest) == True:
                        x = random.randint(52,204)
                        y = random.randint(32,224)
            
            else: #mouth, eyes done first
                if check == True:
                    x = random.randint(100, 156)
                    y = random.randint(132, 198)
                else:
                    x = random.randint(52, 204)
                    y = random.randint(32, 224)
                    while check_inside_face(x,y) == False or check_inside_mouth_region(x,y) == True:
                        x = random.randint(52, 204)
                        y = random.randint(32, 224)
        else: #face is not true, dont bother adjusting regions
            if currentFeature == 1: #nose, eyes done first
                if check == True:
                    x = random.randint(100, 156)
                    y = random.randint(96, 146)
                else:
                        x = random.randint(52, 204)
                        y = random.randint(32, 224)
                        while check_inside_face(x, y) == False or check_inside_nose_region == True:
                            x = random.randint(52, 204)
                            y = random.randint(32, 224)
            else:
                if check == True:
                    x = random.randint(100, 156)
                    y = random.randint(132, 198)
                else:
                    x = random.randint(52, 204)
                    y = random.randint(32, 224)
                    while check_inside_face(x,y) == False or check_inside_mouth_region(x,y) == True:
                        x = random.randint(52, 204)
                        y = random.randint(32, 224)

    elif currentFeature == featureGenOrder[1] and featureGenOrder[0] == 1: #eye or mouth if nose first 
        if face == True:
            if currentFeature == 0: # eye
                shapeindex = noseShapes[i] # get nose shape
                size = noseSizes[i] # and its size
                lradius = largestRadius[shapeindex]*size # calc radius of bounding box for furthest away point from centre of the nose multiplied by size mult
                leftestPoint = noseCentreCoords[0] - lradius
                rightestPoint = noseCentreCoords[0] + lradius
                highestPoint = noseCentreCoords[1] + lradius
                if check == True and side != None:
                    if side == "left": #if left eye
                        if highestPoint > 122: #if existing nose's highest point is above the bottom of the eye boundary box
                            if leftestPoint < 116: # if nose extends into left eye boundary
                                if alreadyY == True:
                                    y = positionY
                                    x = random.randint(68, (leftestPoint - 5))
                                    while check_inside_left_eye_region(x, y, leftestPoint, highestPoint) == False:
                                        x = random.randint(68, (leftestPoint - 5))
                                else:
                                    y = random.randint(74, (highestPoint - 5))
                                    x = random.randint(68, (leftestPoint - 5))
                                    while check_inside_left_eye_region(x, y, leftestPoint, highestPoint) == False:
                                        x = random.randint(68, (leftestPoint - 5))
                                        y = random.randint(74, (highestPoint - 5))
                            else:
                                if alreadyY == True:
                                    y = positionY
                                    x = random.randint(68, 116)
                                    while check_inside_left_eye_region(x, y, yex = highestPoint) == False:
                                        x = random.randint(68, 116)
                                else:
                                    y = random.randint(74, (highestPoint - 5))
                                    x = random.randint(68, 116)
                                    while check_inside_left_eye_region(x, y, yex = highestPoint) == False:
                                        x = random.randint(68, 116)
                                        y = random.randint(74, (highestPoint - 5))
                        else:
                            if leftestPoint < 116: # if nose extends into left eye boundary
                                if alreadyY == True:
                                    y = positionY
                                    x = random.randint(68, (leftestPoint - 5))
                                    while check_inside_left_eye_region(x, y, leftestPoint) == False:
                                        x = random.randint(68, (leftestPoint - 5))
                                else:
                                    y = random.randint(74 ,122)
                                    x = random.randint(68, (leftestPoint - 5))
                                    while check_inside_left_eye_region(x, y, leftestPoint) == False:
                                        x = random.randint(68, (leftestPoint - 5))
                                        y = random.randint(74, 122)
                            else:
                                if alreadyY == True:
                                    y = positionY
                                    x = random.randint(68, 116)
                                    while check_inside_left_eye_region(x, y) == False:
                                        x = random.randint(68, 116)
                                else:
                                    y = random.randint(74, 122)
                                    x = random.randint(68, 116)
                                    while check_inside_left_eye_region(x, y) == False:
                                        x = random.randint(68, 116)
                                        y = random.randint(74, 122)
                    elif side == "right":
                        if highestPoint > 122: #if existing nose's highest point is above the bottom of the eye boundary box
                            if rightestPoint > 140: # if nose extends into right eye boundary
                                if alreadyY == True:
                                    y = positionY
                                    x = random.randint(68, (rightestPoint + 5))
                                    while check_inside_right_eye_region(x, y, rightestPoint, highestPoint) == False:
                                        x = random.randint(68, (rightestPoint + 5))
                                else:
                                    y = random.randint(74, (highestPoint - 5))
                                    x = random.randint(68, (rightestPoint + 5))
                                    while check_inside_right_eye_region(x, y, rightestPoint, highestPoint) == False:
                                        x = random.randint(68, (rightestPoint + 5))
                                        y = random.randint(74, (highestPoint - 5))
                            else:
                                if alreadyY == True:
                                    y = positionY
                                    x = random.randint(68, 116)
                                    while check_inside_right_eye_region(x, y, yex = highestPoint) == False:
                                        x = random.randint(68, 116)
                                else:
                                    y = random.randint(74, (highestPoint - 5))
                                    x = random.randint(68, 116)
                                    while check_inside_right_eye_region(x, y, yex = highestPoint) == False:
                                        x = random.randint(68, 116)
                                        y = random.randint(74, (highestPoint - 5))
                        else:
                            if rightestPoint > 140: # if nose extends into right eye boundary
                                if alreadyY == True:
                                    y = positionY
                                    x = random.randint(68, (rightestPoint + 5))
                                    while check_inside_right_eye_region(x, y, rightestPoint) == False:
                                        x = random.randint(68, (rightestPoint + 5))
                                else:
                                    y = random.randint(74 ,122)
                                    x = random.randint(68, (rightestPoint + 5))
                                    while check_inside_right_eye_region(x, y, rightestPoint) == False:
                                        x = random.randint(68, (rightestPoint + 5))
                                        y = random.randint(74, 122)
                            else:
                                if alreadyY == True:
                                    y = positionY
                                    x = random.randint(68, 116)
                                    while check_inside_right_eye_region(x, y) == False:
                                        x = random.randint(68, 116)
                                else:
                                    y = random.randint(74, 122)
                                    x = random.randint(68, 116)
                                    while check_inside_right_eye_region(x, y) == False:
                                        x = random.randint(68, 116)
                                        y = random.randint(74, 122)
                elif check == False:
                    if alreadyY:
                        y = positionY
                        x = random.randint(52, 204)
                        while check_inside_face(x, y) == False or check_inside_left_eye_region == True or check_inside_right_eye_region == True:
                            x = random.randint(52, 204)
                    else:
                        y = random.randint(32, 224)
                        x = random.randint(52, 204)
                        while check_inside_face(x, y) == False or check_inside_left_eye_region == True or check_inside_right_eye_region == True:
                            x = random.randint(52, 204)
                            y = random.randint(32, 224)
            else: #mouth
                if check == True:
                    yList = [] # list of y coordinates of already generated noses
                    for i in range(0,len(noseCentreCoords)): # for each nose
                        ycoord = noseCentreCoords[i][1] # get y coord of centre of nose
                        shapeindex = noseShapes[i] # get its shape
                        size = noseSizes[i] # and its size
                        lradius = largestRadius[shapeindex]*size # calc radius of bounding box for furthest away point from centre of the nose multiplied by size mult
                        ylowest = lradius+ycoord # calc the lowest possible point of the nose
                        yList.append(ylowest) #add the lowest point to a list
                    
                    currentlowest = 132 # top of the mouth allowed region
                    for i in yList: # for each nose lowest coordinates 
                        if i > currentlowest: # if the nose's lowest point is lower than either the lowest nose's lowest point so far or the top of the boundary box if there have yet to be any nose that pass it
                            currentlowest = i # set a new lowest point
                    if currentlowest != 132: # if an nose has been generated with its lowest point below the top of the default allowed region
                        currentlowest = currentlowest + 5 # make the heighest point of the mouth allowed region box 5 pixels lower than the lowest point of the lowest nose
                    
                    x = random.randint(100, 156)
                    y = random.randint(currentlowest, 198)
                else:
                    x = random.randint(52 ,204)
                    y = random.ranndint(32, 224)
                    while check_inside_face(x, y) == False or check_inside_mouth_region(x, y) == True:
                        x = random.randint(52 ,204)
                        y = random.ranndint(32, 224)

    elif currentFeature == featureGenOrder[1] and featureGenOrder[0] == 2: #2nd feature, mouth done first
        if face == True:
            if currentFeature == 0:
                if check == True and side != None: #if eye in allowed position and it has a side to generate in
                    if side == "left": #generate pos in left side
                        x = random.randint(68,116)
                        if alreadyY == True:
                            y = positionY #if an eye copied from another the y coord was passed in so that doesnt change
                        else:
                            y = random.randint(74,122)
                        while check_inside_left_eye_region(x,y) == False:
                            x = random.randint(68,116)
                            if alreadyY == True:
                                y = positionY
                            else:
                                y = random.randint(74,122)
                    elif side == "right": #generate pos in right side
                        x = random.randint(140,188)
                        if alreadyY == True:
                            y = positionY #if an eye copied from another the y coord was passed in so that doesnt change
                        else:
                            y = random.randint(74,122)
                        while check_inside_right_eye_region(x,y) == False:
                            x = random.randint(140,188)
                            if alreadyY == True:
                                y = positionY
                            else:
                                y = random.randint(74,122)
                else: #if its in a disallowed position
                    if alreadyY == True: #if copied blah blah blah blah
                        y = positionY
                    else:
                        y = random.randint(32,224)
                    x = random.randint(52,204)
                    while check_inside_face(x,y) == False or check_inside_left_eye_region(x,y) == True or check_inside_right_eye_region(x,y) == True:
                        x = random.randint(52,204)
                        if alreadyY == True:
                            y = positionY
                        else:
                            y = random.randint(32,224)

            if currentFeature == 1: #nose, mouth already done
                yList = [] # list of y coordinates of already generated mouth
                for i in range(0,len(mouthCentreCoords)): # for the mouth
                    ycoord = mouthCentreCoords[i][1] # get y coord of mouth
                    shapeindex = mouthShapes[i] # get its shape
                    size = mouthSizes[i] # and its size
                    lradius = largestRadius[shapeindex]*size # calc radius of bounding box for furthest away point from centre of the  multiplied by size mult
                    yhighest = lradius-ycoord # calc the highest possible point of the mouth
                    yList.append(yhighest) #add the highest point to a list
                
                currentHighest = 146 # bottom of the nose allowed region
                for i in yList: # for mouth highest coord
                    if i < currentHighest: # if the mouths highest point encroaches into nose allowed region, shorten nose allowed region
                        currentHighest = i
                if currentHighest != 146: 
                    currentHighest = currentHighest - 5 

                if check == True:
                    x = random.randint(100,156)
                    y = random.randint(96,currentHighest)
                
                if check == False:
                    x = random.randint(52,204)
                    y = random.randint(32,224)
                    while check_inside_face(x,y) == False or check_inside_nose_region(x,y,ybot=currentHighest):
                        x = random.randint(52,204)
                        y = random.randint(32,224)

        else: #face false
            if currentFeature == 0:#eyes mouth already generated
                if check == True and side != None: #if eye in allowed position and it has a side to generate in
                    if side == "left": #generate pos in left side
                        x = random.randint(68,116)
                        if alreadyY == True:
                            y = positionY #if an eye copied from another the y coord was passed in so that doesnt change
                        else:
                            y = random.randint(74,122)
                        while check_inside_left_eye_region(x,y) == False:
                            x = random.randint(68,116)
                            if alreadyY == True:
                                y = positionY
                            else:
                                y = random.randint(74,122)
                    elif side == "right": #generate pos in right side
                        x = random.randint(140,188)
                        if alreadyY == True:
                            y = positionY #if an eye copied from another the y coord was passed in so that doesnt change
                        else:
                            y = random.randint(74,122)
                        while check_inside_right_eye_region(x,y) == False:
                            x = random.randint(140,188)
                            if alreadyY == True:
                                y = positionY
                            else:
                                y = random.randint(74,122)
                else: #if its in a disallowed position
                    if alreadyY == True: #if copied blah blah blah blah
                        y = positionY
                    else:
                        y = random.randint(32,224)
                    x = random.randint(52,204)
                    while check_inside_face(x,y) == False or check_inside_left_eye_region(x,y) == True or check_inside_right_eye_region(x,y) == True:
                        x = random.randint(52,204)
                        if alreadyY == True:
                            y = positionY
                        else:
                            y = random.randint(32,224)
                            
            elif currentFeature == 1: #nose mouth already done
                if check == True: #in allowed pos
                    x = random.randint(100,156)
                    y = random.randint(96,146)
                elif check == False: #disallowed pos
                    x = random.randint(52,204)
                    y = random.randint(32,224)
                    while check_inside_face(x,y) == False or check_inside_nose_region(x,y) == True:
                        x = random.randint(52,204)
                        y = random.randint(32,224)
            
    else:
        if face == True:
            print("3rd feature, either eyes and nose done, eyes and mouth done or nose and mouth done")
    
    
    return x, y, 



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

#face_outline(canvas)

for i in range (15):
    decide_face_type()



def save_all_da_shit():
    cwd = os.getcwd()
    for i in range (5): #change to 20000 for final test
        filename = str(str(i) + ".png")
        pygame.image.save(canvas, os.path.join(cwd, filename))


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    pygame.display.flip()


pygame.quit()