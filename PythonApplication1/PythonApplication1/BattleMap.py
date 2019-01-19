import json
from ReadJSONList import ReadJSONList

class MapInator(object):
    """
    Creates and manages the Battle Map.
    Calculates then performs movement of units.
    Calls Judge Classes when needed to resolve attacks, effects, etc.
    """


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
    def get_X(self): # redundant?
        return self.X
    def get_Y(self): # redundant?
        return self.Y
    def get_map_size(self):
        return (self.X, self.Y) # should return Tuple

    #Getter function to get a tile
    def get_tile(self, X, Y):
        Y_List = self.MainList(Y) # find the Y value
        X_Tile = Y_List(X) # find the X value
        return X_Tile # return the tile

    def print_map(self):
        print('*' * self.X)
        for i in self.MainList:
            print('*', end='')
            for j in self.MainList[i]:
                print(self._print_tile(SubList[j]), end='') # Fix
            print('*')
        print('*' * self.X)

    def _print_tile(self, space): # Fix
        if space.is_unoccupied():
            print('.') # make dynamic based on terrain
        else:
            print('P') # make dynamic based on Unit
            

    #Find Unit Function

    #

class Tile(object):
    """Tile Object containing all relevant information for a tile"""
       
    
    terrainList = ReadJSONList('MapTerrain.json') # temporary for now

    def __init__(self, X, Y, terraintype):
        self.X = X #X coordinate
        self.Y = Y #Y coordinate
        #function for selecting the terrain type
        self.terrain = terrainList.get_item('Grass')
        self.tileEffects = []
        self.unit = None


    #Getter functions for the X and Y coordinates
    def get_X(self):
        return self.X

    def get_Y(self):
        return self.Y


    #Terrain Info and Effects
    def get_terrain_type(self):
        return self.terrain['ID']

    def get_terrain_movement_cost(self):
        return self.terrain['Movement_Cost']

    #def get_whatever(self): # getter for other misc. terrain info


    #Tile Effects
    #may need to change 'effect' variable
    #def add_effect(self, effect):
        #self.tileEffects.append(effect)

    #def remove_effect(self, effect):
        #self.tileEffects.remove(effect)

    #method to return specific effect
    #def has_effect(self, effect):
        #for i in tileEffects:
            #if tileEffects[i]==effect:
                #return true
        #return false


    #Unit: Getter and Setter
    def get_unit(self):
        return self.unit

    #Intention: point to the unit, never create a new one
    def set_unit(self, unit): # ONLY EVER 1 UNIT
        self.unit = unit

    def set_unit_empty(self):
        self.unit = None

    def is_unoccupied(self):
        return self.unit == None


class Movement(object):
    """
    Calculates then performs ALL movement of units
    """


    #def move_unit(self, unit): # Basic movement, adjacent orthogonal tiles only
        #get X,Y of unit moving
        #get X,Y of destination
        #tempUnit = unit
        #remove unit from starting position
        #set unit to destination
        #subtract stamina

    #def place_unit(self, unit): # no movement restriction, used by cards/effects
        #get X,Y of unit moving
        #get X,Y of destination
        #tempUnit = unit
        #remove unit from starting position
        #set unit to destination

    #def swap_units(self): # swaps the position of 2 units, may be unneeded


class RangeInator(object):
    """
    Calculates the valid tiles for targeting
    """