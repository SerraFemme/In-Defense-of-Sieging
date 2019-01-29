"""
Contains all functions needed for the individuals of the player team to take
their turn and complete the player phase.
"""


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

    def player_turn_loop(self):
        keep_playing = True
        for person in self.player_team:
            if person.conscious is True:
                person.turn_beginning()
                turn = True
                self.battle_map.print_map()
                keep_playing = self.print_player_menu(person)
                if keep_playing is not False:
                    while turn:
                        self.battle_map.print_map()
                        print('\n' + 'Turn:', person.Player_Name)
                        value = self.print_action_menu(person, self.movement)
                        turn = self.process_player_selection(value, self.movement, person)
            else:
                print(person.Player_Name, 'is unconscious. Passing Turn' + '\n')
        return keep_playing

    def print_player_menu(self, player):
        print('\n' + 'Player Menu:', player.Player_Name)
        print('0: Exit Game')
        print('1: Player Turn')
        while True:
            try:
                value = input("Input: ")
            except ValueError:
                print('Invalid input, try again')
            else:
                if value == '0':
                    return False
                else:
                    return value

    def print_action_menu(self, player, movement):
        global i, action
        i = True
        while i:
            i = False
            s = []
            s.clear()
            print('\n' + player.get_class_name(), end='')
            print(': Remaining Stamina:', player.Stamina.get_stamina_points())
            print('0: Pass Turn')
            if player.Stamina.get_stamina_points() > 0:
                if movement.can_move(player):
                    print('1: Move')
                else:
                    print('Cannot Move, Player trapped')
                    s.append('1')
            else:
                print('Cannot Move, insufficient stamina')
                s.append('1')
            print('2: Action')
            print('3: Print Player Info')
            print('4: Print Equipment Info')
            while True:
                try:
                    action = input("Input: ")
                except ValueError:
                    print('Improper input, try again')
                else:
                    if action in s:
                        print('Improper selection' + '\n')
                        i = True
                    break

        return action

    def process_player_selection(self, value, movement, player):
        v = True
        if value == '0':
            v = False
        elif value == '1':
            movement.move_player(player)
        elif value == '2':
            print('No actions yet')
        elif value == '3':
            print(player.print_info())
        elif value == '4':
            print('')
            for k in player.Equipment:
                k.print_info()
                print('')
        return v
