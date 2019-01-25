from random import randrange
from ReadGameData import SubListManager
from Player import Player


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
        if 19 <= r <= 20:
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
        if tile.is_unoccupied():
            print(tile.get_terrain_char(), end='')  # make dynamic based on terrain
        elif tile.get_unit() == 'Invalid':
            print(tile.get_terrain_char(), end='')  # make dynamic based on terrain
        elif tile.get_unit() == 2:
            print('E', end='')
        else:
            print('P', end='')

    # Find Unit Function


class Tile(object):
    """Contains all relevant information for a tile"""

    def __init__(self, X, Y, terraintype):
        self.coordinate = (X, Y)
        self.terrain = terraintype
        self.tileEffects = []
        self.unit = None
        if 'Unit' in self.terrain:
            self.unit = self.terrain['Unit']

    # Getter functions for the X and Y coordinates

    def get_coordinate(self):
        return self.coordinate

    # Terrain Info and Effects
    def get_terrain_char(self):
        return self.terrain['Char']

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

    def set_unit(self, unit):
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

    def __init__(self, map_given):
        self.battle_map = map_given

    def place_enemy(self):
        value = True
        while value:
            x = randrange(0, 11)
            y = randrange(9, 11)
            if self.battle_map.is_tile_unoccupied(x, y):
                self.battle_map.set_unit(x, y, 2)
                value = False

    def place_starting_player(self, player):
        value = True
        while value:
            print('Choose starting position in the bottom 3 rows:')
            x_place = int(input('Enter a value 0 to 11 for X: '))
            while x_place < 0 or x_place > 11:
                print(x_place, 'is invalid for X')
                x_place = int(input('Enter a value 0 to 11 for X: '))
            y_place = int(input('Enter a value 0 to 2 for Y: '))
            while y_place < 0 or y_place > 2:
                print(y_place, 'is invalid for Y')
                y_place = int(input('Enter a value 0 to 2 for Y: '))
            if self.battle_map.is_tile_unoccupied(x_place, y_place):
                self.battle_map.set_unit(x_place, y_place, player)
                player.set_position((x_place, y_place))
                value = False
            else:
                print(x_place, ',', y_place, 'is occupied.')

    def place_unit(self):
        value = True
        print('')
        print('Choose a new unoccupied position:')
        while value:
            x_place = int(input('Enter a value 0 to 11 for X: '))
            while x_place < 0 or x_place > 11:
                print(x_place, 'is invalid for X')
                x_place = int(input('Enter a value 0 to 11 for X: '))
            y_place = int(input('Enter a value 0 to 11 for Y: '))
            while y_place < 0 or y_place > 11:
                print(y_place, 'is invalid for Y')
                y_place = int(input('Enter a value 0 to 11 for Y: '))
            if self.battle_map.is_tile_unoccupied(x_place, y_place):
                self.battle_map.set_unit(x_place, y_place, 1)
                value = False
            else:
                print(x_place, ',', y_place, 'is occupied.')
                value = True
        return x_place, y_place

    def move_player(self, player):
        print('Which direction would you like to go?')
        print('1: Up')
        print('2: Right')
        print('3: Down')
        print('4: Left')
        direction = int(input('Select Direction: '))
        distance = int(input('Enter distance: '))
        self.move_unit(player, direction, distance)

    def move_unit(self, unit, direction, distance):
        if direction == 1:
            for i in range(distance):
                if self.can_move_onto_tile(unit, 0, 1):
                    self.move_onto_tile(unit, 0, 1)
                else:
                    break
        if direction == 2:
            for i in range(distance):
                if self.can_move_onto_tile(unit, 1, 0):
                    self.move_onto_tile(unit, 1, 0)
                else:
                    break
        if direction == 3:
            for i in range(distance):
                if self.can_move_onto_tile(unit, 0, -1):
                    self.move_onto_tile(unit, 0, -1)
                else:
                    break
        if direction == 4:
            for i in range(distance):
                if self.can_move_onto_tile(unit, -1, 0):
                    self.move_onto_tile(unit, -1, 0)
                else:
                    break

    def move_onto_tile(self, unit, x, y):
        coordinate = unit.get_position()
        if self.can_move(unit):
            new_position = (coordinate[0]+x, coordinate[1]+y)
            destination = self.battle_map.get_tile(new_position[0], new_position[1])
            if destination.is_unoccupied():
                # check if tile has a move cost, else don't move
                destination_cost = destination.get_terrain_movement_cost()
                if unit.Stamina.can_spend(destination_cost):
                    unit.set_position(new_position)
                    destination.set_unit(unit)
                    unit.Stamina.spend_stamina_points(destination_cost)
                    self.battle_map.set_tile_unoccupied(coordinate[0], coordinate[1])
                else:
                    print('Insufficient Stamina')
            else:
                print(destination.get_coordinate(), 'is occupied.')

    def can_move(self, unit):  # optimize
        coordinate = unit.get_position()
        x = coordinate[0]
        y = coordinate[1]
        value = False
        if unit.Stamina.get_stamina_points() > 0:
            map_size = self.battle_map.get_map_size()
            if 0 <= x < map_size[0] and 0 <= y + 1 < map_size[1]:
                if self.battle_map.is_tile_unoccupied(x, y + 1):
                    value = True
            if 0 <= x + 1 < map_size[0] and 0 <= y < map_size[1]:
                if self.battle_map.is_tile_unoccupied(x + 1, y):
                    value = True
            if 0 <= x < map_size[0] and 0 <= y - 1 < map_size[1]:
                if self.battle_map.is_tile_unoccupied(x, y - 1):
                    value = True
            if 0 <= x - 1 < map_size[0] and 0 <= y < map_size[1]:
                if self.battle_map.is_tile_unoccupied(x + 1, y):
                    value = True
        else:
            print(unit.get_class_name(), 'has', unit.Stamina.get_stamina_points(), 'and cannot move.')
        return value

    def can_move_onto_tile(self, unit, x, y):
        coordinate = unit.get_position()
        destination = self.battle_map.get_tile(coordinate[0]+x, coordinate[1]+y)
        if unit.Stamina.get_stamina_points() >= destination.get_terrain_movement_cost():
            return True
        else:
            return False


class RangeInator(object):
    """
    Calculates the valid tiles for targeting
    """
