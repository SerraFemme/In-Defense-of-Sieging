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

    def __init__(self, t, player_team, enemy_team, generator=None):
        self.terrain_list = t
        self.player_team = player_team
        self.enemy_team = enemy_team
        self.map_size = self.__calculate_map_size()
        self.main_list = []  # "List of rows"
        map_t_generator = TerrainGenerator(t, self.map_size)
        if generator is None:  # basic_map_generator
            for i in range(self.map_size[1]):
                sub_list = []  # List of Tiles
                self.main_list.append(sub_list)
                for j in range(self.map_size[0]):
                    terrain = map_t_generator.default()
                    sub_list.append(Tile(j, i, terrain))
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

    def __calculate_map_size(self):
        """
        Will calculate the map size based on the total number of units that will be on the map.
        :return:
        """
        number_of_players = len(self.player_team)
        number_of_enemies = len(self.enemy_team)
        total_number_of_units = number_of_players + number_of_enemies
        if total_number_of_units <= 8:
            map_size = (8, 8)
        else:
            map_size = (12, 12)
        return map_size

    def __calculate_adjacent_tiles(self, location):
        adjacent_dict = {}
        for i in direction_dict:
            coordinate = direction_dict[i]
            x = location[0] + coordinate[0]
            y = location[1] + coordinate[1]
            if 0 <= x < self.map_size[0] and 0 <= y < self.map_size[1]:
                adjacent_dict[i] = (x, y)

        return adjacent_dict

    # Tile Functions
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

    # Movement Functions
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

    # Range Functions
    def calculate_range(self, position, effect_range):
        """
        :param position: tuple: (x, y)
        :param effect_range: dict: {min-range, max_range, restriction}
        :return: list of tuples of positions
        Calculates a list of tuples of positions that are in the effect range.
        """
        x = position[0]
        y = position[1]

        min_range = effect_range['Min']
        max_range = effect_range['Max']
        range_restriction = effect_range['Restriction']

        all_tiles = []

        for i in range(-max_range, max_range + 1):  # TODO: rework logic
            if 0 <= x < self.map_size[0] and 0 <= y + i < self.map_size[1]:  # Tile on map
                if min_range <= abs(i) <= max_range:  # Tile in range
                    if i != 0:  # TODO: change for self targeting affects?
                        all_tiles.append((x, y + i))

            side_x = (max_range - abs(i))
            if side_x != 0:  # Don't add 'position' to list
                for v in range(1, side_x + 1):
                    if 0 <= x + v < self.map_size[0] and 0 <= y + i < self.map_size[1]:  # Tile on map
                        if range_restriction is not None:  # Check if 'In-Line' or 'Close' is in effect
                            # TODO: check if tile is In-Line
                            all_tiles.append((x + v, y + i))
                        else:
                            all_tiles.append((x + v, y + i))
                    if 0 <= x + (-1 * v) < self.map_size[0] and 0 <= y + i < self.map_size[1]:  # Tile on map
                        if range_restriction is not None:  # Check if 'In-Line' or 'Close' is in effect
                            # TODO: check if tile is In-Line
                            all_tiles.append((x + (-1 * v), y + i))
                        else:
                            all_tiles.append((x + (-1 * v), y + i))

        return all_tiles


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
    def __init__(self, t, size):
        self.terrain_list = t
        self.map_size = size  # tuple: (x, y)

    def default(self):
        """
        Randomly selects a terrain, then returns a terrain dict.
        :return: terrain dict
        """
        basic_map_list = ['Grass', 'Hill', 'Mountain']
        r = randrange(1, 20)
        if 19 <= r <= 20:
            value = 2
        elif 17 <= r <= 18:
            value = 1
        else:
            value = 0
        return self.terrain_list.get_item(basic_map_list[value])

    def mountain_map_generator(self, x, y):
        # very mountainous, some grass, few hills
        pass

    def hill_map_generator(self, x, y):
        # lots of hills, few mountains, some grass
        pass
