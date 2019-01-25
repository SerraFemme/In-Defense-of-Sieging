from ReadGameData import *
from BattleMap import MapInator, Movement
from Player import Player


def main():
    """
    Runs the Game.  Battle Map only for now.
    """
    global keep_playing
    keep_playing = True

    r = MasterListManager()
    terrainlist = r.get_list('Terrain')
    classlist = r.get_list('Class')
    battle_map = MapInator(terrainlist)
    movement = Movement(battle_map)

    player_team = []
    # enemy_team = []

    player_1 = Player(classlist, 'Paladin')

    player_team.append(player_1)

    movement.place_enemy()

    for person in player_team:
        battle_map.print_map()
        print('')
        print(person.get_class_name())
        movement.place_starting_player(person)

    while keep_playing:
        global turn
        turn = True

        for person in player_team:
            person.turn_beginning()
            while turn:
                battle_map.print_map()
                print('')
                print(person.get_class_name(), 'turn:')
                keep_playing = print_player_menu()
                if keep_playing is False:
                    turn = False
                else:
                    value = print_action_menu(person, movement)
                    turn = process_player_selection(value, movement, person)

        print('')
        print('Enemy Turn: N/A')
        print('')


def print_player_menu():
    print('0: Exit Game')
    print('1: Player Turn')
    value = input("Input: ")
    if value == '0':
        return False
    else:
        return value


def print_action_menu(player, movement):
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


def process_player_selection(value, movement, player):
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


if __name__ == "__main__":
    main()
