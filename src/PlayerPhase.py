"""
Contains all functions needed for the player team to make their team and take
their turns.
"""

from src.ReadGameData import SubListManager
from src.Player import Player
from src.Equipment import Equipment


class TeamMaker(object):
    """
    Creates the player team.
    For each player, asks them to enter their name, then select which class
    they would like to play, then creates a Player object with the proper info.
    """
    def __init__(self, c, se, e, sd, card):
        self.class_list = SubListManager(c)
        self.s_equipment = SubListManager(se)  # Starting Equipment
        self.equipment_list = SubListManager(e)
        self.s_deck = SubListManager(sd)  # Starting Deck
        self.card_library = SubListManager(card)
        self.player_list = []

    def team_init(self):
        while True:
            try:
                print('Create your team:')
                v = int(input('\n' + 'Enter number of Players (1-4): '))

            except ValueError:
                print('Invalid input, try again')
            else:
                if 0 < v <= 4:
                    break
                else:
                    print(v, 'is not a valid number')

        available_classes = self.__available_classes()
        for i in range(v):
            name = input('\n' + 'Enter Player Name: ')
            selected_class = self.__select_class(available_classes)
            print(name, selected_class, sep=': ')
            class_info = self.class_list.get_item(selected_class)
            player = Player(class_info, name, len(self.player_list)+1)
            self.equip_s_equipment(player,
                                   self.s_equipment.get_item(selected_class),
                                   self.equipment_list)
            # give class passive
            # give player starting deck
            # self.add_s_deck(player, self.s_deck.get_item(selected_class, self.card_library)
            # self.add_s_deck(player, self.s_deck.get_item("Test", self.card_library)
            self.player_list.append(player)
        return self.player_list

    def __select_class(self, class_list):
        print('\n' + 'Select Class:')
        for i, item in enumerate(class_list):
            print(i, item['ID'], sep=': ')
        while True:
            try:
                v = int(input('Enter digit of class: '))
            except ValueError:
                print('Invalid input, try again', '\n')
            else:
                if 0 <= v < len(class_list):
                    break
                else:
                    print(v, 'is not a valid class selection')

        selection = class_list.pop(v)
        return selection['ID']

    def __available_classes(self):
        item_list = self.class_list.get_list()
        return item_list

    def equip_s_equipment(self, player, s_equip, equip_list):
        s_list = s_equip['Starting_Equipment']
        for i in s_list:
            e = Equipment(equip_list.get_item(i))
            player.add_equipment(e)

    # def add_s_deck(self, player, s_deck, card_list):
    #     deck = []
    #     deck_list = s_deck['Starting_Deck']
    #     for i in deck_list:
    #         card = CardMaker(card_list.get_item(i))
    #         deck.append(card)
    #     player.Deck = deck


class PlayerTurn(object):
    """
    Contains all functions needed for a player to take their turn.
    """
    def __init__(self, team, bmap, move):
        self.player_team = team
        self.battle_map = bmap
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
                        print('Icon:', person.Player_Number)
                        value = self.print_action_menu(person, self.movement)
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

    def print_action_menu(self, player, movement):  # clean up
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
