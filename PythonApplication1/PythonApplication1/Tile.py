import json

class Tile(object):
    """Tile Object containing all relevant information for a tile"""

    #used to create instance of a tile at X, Y
    def __init__(self, X, Y, terraintype):
        self.X = X #X coordinate
        self.Y = Y #Y coordinate
        self.terrain = ReadTerrainList(terraintype) #function for setting the Terrain Type
        self.tileEffects = None
        self.unit = None


    #Getter functnions for the X and Y coordinates
    def get_X(self):
        return self.X
    def get_Y(self):
        return self.Y


    #Terrain Info and Effects
        #Pull Terrain Info from JSON List
        #method to return specific info


    #Tile Effects
        #Given by "Outside" sources
        #List of Effects?
        #method to return specific info


    #Unit: Getter and Setter
    def get_Unit(self):
        return self.unit
    def set_Unit(self, unit):
        self.unit = unit #ONLY EVER 1 UNIT, 2 units cannot occupy the same tile


    #No need for Setter functions (yet)
    #coordinates should only be created when instantiated
    
    
    
