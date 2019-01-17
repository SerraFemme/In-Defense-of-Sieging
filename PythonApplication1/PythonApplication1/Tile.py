import json
import ReadJSONList

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


    #Getter functnions for the X and Y coordinates
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