from random import randrange
from ReadGameData import SubListManager


class MapInator(object):
    """
    Creates and manages the Battle Map.
    Calculates then performs movement of units.
    Calls Judge Classes when needed to resolve attacks, effects, etc.
    """

    # used to create an X by Y sized Map
    def __init__(self, terrainlist, X=12, Y=12):
        self.terrain_list = SubListManager(terrainlist)
        self.X = X  # Size in X Tiles on the X-axis
        self.Y = Y  # Size in Y Tiles on the Y-axis
        self.MainList = []  # "List of rows"
        for i in range(Y):
            sub_list = []  # List of Tiles
            self.MainList.append(sub_list)
            for j in range(X):
                sub_list.append(Tile(j, i, self.terrain_list.get_item(self.map_generator())))

    def map_generator(self):
        basic_map_list = ['Grass', 'Hill', 'Mountain']
        r = randrange(1, 20)
        if 19 <=r <= 20:
            value = 2
        elif 17 <= r <= 18:
            value = 1
        else:
            value = 0
        return basic_map_list[value]

    def get_map_size(self):
        return self.X, self.Y  # should return Tuple

    # Getter function to get a tile
    def get_tile(self, X, Y):
        Y_List = self.MainList[Y]  # find the Y value
        X_Tile = Y_List[X]  # find the X value
        return X_Tile  # return the tile

    def is_tile_unoccupied(self, X, Y):
        tile = self.get_tile(X, Y)
        return tile.is_unoccupied()

    def get_unit(self, X, Y):
        tile = self.get_tile(X, Y)
        return tile.get_unit()

    def set_unit(self, X, Y, unit):
        tile = self.get_tile(X, Y)
        tile.set_unit(unit)

    def set_tile_unoccupied(self, X, Y):
        tile = self.get_tile(X, Y)
        tile.set_unit(None)

    def print_map(self):
        print('')
        print('Map:')
        print('*' * (self.X+2))
        for self.Sub_List in reversed(self.MainList):
            print('*', end='')
            for tile in self.Sub_List:
                self._print_tile(tile)
            print('*')
        print('*' * (self.X+2))

    def _print_tile(self, tile):  # Fix
        terrain_character = {"Grass": ".", "Hill": "~", "Mountain": "&"}
        unit_character = {1: "P", 2: "E"}

        if tile.is_unoccupied():
            for i in terrain_character:
                if i == tile.get_terrain_type():
                    print(terrain_character[i], end='')  # make dynamic based on terrain
        else:
            for i in unit_character:
                if i == tile.get_unit():
                    print(unit_character[i], end='')  # make dynamic based on terrain

    # Find Unit Function


class Tile(object):
    """Contains all relevant information for a tile"""

    terrainList = SubListManager('MapTerrain.json')  # temporary for now

    def __init__(self, X, Y, terraintype):
        self.X = X  # X coordinate
        self.Y = Y  # Y coordinate
        self.terrain = terraintype
        self.tileEffects = []
        self.unit = None

    # Getter functions for the X and Y coordinates
    def get_X(self):
        return self.X

    def get_Y(self):
        return self.Y

    # Terrain Info and Effects
    def get_terrain_type(self):
        return self.terrain['ID']

    def get_terrain_movement_cost(self):
        return self.terrain['Movement_Cost']

    # def get_whatever(self): # getter for other misc. terrain info

    # Tile Effects
    # may need to change 'effect' variable
    # def add_effect(self, effect):
    # self.tileEffects.append(effect)

    # def remove_effect(self, effect):
    # self.tileEffects.remove(effect)

    # method to return specific effect
    # def has_effect(self, effect):
    # for i in tileEffects:
    # if tileEffects[i]==effect:
    # return true
    # return false

    # Unit: Getter and Setter
    def get_unit(self):
        return self.unit

    # Intention: point to the unit, never create a new one
    def set_unit(self, unit):  # ONLY EVER 1 UNIT
        self.unit = unit

    def set_unit_empty(self):
        self.unit = None

    def is_unoccupied(self):
        return self.unit is None


class TerrainGenerator(object):
    pass


class Movement(object):
    """
    Calculates then performs ALL movement of units
    """

    # def move_unit(self, unit): # Basic movement, adjacent orthogonal tiles only
    # get X,Y of unit moving
    # get X,Y of destination
    # tempUnit = unit
    # remove unit from starting position
    # set unit to destination
    # subtract stamina

    # def place_unit(self, unit): # no movement restriction, used by cards/effects
    # get X,Y of unit moving
    # get X,Y of destination
    # tempUnit = unit
    # remove unit from starting position
    # set unit to destination

    # def swap_units(self): # swaps the position of 2 units, may be unneeded


class RangeInator(object):
    """
    Calculates the valid tiles for targeting
    """
