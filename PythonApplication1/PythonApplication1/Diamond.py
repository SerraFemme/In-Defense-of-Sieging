class Diamond(object):
    """description of class"""

    # Primary class to be used to calculate targeting range and range damage
    # Can later be adapted to movement range calculations

    #method used for range

    #method used for splash damage
    
    
    
    range = 3
    X=5
    Y=5

    for i in range(-range, range+1):
        print(X, Y+i)
        #check if the coordinates are valid
        #if valid, add to the list of affected tiles


        sideX = (range-abs(i))
        if sideX !=0:
            for v in range(1, sideX+1):
                print(X+v, Y+i)
                print(X+(-1*v), Y+i)
                #check if the coordinates are valid
                #if valid, add to the list of affected tiles


    #return a list of tuples of affected tiles