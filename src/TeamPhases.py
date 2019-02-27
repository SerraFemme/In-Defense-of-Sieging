"""
Contains all functions needed for either side to make their team and take
their turns.
"""

from src.ReadGameData import SubListManager
from src.Unit import Player, Enemy
from src.Equipment import Equipment
from src.EnemyTargeting import *
import src.ClassPassives


class PlayerMaker(object):
    """
    Creates the player team.
    For each player, asks them to enter their name, then select which class
    they would like to play, then creates a Player object with the proper info.
    """

    def __init__(self, c, se, e, sd, card):
        self.class_list = c
        self.s_equipment = se  # Starting Equipment
        self.equipment_list = e
        self.s_deck = sd  # Starting Deck
        self.card_library = card

    def create_player(self, player_name, player_number, selected_class):
        player = Player(self.class_list.get_item(selected_class), player_name, player_number)
        self.__equip_s_equipment(player,
                                 self.s_equipment.get_item(selected_class),
                                 self.equipment_list)
        # player.Passive = getattribute(src.ClassPassives, selected_class)
        # TODO: give player starting deck
        # self.add_s_deck(player, self.s_deck.get_item(selected_class, self.card_library)
        # self.add_s_deck(player, self.s_deck.get_item("Test", self.card_library)
        return player

    def __equip_s_equipment(self, player, s_equip, equip_list):
        s_list = s_equip['Starting_Equipment']
        for i in s_list:
            e = Equipment(equip_list.get_item(i))
            player.add_equipment(e)


class PlayerTurn(object):
    """
    Contains all functions needed for a player to take their turn.
    """

    def __init__(self, team, b_map, move):
        self.player_team = team
        self.battle_map = b_map
        self.movement = move

    def setup_players(self):
        print('\n' + 'Player Team:')
        print('Choose starting positions')
        for person in self.player_team:
            self.battle_map.print_map()
            print('\n' + person.Player_Name, person.Class_Name, sep=': ')
            self.movement.place_starting_player(person)
            # hand = person.Deck.value
            # person.Deck.draw(hand)

    def player_turn_loop(self):
        keep_playing = True
        for person in self.player_team:
            if person.Conscious is True:
                person.turn_beginning()
                turn = True
                self.battle_map.print_map()
                keep_playing = self.print_player_menu(person)
                if keep_playing is not False:
                    while turn:
                        self.battle_map.print_map()
                        print('\n' + 'Turn:', person.Player_Name)
                        print('Icon:', person.Icon)
                        value = self.print_turn_menu(person, self.movement)
                        turn = self.process_player_selection(value,
                                                             self.movement,
                                                             person)
            else:
                print(person.Player_Name,
                      'is unconscious. Passing Turn' + '\n')
        return keep_playing

    def print_player_menu(self, player):
        print('\n' + 'Player Menu:', player.Player_Name)
        print('0: Exit Game')
        print('1: Player Turn')
        while True:
            try:
                v = input("Input: ")
            except ValueError:
                print('Invalid input, try again')
            else:
                if v == '0':
                    return False
                else:
                    return v

    def print_turn_menu(self, player, movement):  # clean up
        global b, action
        b = True
        while b:
            b = False
            s = []
            s.clear()
            print('\n' + player.get_name(), end='')
            print(': Remaining Stamina:', player.Stamina.points)
            print('0: Pass Turn')
            if player.Stamina.points > 0:
                if movement.can_move(player):
                    print('1: Move')
                else:
                    print('Cannot Move, Player trapped')
                    s.append(1)
            else:
                print('Cannot Move, insufficient stamina')
                s.append(1)
            print('2: Action')
            print('3: Print Player Info')
            print('4: Print Equipment Info')
            print('5: Print your current tile info')
            while True:
                try:
                    action = int(input("Input: "))
                except ValueError:
                    print('Invalid input, try again')
                else:
                    if action in s:
                        print('Unavailable action' + '\n')
                        b = True
                    break

        return action

    def process_player_selection(self, value, movement, player):
        if value == 0:
            return False
        elif value == 1:
            movement.move_player(player)
        elif value == 2:
            print('No actions yet')
            # self.action_menu(player)
        elif value == 3:
            print(player.print_info())
        elif value == 4:
            print('')
            for k in player.Equipment:
                k.print_info()
                print('')
        elif value == 5:
            print('')
            tile = self.battle_map.get_tile(player.Position[0],
                                            player.Position[1])
            tile.print_info()
        return True

    def action_menu(self, player):
        if player.Passive is None:
            pass
        else:
            pass  # Is an activated passive


class HordeMaker(object):
    """
    Creates an enemy horde based on the encounter list then puts them on the map
    """

    def __init__(self, races, roles, equipment_list, n):
        self.number_of_players = n
        self.race_list = SubListManager(races)
        self.role_list = SubListManager(roles)
        self.equipment_list = SubListManager(equipment_list)

    def create_enemy_team(self, encounter):
        enemy_horde = []
        enemy_list = encounter['Enemies']

        for i in enemy_list:
            if isinstance(i['Number'], int):
                for j in range(i['Number']):
                    race = self.race_list.get_item(i['Race'])
                    role = self.role_list.get_item(i['Role'])
                    enemy = Enemy(race, role, j + 1)
                    for e in i['Equipment']:
                        equipment = self.equipment_list.get_item(e)
                        enemy.add_equipment(Equipment(equipment))
                    enemy_horde.append(enemy)
            else:  # Numbers is a string
                for j in range(self.number_of_players):
                    race = self.race_list.get_item(i['Race'])
                    role = self.role_list.get_item(i['Role'])
                    enemy = Enemy(race, role, j + 1)
                    for e in i['Equipment']:
                        equipment = self.equipment_list.get_item(e)
                        enemy.add_equipment(Equipment(equipment))
                    enemy_horde.append(enemy)

        return enemy_horde


class EnemyTurn(object):
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
