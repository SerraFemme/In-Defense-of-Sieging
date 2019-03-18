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
        self.active_team_number = 0
        self.active_team = None
        self.active_team_size = None
        self.initiate = True

    def setup(self):
        self.__place_enemies()  # TODO: place enemies

        self.__place_players()  # TODO: place players
        pass

    def run(self):
        if self.active_unit_number == 0:
            pass

        self.__cycle_unit()  # TODO: pass to other team
        pass

    def __place_enemies(self):
        pass

    def __place_players(self):
        pass

    def __cycle_unit(self):
        """
        Changes active unit to next unit on team.
        If last unit, switch to other team.
        """

        self.active_unit_number += 1
        if self.active_unit_number > self.active_team_size:
            self.__cycle_teams()
        else:
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