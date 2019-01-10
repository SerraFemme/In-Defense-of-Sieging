#class Diamond(object):
#    """description of class"""


# Primary method to be used to calculate targeting range and splash damage
# Can later be adapted to movement range calculations

#Variables for testing, replace later with variables that are passed to this class
splash = 3
X=5
Y=5

for i in range(-splash, splash+1):
    print(X, Y+i)
    #check if the coordinates are valid
    #if valid, add to the list of affected tiles


    sideX = (splash-abs(i))
    if sideX !=0:
        for v in range(1, sideX+1):
            print(X+v, Y+i)
            print(X+(-1*v), Y+i)
            #check if the coordinates are valid
            #if valid, add to the list of affected tiles


#return a list of tuples of affected tiles