from random import randrange
from src.CONSTANTS import CONSTANTS

DIRECTION = CONSTANTS.DIRECTION_TUPLES
map_percentage = CONSTANTS.STARTING_ROW_PERCENTAGE


class MapInator(object):
    """
    Creates and manages the Battle Map.
    Calculates then performs movement of units.
    Calls Judge Classes when needed to resolve attacks, effects, etc.
    """

    # used to create an X by Y sized Map
    def __init__(self, t, x=12, y=12, generator=None):
        self.terrain_list = t
        self.map_size = (x, y)
        self.main_list = []  # "List of rows"
        if generator is None:
            for i in range(y):
                sub_list = []  # List of Tiles
                self.main_list.append(sub_list)
                for j in range(x):
                    sub_list.append(Tile(j, i, self.terrain_list.get_item(self.basic_map_generator())))
        else:  # TODO: Add premade and other random map generators
            pass
        starting_y = int(self.map_size[1] * map_percentage) - 1
        if starting_y == 0:
            starting_y = 1
        self.starting_range = starting_y

    def basic_map_generator(self):
        basic_map_list = ['Grass', 'Hill', 'Mountain']
        r = randrange(1, 20)
        if 19 <= r <= 20:
            value = 2
        elif 17 <= r <= 18:
            value = 1
        else:
            value = 0
        return basic_map_list[value]

    def get_tile(self, x, y):
        y_list = self.main_list[y]  # find the Y value
        x_tile = y_list[x]  # find the X value
        return x_tile  # return the tile

    def is_tile_unoccupied(self, x, y):
        tile = self.get_tile(x, y)
        return tile.is_unoccupied()

    def get_unit(self, x, y):
        tile = self.get_tile(x, y)
        return tile.unit

    def set_unit(self, x, y, unit):
        tile = self.get_tile(x, y)
        tile.unit = unit

    def set_tile_unoccupied(self, x, y):
        tile = self.get_tile(x, y)
        tile.set_unit_empty()


