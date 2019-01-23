from BattleMap import MapInator
from ReadGameData import *


def main():
    """
    Runs the Game.  Battle Map only for now.
    """

    keep_playing = True

    r = MasterListManager()

    terrainlist = r.get_list('Terrain')

    battle_map = MapInator(terrainlist)

    battle_map.set_unit(6, 11, 2)
    battle_map.print_map()

    player_position = place_starting_unit(battle_map)

    while keep_playing:
        battle_map.print_map()
        player_position = move_unit(battle_map, player_position)
        battle_map.print_map()
        keep_playing = continue_playing()


def continue_playing():
    v = True
    value = input("Keep Playing? 1 or 0: ")
    print('')
    if value != '1':
        v = False
    return v


def place_starting_unit(battle_map):
    print('')
    print('Choose starting position in the bottom 3 rows:')
    x_place = int(input('Enter a value 0 to 11 for X: '))
    while x_place < 0 or x_place > 11:
        print(x_place, 'is invalid for X')
        x_place = int(input('Enter a value 0 to 11 for X: '))
    y_place = int(input('Enter a value 0 to 2 for Y: '))
    while y_place < 0 or y_place > 2:
        print(y_place, 'is invalid for Y')
        y_place = int(input('Enter a value 0 to 2 for Y: '))
    if battle_map.is_tile_unoccupied(x_place, y_place):
        battle_map.set_unit(x_place, y_place, 1)
    else:
        print(x_place, ',', y_place, 'is occupied.')
    return x_place, y_place


def place_unit(battle_map):
    value = True
    print('')
    print('Choose a new unoccupied position:')
    while value:
        x_place = int(input('Enter a value 0 to 11 for X: '))
        while x_place < 0 or x_place > 11:
            print(x_place, 'is invalid for X')
            x_place = int(input('Enter a value 0 to 11 for X: '))
        y_place = int(input('Enter a value 0 to 11 for Y: '))
        while y_place < 0 or y_place > 11:
            print(y_place, 'is invalid for Y')
            y_place = int(input('Enter a value 0 to 11 for Y: '))
        if battle_map.is_tile_unoccupied(x_place, y_place):
            battle_map.set_unit(x_place, y_place, 1)
            value = False
        else:
            print(x_place, ',', y_place, 'is occupied.')
            value = True
    return x_place, y_place


def move_unit(battle_map, player_position):
    battle_map.set_tile_unoccupied(player_position[0], player_position[1])  # fix
    new_position = place_unit(battle_map)
    return new_position[0], new_position[1]


if __name__ == "__main__":
    main()
