from random import randrange
from src.CONSTANTS import CONSTANTS

direction_dict = CONSTANTS.DIRECTION_DICT
map_percentage = CONSTANTS.STARTING_ROW_PERCENTAGE


class MapManager(object):
    """
    Creates and manages the Battle Map.
    Calculates then performs movement of units.
    Calls Judge Classes when needed to resolve attacks, effects, etc.
    """

    # TODO: convert all functions to use tuples for coordinates instead of separate x and y values
    def __init__(self, t, size=(12, 12), generator=None):
        self.terrain_list = t
        self.map_size = size
        self.main_list = []  # "List of rows"
        if generator is None:  # basic_map_generator
            for i in range(self.map_size[1]):
                sub_list = []  # List of Tiles
                self.main_list.append(sub_list)
                for j in range(self.map_size[0]):
                    sub_list.append(Tile(j, i, self.terrain_list.get_item(self.__basic_map_generator())))
        else:  # TODO: Add premade and other random map generators
            pass
        starting_y = int(self.map_size[1] * map_percentage) - 1
        if starting_y == 0:
            starting_y = 1
        self.starting_range = starting_y

        # Create dictionary of adjacent tiles for the current tile
        for x in range(self.map_size[0]):
            for y in range(self.map_size[1]):
                position = (x, y)
                tile = self.get_tile(position)
                tile.adjacent_tile_positions = self.__calculate_adjacent_tiles(position)

    def __basic_map_generator(self):
        basic_map_list = ['Grass', 'Hill', 'Mountain']
        r = randrange(1, 20)
        if 19 <= r <= 20:
            value = 2
        elif 17 <= r <= 18:
            value = 1
        else:
            value = 0
        return basic_map_list[value]

    def __calculate_adjacent_tiles(self, location):
        adjacent_dict = {}
        for i in direction_dict:
            coordinate = direction_dict[i]
            x = location[0] + coordinate[0]
            y = location[1] + coordinate[1]
            if 0 <= x < self.map_size[0] and 0 <= y < self.map_size[1]:
                adjacent_dict[i] = (x, y)

        return adjacent_dict

    def get_tile(self, position):
        y_list = self.main_list[position[1]]  # find the Y value
        x_tile = y_list[position[0]]  # find the X value
        return x_tile  # return the tile

    def is_tile_unoccupied(self, position):
        tile = self.get_tile(position)
        return tile.is_unoccupied()

    def get_unit(self, position):
        tile = self.get_tile(position)
        return tile.unit

    def set_unit(self, position, unit):
        tile = self.get_tile(position)
        tile.unit = unit

    def set_tile_unoccupied(self, position):
        tile = self.get_tile(position)
        tile.set_unit_empty()

    def move_unit(self, unit, destination, cost=True):
        start = unit.Position
        dest_tile = self.get_tile(destination)
        if self.is_tile_unoccupied(destination):
            destination_cost = dest_tile.get_terrain_movement_cost()
            if cost:
                if unit.Stamina.can_spend(destination_cost):
                    self.set_unit(destination, unit)
                    unit.Position = destination
                    unit.Stamina.spend_stamina_points(destination_cost)
                    self.set_tile_unoccupied(start)
            else:
                self.set_unit(destination, unit)
                unit.Position = destination
                self.set_tile_unoccupied(start)


class Tile(object):
    """Contains all relevant information for a tile"""

    def __init__(self, x, y, t):
        self.coordinate = (x, y)
        self.terrain = t  # dict of info
        self.adjacent_tile_positions = None  # dict of adjacent tile coordinates
        self.tile_effects = []
        self.unit = None
        if 'Unit' in self.terrain:
            self.unit = self.terrain['Unit']

    # Terrain Info and Effects
    def get_terrain_type(self):
        return self.terrain['ID']

    def get_terrain_movement_cost(self):
        if 'Movement_Cost' in self.terrain:
            return self.terrain['Movement_Cost']
        else:
            return None

    def set_unit_empty(self):
        self.unit = None

    def is_unoccupied(self):
        return self.unit is None

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


class TerrainGenerator(object):
    pass


class RangeInator(object):
    """
    Calculates the valid tiles for targeting
    """

    def __init__(self, battle_map):
        self.battle_map = battle_map

    def calculate_range(self):
        valid_targets = []
        # Unit, min range, max range, restriction
        pass