class Tile(object):
    """Contains all relevant information for a tile"""

    def __init__(self, x, y, t):
        self.coordinate = (x, y)
        self.terrain = t  # dict of info
        self.tileEffects = []
        self.unit = None
        if 'Unit' in self.terrain:
            self.unit = self.terrain['Unit']

    # Terrain Info and Effects
    def get_terrain_char(self):
        return self.terrain['Char']

    def get_terrain_type(self):
        return self.terrain['ID']

    def get_terrain_movement_cost(self):
        if 'Movement_Cost' in self.terrain:
            return self.terrain['Movement_Cost']
        else:
            return None

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

    def __init__(self, map_given):
        self.battle_map = map_given
        self.map_size = self.battle_map.map_size

    def place_enemy_random(self, enemy):
        while True:
            x = randrange(0, self.map_size[0] - 1)
            y = randrange(self.map_size[1] - self.battle_map.starting_range, self.map_size[1]) - 1
            if self.battle_map.is_tile_unoccupied(x, y):
                self.battle_map.set_unit(x, y, enemy)
                enemy.Position = (x, y)
                break

    def place_enemy_team_random(self, enemy_team):
        for enemy in enemy_team:
            self.place_enemy_random(enemy)

    def move_unit(self, unit, destination, cost=True):
        start = unit.Position
        x = destination[0]
        y = destination[1]
        dest_tile = self.battle_map.get_tile(x, y)
        if self.battle_map.is_tile_unoccupied(x, y):
            destination_cost = dest_tile.get_terrain_movement_cost()
            if cost:
                if unit.Stamina.can_spend(destination_cost):
                    self.battle_map.set_unit(x, y, unit)
                    unit.Position = (x, y)
                    unit.Stamina.spend_stamina_points(destination_cost)
                    self.battle_map.set_tile_unoccupied(start[0], start[1])
            else:
                self.battle_map.set_unit(x, y, unit)
                unit.Position = (x, y)
                self.battle_map.set_tile_unoccupied(start[0], start[1])

    # def move_player(self, player):  # TODO: Delete
    #     print('Which direction would you like to go?')
    #     print('1: Up')
    #     print('2: Right')
    #     print('3: Down')
    #     print('4: Left')
    #     while True:
    #         try:
    #             v = int(input('Select Direction: '))
    #         except ValueError:
    #             print('Invalid input, try again' + '\n')
    #         else:
    #             if 0 < v <= 4:
    #                 break
    #             else:
    #                 print(v, 'is not a valid selection, try again' + '\n')
    #     while True:
    #         try:
    #             distance = int(input('Enter distance: '))
    #         except ValueError:
    #             print('Invalid input, try again')
    #         else:
    #             break
    #     self.move_unit(player, DIRECTION[v-1], distance)

    # def move_unit(self, unit, direction, distance):  # TODO: Delete
    #     for i in range(distance):  # Move Up
    #         if self.can_move_onto_tile(unit, direction[0], direction[1]):
    #             self.move_onto_tile(unit, direction[0], direction[1])
    #         else:
    #             break

    # def move_onto_tile(self, unit, x, y):  # TODO: Delete
    #     coordinate = unit.Position
    #     if self.can_move(unit):
    #         new_position = (coordinate[0] + x, coordinate[1] + y)
    #         destination = self.battle_map.get_tile(new_position[0],
    #                                                new_position[1])
    #         if destination.is_unoccupied():
    #             destination_cost = destination.get_terrain_movement_cost()
    #             if unit.Stamina.can_spend(destination_cost):
    #                 unit.Position = new_position
    #                 destination.unit = unit
    #                 unit.Stamina.spend_stamina_points(destination_cost)
    #                 self.battle_map.set_tile_unoccupied(coordinate[0],
    #                                                     coordinate[1])
    #             else:
    #                 print('Insufficient Stamina')
    #         else:
    #             print(destination.coordinate, 'is occupied.')

    # def can_move(self, unit):  # FIXME: Convert for use by Enemies only
    #     coordinate = unit.Position
    #     x = coordinate[0]
    #     y = coordinate[1]
    #     if unit.Stamina.points > 0:
    #         if 0 <= x < self.map_size[0] and 0 <= y + 1 < self.map_size[1]:
    #             if self.battle_map.is_tile_unoccupied(x, y + 1):
    #                 return True
    #         if 0 <= x + 1 < self.map_size[0] and 0 <= y < self.map_size[1]:
    #             if self.battle_map.is_tile_unoccupied(x + 1, y):
    #                 return True
    #         if 0 <= x < self.map_size[0] and 0 <= y - 1 < self.map_size[1]:
    #             if self.battle_map.is_tile_unoccupied(x, y - 1):
    #                 return True
    #         if 0 <= x - 1 < self.map_size[0] and 0 <= y < self.map_size[1]:
    #             if self.battle_map.is_tile_unoccupied(x - 1, y):
    #                 return True
    #     else:
    #         print('Unit has', unit.Stamina.points, 'and cannot move.')
    #     return False

    # def can_move_onto_tile(self, unit, x, y):  # FIXME: Convert for use by Enemies only
    #     coordinate = unit.Position
    #     if 0 <= coordinate[0] + x < self.battle_map.map_size[0]\
    #             and 0 <= coordinate[1] + y < self.battle_map.map_size[1]:
    #         destination = self.battle_map.get_tile(coordinate[0] + x,
    #                                                coordinate[1] + y)
    #         if destination.is_unoccupied():
    #             if unit.Stamina.points >= destination.get_terrain_movement_cost():
    #                 return True
    #
    #     return False

    # def move_enemy(self, enemy, destination):  # FIXME: change to use new functions
    #     x_distance = abs(enemy.Position[0] - destination[0])
    #     y_distance = abs(enemy.Position[1] - destination[1])
    #     i = 0
    #     while i <= enemy.Stamina.get_pool_size():
    #         if x_distance != 0:
    #             if enemy.Position[0] < destination[0] and self.can_move_onto_tile(enemy, 1, 0):
    #                 self.move_unit(enemy, DIRECTION[1], 1)
    #             elif enemy.Position[0] > destination[0] and self.can_move_onto_tile(enemy, -1, 0):
    #                 self.move_unit(enemy, DIRECTION[3], 1)
    #         if y_distance != 0:
    #             if enemy.Position[1] < destination[1] and self.can_move_onto_tile(enemy, 0, 1):
    #                 self.move_unit(enemy, DIRECTION[0], 1)
    #             elif enemy.Position[1] > destination[1] and self.can_move_onto_tile(enemy, 0, -1):
    #                 self.move_unit(enemy, DIRECTION[2], 1)
    #         if enemy.Stamina.points == 0:
    #             break
    #
    #         x_distance = abs(enemy.Position[0] - destination[0])
    #         y_distance = abs(enemy.Position[1] - destination[1])
    #
    #         i += 1


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
