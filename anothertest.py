import random

thingthing = [[1, 2, 3], [1, 2], [1, 2, 3, 4], [1], [1, 2]]
for thing in thingthing:
    if len(thing) == 2:
        print(thing)
        b = random.randint(1, 3)
        if b == 2:
            print(b)
        else:
            print("else")
    print("a")
    
print("done")


thislist = [True, False, True, True, False]
for i in thislist:
    if i == False:
        thislist.remove(i)
print(thislist)