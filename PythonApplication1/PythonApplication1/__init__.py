from ReadGameData import *
from BattleMap import MapInator, Movement
from Player import Player


def main():
    """
    Runs the Game.  Battle Map only for now.
    """

    keep_playing = True

    r = MasterListManager()
    terrainlist = r.get_list('Terrain')
    classlist = r.get_list('Class')

    player_1 = Player(classlist, 'Paladin')

    battle_map = MapInator(terrainlist)
    movement = Movement(battle_map)

    movement.place_enemy()

    battle_map.print_map()

    print('')
    print(player_1.get_class_name())
    player_1.set_position(movement.place_starting_unit())

    while keep_playing:
        battle_map.print_map()
        print('')
        print(player_1.get_class_name(), 'turn:')
        value = print_player_menu()
        keep_playing = process_menu_selection(value, movement, player_1)


def print_player_menu():
    print('0: Exit')
    print('1: Move')
    print('2: Action')
    print('3: Print Tile Icon List')
    value = input("Input: ")
    return value


def process_menu_selection(value, movement, player):
    v = True
    if value == '0':
        v = False
    elif value == '1':
        player.set_position(movement.move_unit(player.get_position()))
    elif value == '2':
        pass
    elif value == '3':
        pass
    return v


if __name__ == "__main__":
    main()
