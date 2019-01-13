class BattleMap(object):
    """Creates the Map"""

    #terrainType = 'Grass'

    #used to create an X by Y sized Map
    def __init__(self, X=12, Y=12):
        self.X = X #Size in X Tiles on the X-axis
        self.Y = Y #Size in Y Tiles on the Y-axis
        MAINLIST = [] #"List of rows"
        for i in range(Y):
            SUBLIST = [] #List of Tiles
            MAINLIST.append(SUBLIST)
            for j in range(X):
                SUBLIST.append(Tile(X, Y, terrainType)) #'seat %2d%c'%(i,ord('A')+j)

    
    #Getter functnions for the X and Y sizes of the map
    def get_X(self):
        return self.X
    def get_Y(self):
        return self.Y
    def get_Map_Size(self):
        return (self.X, self.Y) # should return Tuple

    #Getter function to get a tile
    def get_Tile(self, X, Y):
        Y_List = self.MAINLIST(Y)
        X_Tile = Y_List(X)
        return X_Tile
    #TerrainList = ReadTerrainList()

    





#    for i in range(Y):
#        for j in range(X):
#            print(j, end=" ", flush=True)
#        print('\n')


#    class Array(object):
#    def __init__(self, rows, cols):
#        self.rows = rows
#        self.cols = cols
#        # initialize array and fill with zeroes
#        self.data = [[0 for _ in range(cols)] for _ in range(rows)]
#    def __iter__(self):
#        for row in self.data:
#            yield row
#    def __repr__(self):
#        return 'Array(%d, %d)' % (self.rows, self.cols)




