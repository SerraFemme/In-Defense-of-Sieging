from random import randrange
from ReadGameData import SubListManager
from Player import Player
from Enemy import Enemy


class MapInator(object):
    """
    Creates and manages the Battle Map.
    Calculates then performs movement of units.
    Calls Judge Classes when needed to resolve attacks, effects, etc.
    """

    # used to create an X by Y sized Map
    def __init__(self, t, x=12, y=12):
        self.terrain_list = SubListManager(t)
        self.map_size = (x, y)
        self.main_list = []  # "List of rows"
        for i in range(y):
            sub_list = []  # List of Tiles
            self.main_list.append(sub_list)
            for j in range(x):
                sub_list.append(Tile(j, i, self.terrain_list.get_item(self.basic_map_generator())))

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

    # Getter function to get a tile
    def get_tile(self, x, y):
        y_list = self.main_list[y]  # find the Y value
        x_tile = y_list[x]  # find the X value
        return x_tile  # return the tile

    def is_tile_unoccupied(self, X, Y):
        tile = self.get_tile(X, Y)
        return tile.is_unoccupied()

    def get_unit(self, X, Y):
        tile = self.get_tile(X, Y)
        return tile.unit

    def set_unit(self, X, Y, unit):
        tile = self.get_tile(X, Y)
        tile.unit = unit

    def set_tile_unoccupied(self, X, Y):
        tile = self.get_tile(X, Y)
        tile.set_unit_empty()

    def print_map(self):
        x = self.map_size[0]
        print('\n' + 'Map:')
        print('*' * (x + 2))
        for self.sub_list in reversed(self.main_list):
            print('*', end='')
            for tile in self.sub_list:
                self.__print_tile(tile)
            print('*')
        print('*' * (x + 2))

    def __print_tile(self, tile):  # Fix
        if tile.is_unoccupied():
            print(tile.get_terrain_char(), end='')
        elif tile.unit == 'Invalid':
            print(tile.get_terrain_char(), end='')
        elif isinstance(tile.unit, Player):
            print(tile.unit.Player_Number, end='')
        elif isinstance(tile.unit, Enemy):
            print(tile.unit.Char, end='')
        else:  # something unexpected
            print('Q', end='')

    # Find Unit Function


class Tile(object):
    """Contains all relevant information for a tile"""

    def __init__(self, X, Y, t):
        self.coordinate = (X, Y)
        self.terrain = t
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

    def set_unit_empty(self):
        self.unit = None

    def is_unoccupied(self):
        return self.unit is None

    def print_info(self):
        print('Type:', self.terrain['ID'])
        print('Icon: [' + self.terrain['Char'] + ']')
        if 'Movement_Cost' in self.terrain:
            print('Movement Cost:', self.terrain['Movement_Cost'])
        else:
            print('Cannot be moved onto')
        if self.unit == 'Invalid':
            print('Cannot be occupied')
        else:
            print('Occupied:', type(self.unit))


class TerrainGenerator(object):
    pass


