"""
Processes the game logic of teams and their members taking their turns.
"""

from src.CONSTANTS import CONSTANTS
from src.EnemyTargeting import *

DIRECTION = CONSTANTS.DIRECTION_TUPLES


class BattlePhase(object):
    def __init__(self, player_team, enemy_team, battle_map):
        self.player_team = player_team
        self.enemy_team = enemy_team
        self.battle_map = battle_map
        self.active_unit_number = 0
        self.active_unit = None
        self.active_team = None
        self.active_team_number = 0
        self.team_list = ['Player Team',
                          'Enemy Team']
        self.active_team_size = None
        self.initiate = True

    def setup(self):
        self.place_enemy_team_random()

        self.set_team(0)
        self.set_unit(0)

    def set_unit(self, value):
        if value <= self.active_team_size:
            self.active_unit = self.active_team[value]
            self.active_unit_number = value

    def set_team(self, value):
        if value == 0:
            self.active_team = self.player_team
        else:
            self.active_team = self.enemy_team

        self.active_team_size = len(self.active_team)

    def cycle_unit(self, initiate=False):
        """
        Changes active unit to next unit on team.
        If last unit, switches active team.
        """
        self.active_unit_number += 1
        if initiate is False:
            if self.active_unit_number >= self.active_team_size:
                self.__cycle_teams()
            else:
                self.active_unit = self.active_team[self.active_unit_number]
                self.active_unit.turn_beginning()
        else:
            if self.active_unit_number < self.active_team_size:
                self.active_unit = self.active_team[self.active_unit_number]

    def __cycle_teams(self):
        """
        Swaps active team and active unit
        """

        self.active_unit_number = 0

        if self.active_team_number == 0:  # Swap to enemy team
            self.active_team_number = 1
            self.active_team = self.enemy_team

        else:
            self.active_team_number = 0
            self.active_team = self.player_team

        self.active_team_size = len(self.active_team)
        self.active_unit = self.active_team[self.active_unit_number]

    def place_player(self, position_selected):
        initiate = False
        if self.active_unit_number < len(self.player_team):
            tile = self.battle_map.get_tile(position_selected)
            if tile.unit is None:
                player = self.player_team[self.active_unit_number]
                tile.unit = player
                player.Position = position_selected
                if self.active_unit_number < len(self.player_team):
                    initiate = True
                self.cycle_unit(True)

        return initiate

    def place_enemy_team_random(self):
        """
        In enemy order, randomly places an enemy on an unoccupied tile on their side of the map
        """
        for enemy in self.enemy_team:
            self.place_enemy_random(enemy)

    def place_enemy_random(self, enemy):
        while True:
            x = randrange(0, self.battle_map.map_size[0] - 1)
            y = randrange(self.battle_map.map_size[1] - self.battle_map.starting_range,
                          self.battle_map.map_size[1]) - 1
            position = (x, y)
            if self.battle_map.is_tile_unoccupied(position):
                self.battle_map.set_unit(position, enemy)
                enemy.Position = position
                break

    def team_string(self):
        return self.team_list[self.active_team_number]


class PlayerTurn(object):  # TODO: Update to new system
    """
    Contains all functions needed for a player to take their turn.
    """

    pass


class EnemyTurn(object):  # TODO: Update to new system
    """
    Controls the enemy during their phase.
    Enemies will always try to move first.
    After movement, enemies will try to take the best action(s).
    Then the enemy will pass their turn.
    """

    def __init__(self, battle_map, player_team):
        self.battle_map = battle_map
        self.player_team = player_team
        self.current_target = None

    def start_turn(self, enemy):
        if enemy.Alive:
            enemy.turn_beginning()
            self.current_target = self.__find_target(enemy)
            return True
        else:
            return False

    def take_turn(self, enemy):
        if enemy.Stamina.points > 0:
            self.__move_into_range(enemy, self.current_target)
            if enemy.Stamina.points > 0:
                # self.take_selected_action()
                pass
            enemy.turn_ending()
            self.current_target = None

    def __find_target(self, enemy):
        if enemy.Role_Name == 'Grunt':
            target = TargetNearest(enemy, self.player_team).find_nearest_player()
        else:
            target = TargetAT(enemy, self.player_team).find_AT_target()
        return target

    def __move_into_range(self, enemy, target):
        # check available actions
        # move into range of the best action to take
        self.__move_enemy(enemy, target.Position)

    def __move_enemy(self, enemy, destination):
        x_distance = abs(enemy.Position[0] - destination[0])
        y_distance = abs(enemy.Position[1] - destination[1])
        i = 0
        while i <= enemy.Stamina.get_pool_size():
            if x_distance != 0:
                # Move Right
                if enemy.Position[0] < destination[0] and self.__can_move_onto_tile(enemy, DIRECTION[1]):
                    self.__move_onto_tile(enemy, DIRECTION[1])
                # Move Left
                elif enemy.Position[0] > destination[0] and self.__can_move_onto_tile(enemy, DIRECTION[3]):
                    self.__move_onto_tile(enemy, DIRECTION[3])
            if y_distance != 0:
                # Move Up
                if enemy.Position[1] < destination[1] and self.__can_move_onto_tile(enemy, DIRECTION[0]):
                    self.__move_onto_tile(enemy, DIRECTION[0])
                # Move Down
                elif enemy.Position[1] > destination[1] and self.__can_move_onto_tile(enemy, DIRECTION[2]):
                    self.__move_onto_tile(enemy, DIRECTION[2])
            if enemy.Stamina.points == 0:
                break

            x_distance = abs(enemy.Position[0] - destination[0])
            y_distance = abs(enemy.Position[1] - destination[1])

            i += 1

    def __move_onto_tile(self, enemy, direction):
        tile_position = (enemy.Position[0] + direction[0], enemy.Position[1] + direction[1])
        self.battle_map.move_unit(enemy, tile_position)

    def __can_move_onto_tile(self, unit, direction):
        x = direction[0]
        y = direction[1]
        coordinate = unit.Position
        if 0 <= coordinate[0] + x < self.battle_map.map_size[0]\
                and 0 <= coordinate[1] + y < self.battle_map.map_size[1]:
            destination = self.battle_map.get_tile((coordinate[0] + x,
                                                   coordinate[1] + y))
            if destination.is_unoccupied():
                if unit.Stamina.points >= destination.get_terrain_movement_cost():
                    return True

        return False

    def take_selected_action(self, enemy, target):  # TODO: rework for future implementation
        x = abs(enemy.Position[0] - target.Position[0])
        y = abs(enemy.Position[1] - target.Position[1])
        distance = x + y
        if distance > 1:
            print('Target out of range!')
        elif enemy.Stamina.points >= 2:
            print('Dealing', enemy.Weapon_Damage.value, 'to',
                  target.Player_Name, target.Class_Name)
        else:
            print(enemy.Stamina.points, 'is not enough points for an action')
