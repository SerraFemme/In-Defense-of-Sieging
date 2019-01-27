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
        print('')
        print('Player Team: Choose starting positions')
        print('')
        for person in self.player_team:
            self.battle_map.print_map()
            print('')
            print(person.Player_Name, person.Class_Name, sep=': ')
            self.movement.place_starting_player(person)

    def player_turn_loop(self):
        keep_playing = True
        for person in self.player_team:
            person.turn_beginning()
            turn = True
            self.battle_map.print_map()
            keep_playing = self.print_player_menu(person)
            if keep_playing is not False:
                while turn:
                    self.battle_map.print_map()
                    print('')
                    print(person.Player_Name, 'turn:')
                    value = self.print_action_menu(person, self.movement)
                    turn = self.process_player_selection(value, self.movement, person)
        return keep_playing

    def print_player_menu(self, player):
        print('')
        print('Player Menu:', player.Player_Name)
        print('0: Exit Game')
        print('1: Player Turn')
        value = input("Input: ")
        if value == '0':
            return False
        else:
            return value

    def print_action_menu(self, player, movement):
        i = True
        while i:
            i = False
            s = []
            s.clear()
            print('')
            print(player.get_class_name(), end='')
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
            value = input("Input: ")
            if value in s:
                print('Improper selection')
                print('')
                i = True
        return value

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
        return v