class Movement(object):
    """
    Calculates then performs ALL movement of units
    """

    def __init__(self, map_given):
        self.battle_map = map_given

    def place_enemy_random(self, enemy):
        while True:
            x = randrange(0, 11)
            y = randrange(9, 11)
            if self.battle_map.is_tile_unoccupied(x, y):
                self.battle_map.set_unit(x, y, enemy)
                enemy.Position = (x, y)
                break

    def place_starting_player(self, player):
        x = self.battle_map.map_size[0]
        # y = self.battle_map.map_size[1]
        while True:
            print('Choose starting position in the bottom 3 rows:')

            while True:
                try:
                    print('Enter a value 0 to', x - 1, end='')
                    x_place = int(input(' for X: '))
                except ValueError:
                    print('Invalid input, try again' + '\n')
                else:
                    if 0 <= x_place < x:
                        break
                    else:
                        print(x_place, 'is invalid for X')

            while True:
                try:
                    y_place = int(input('Enter a value 0 to 2 for Y: '))
                except ValueError:
                    print('Invalid input, try again' + '\n')
                else:
                    if 0 <= y_place <= 2:
                        break
                    else:
                        print(y_place, 'is invalid for y')

            if self.battle_map.is_tile_unoccupied(x_place, y_place):
                self.battle_map.set_unit(x_place, y_place, player)
                player.Position = (x_place, y_place)
                break
            else:
                print(x_place, ',', y_place, 'is occupied.')

    # def teleport_unit(self):  # teleports unit
    #     value = True
    #     print('\n' + 'Choose a new unoccupied position:')
    #     while value:
    #         x_place = int(input('Enter a value 0 to 11 for X: '))
    #         while x_place < 0 or x_place > 11:
    #             print(x_place, 'is invalid for X')
    #             x_place = int(input('Enter a value 0 to 11 for X: '))
    #         y_place = int(input('Enter a value 0 to 11 for Y: '))
    #         while y_place < 0 or y_place > 11:
    #             print(y_place, 'is invalid for Y')
    #             y_place = int(input('Enter a value 0 to 11 for Y: '))
    #         if self.battle_map.is_tile_unoccupied(x_place, y_place):
    #             self.battle_map.set_unit(x_place, y_place, 1)
    #             value = False
    #         else:
    #             print(x_place, ',', y_place, 'is occupied.')
    #             value = True
    #     return x_place, y_place

    def move_player(self, player):
        print('Which direction would you like to go?')
        print('1: Up')
        print('2: Right')
        print('3: Down')
        print('4: Left')
        while True:
            try:
                direction = int(input('Select Direction: '))
            except ValueError:
                print('Invalid input, try again' + '\n')
            else:
                if 0 < direction <= 4:
                    break
                else:
                    print(direction, 'is not a valid selection, try again' + '\n')
        while True:
            try:
                distance = int(input('Enter distance: '))
            except ValueError:
                print('Invalid input, try again')
            else:
                break
        self.move_unit(player, direction, distance)

    def move_unit(self, unit, direction, distance):
        if direction == 1:
            for i in range(distance):  # Move Up
                if self.can_move_onto_tile(unit, 0, 1):
                    self.move_onto_tile(unit, 0, 1)
                else:
                    break
        if direction == 2:  # Move Right
            for i in range(distance):
                if self.can_move_onto_tile(unit, 1, 0):
                    self.move_onto_tile(unit, 1, 0)
                else:
                    break
        if direction == 3:  # Move Down
            for i in range(distance):
                if self.can_move_onto_tile(unit, 0, -1):
                    self.move_onto_tile(unit, 0, -1)
                else:
                    break
        if direction == 4:  # Move Left
            for i in range(distance):
                if self.can_move_onto_tile(unit, -1, 0):
                    self.move_onto_tile(unit, -1, 0)
                else:
                    break

    def move_onto_tile(self, unit, x, y):  # clean up?
        coordinate = unit.Position
        if self.can_move(unit):
            new_position = (coordinate[0] + x, coordinate[1] + y)
            destination = self.battle_map.get_tile(new_position[0],
                                                   new_position[1])
            if destination.is_unoccupied():
                destination_cost = destination.get_terrain_movement_cost()
                if unit.Stamina.can_spend(destination_cost):
                    unit.Position = new_position
                    destination.unit = unit
                    unit.Stamina.spend_stamina_points(destination_cost)
                    self.battle_map.set_tile_unoccupied(coordinate[0],
                                                        coordinate[1])
                else:
                    print('Insufficient Stamina')
            else:
                print(destination.coordinate, 'is occupied.')

    def can_move(self, unit):  # clean up?
        coordinate = unit.Position
        x = coordinate[0]
        y = coordinate[1]
        if unit.Stamina.points > 0:
            map_size = self.battle_map.map_size
            if 0 <= x < map_size[0] and 0 <= y + 1 < map_size[1]:
                if self.battle_map.is_tile_unoccupied(x, y + 1):
                    return True
            elif 0 <= x + 1 < map_size[0] and 0 <= y < map_size[1]:
                if self.battle_map.is_tile_unoccupied(x + 1, y):
                    return True
            elif 0 <= x < map_size[0] and 0 <= y - 1 < map_size[1]:
                if self.battle_map.is_tile_unoccupied(x, y - 1):
                    return True
            elif 0 <= x - 1 < map_size[0] and 0 <= y < map_size[1]:
                if self.battle_map.is_tile_unoccupied(x - 1, y):
                    return True
        else:
            print(unit.get_class_name(), 'has',
                  unit.Stamina.points, 'and cannot move.')
        return False

    def can_move_onto_tile(self, unit, x, y):  # clean up
        coordinate = unit.Position
        if 0 <= coordinate[0] + x < self.battle_map.map_size[0]\
                and 0 <= coordinate[1] + y < self.battle_map.map_size[1]:
            destination = self.battle_map.get_tile(coordinate[0] + x, coordinate[1] + y)
            if destination.is_unoccupied():
                if unit.Stamina.points >= destination.get_terrain_movement_cost():
                    return True

        return False

    def move_enemy(self, enemy, destination):  # Must Improve
        x_distance = abs(enemy.Position[0] - destination[0])
        y_distance = abs(enemy.Position[1] - destination[1])
        i = 0
        while i <= enemy.Stamina.get_pool_size():
            if x_distance != 0:
                if enemy.Position[0] < destination[0] and self.can_move_onto_tile(enemy, 1, 0):
                    self.move_unit(enemy, 2, 1)
                elif enemy.Position[0] > destination[0] and self.can_move_onto_tile(enemy, -1, 0):
                    self.move_unit(enemy, 4, 1)
            if y_distance != 0:
                if enemy.Position[1] < destination[1] and self.can_move_onto_tile(enemy, 0, 1):
                    self.move_unit(enemy, 1, 1)
                elif enemy.Position[1] > destination[1] and self.can_move_onto_tile(enemy, 0, -1):
                    self.move_unit(enemy, 3, 1)
            if enemy.Stamina.points == 0:
                break
            i += 1


class RangeInator(object):
    """
    Calculates the valid tiles for targeting
    """

    def enemy_range(self):
        pass
