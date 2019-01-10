class MapCreator(object):
    """Creates the Map"""

    X = 12
    Y = 12


    #List of Lists
    #Main List acts as a tower of Sub Lists
    #Sub Lists are a set of objects
    #12 TerrainTile in RowList
    #12 RowList in MainList



    #instancelist = [ MyClass() for i in range(29)]

    for i in range(Y):
        for j in range(X):
            print(j, end=" ", flush=True)
        print('\n')

