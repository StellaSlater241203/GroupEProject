import tkinter
import math
import random
from random import shuffle

CANVAS_W, CANVAS_H = 256, 256
FACE_LEFT, FACE_TOP, FACE_RIGHT, FACE_BOTTOM = 52, 32, 204, 224

#set variables:
maxGenCopies = [8,5,5] #generate a maximum of 8 eyes, 5 noses and 5 mouths
defaultGenCopies = [2,1,1] #to check whether a random copy generation has the number of copies of a face

#ALL OF THESE PROBABLITIES CAN BE CHANGED!!!!
FACE_PROB = 0.5
OVERLAP_PROB = 0.1
PREGEN_FACE_PROB = 0.2
DEFAULT_COPIES_PROB = 0.3
ROTATION_MIRROR_VS_SAME_PROB = 0.5
    
    #All values are booleans
# all written out differently even though they are the same so that all these probablilites can be altered separately for each different feature

#Pregenerated face seeds:
    #decide how tf this is gonna work later, might be easier for this to be a function itself with all the pregen face data in it 

def decide_face_type():
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
    mouthIDs, featureNumbers, totalFeatureNumber, defaultCopies = generate_number_of_features(face, totalFeatureNumber, featureNumbers, 2) #run the function to determine the number of noses and their IDs

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

    #Step 3: Decide the sizes for the features
    allowedEyeSizeDifference = 0.2 #just to test initially
    allowedEyeSizes = [0.8, 2.5]
    allowedNoseSizes = [0.8, 2.5]
    allowedMouthSizes = [0.8,2.5] #again just to test initially, if all shapes can be used for all features then the initial sizes of the shapes will need to be normalised and then these changed


    eyeSize = []
    noseSize = []
    mouthSize = [] #1D array that stores the size multiplier of each feature
    eyeShape = []
    noseShape = []
    mouthShape = [] #1D array that stores the shape of each feature

#decide on pregen design would be defined and called here probably xx

def generate_number_of_features(face, totalFeatureNumber, featureNumbers, currentFeature):
    IDs = [] #temp for this call of IDs, will be turned into the featureIDs array of whatever feature is currently being generated for

    #DECIDE ON THE NUMBER OF FEATURES
    if face == True:
        number = defaultGenCopies[currentFeature]
        featureNumbers.append(int(number)) #append the normal face amount of the feature currently running
        defaultCopies = True
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

        if currentFeature == 2 and featureNumbers == defaultGenCopies: #if it managed to generate the normal number of features for a face (this will only work properly on the 3rd call when featureNumbers is complete!!)
            defaultCopies = True #to check whether a face has been randomly generated later
        else: #if it didnt generate the normal number of features for a face
            defaultCopies = False

    #FILL IN FEATUREIDs
    for i in range(number):
        IDs.append(i)

    if currentFeature == 2:
        return(IDs, featureNumbers, totalFeatureNumber, defaultCopies)
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
    order = random.sample(IDs, len(IDs))
    counter = 0
    falseList = [False, False, False, False, False]
    copiesFrom = []
    for i in order:
        if counter == 0 and any(checks[i][0:5]):
            temp = falseList
            temp.extend(checks[i][5:9])
            checks.pop(i)
            checks.insert(i, temp)
            copiesFromID = None
            copiesFrom.insert(i, copiesFromID)
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
                copiesFrom.insert(i, copiesFromID[0])
            else:
                copiesFromID = None
                copiesFrom.insert(i, copiesFromID)
        else:
            pass
        counter += 1
    
    return(order, copiesFrom, checks)
    #if culling of the checks needs to be done do it here! might not need to though cause the matching checks can just be done first and the rest ignored if need
        
        
            
            




def generate_batch(canvases):
    for cv in canvases:
        cv.delete("all")
        decide_face_type()

for i in range(1): #LITERALLY ONLY FOR TESTING, JUST TO GENERATE 3 BATCHES FOR EASE
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
    #root.mainloop()

