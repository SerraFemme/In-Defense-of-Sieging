class BattleMap(object):
    """Creates and manages the Battle Map"""

    terrainType = 'Grass' # replace with map terrain generator

    #used to create an X by Y sized Map
    def __init__(self, X=12, Y=12):
        self.X = X #Size in X Tiles on the X-axis
        self.Y = Y #Size in Y Tiles on the Y-axis
        self.MainList = [] #"List of rows"
        for i in range(Y):
            self.SubList = [] #List of Tiles
            MainList.append(SubList)
            for j in range(X):
                SubList.append(Tile(X, Y, terrainType))

    
    #Getter functnions for the X and Y sizes of the map
    def get_X(self):
        return self.X
    def get_Y(self):
        return self.Y
    def get_map_size(self):
        return (self.X, self.Y) # should return Tuple

    #Getter function to get a tile
    def get_tile(self, X, Y):
        Y_List = self.MainList(Y) # find the Y value
        X_Tile = Y_List(X) # find the X value
        return X_Tile # return the tile