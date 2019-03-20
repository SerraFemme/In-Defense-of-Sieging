"""
Processes the game logic of teams and their members taking their turns.
"""

from src.EnemyTargeting import *


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
            tile = self.battle_map.get_tile(position_selected[0], position_selected[1])
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
            if self.battle_map.is_tile_unoccupied(x, y):
                self.battle_map.set_unit(x, y, enemy)
                enemy.Position = (x, y)
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
    Controls the enemy during their phase
    """

    def __init__(self, enemy_horde, battle_map, movement, player_team):
        self.enemy_horde = enemy_horde
        self.battle_map = battle_map
        self.movement = movement
        self.player_team = player_team

    def enemy_turn_loop(self):
        for enemy in self.enemy_horde:
            if enemy.Alive:
                print('\n' + 'Turn:', enemy.get_name(), enemy.Enemy_Number)
                enemy.turn_beginning()
                if enemy.Stamina.points > 0:
                    target = self.find_target(enemy)
                    print('Targeting:', target.Player_Name + ',', target.Class_Name)
                    print('Moving from', enemy.Position, 'to ', end='')
                    self.move_into_range(enemy, target)
            else:
                print('\n' + enemy.get_name(), enemy.Enemy_Number, 'is dead. Skipping Turn')

    def find_target(self, enemy):
        if enemy.Role_Name == 'Grunt':
            target = TargetNearest(enemy, self.player_team).find_nearest_player()
        else:
            target = TargetAT(enemy, self.player_team).find_AT_target()
        return target

    def move_into_range(self, enemy, target):
        self.movement.move_enemy(enemy, target.Position)
        print(enemy.Position)
        # check available actions
        # move into range of the best action to take
        if enemy.Stamina.points > 0:
            print('Remaining Stamina:', enemy.Stamina.points)
            self.take_selected_action(enemy, target)
        else:
            print(enemy.get_name(), 'is out of Stamina!')

    def take_selected_action(self, enemy, target):
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
