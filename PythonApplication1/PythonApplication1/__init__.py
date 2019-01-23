from BattleMap import MapInator
from ReadGameData import *


def main():
    """
    Runs the Game.  Battle Map only for now.
    """

    keep_playing = True



    r = MasterListManager()

    # l = r.TEST_LIST_1
    # l2 = r.get_list()
    # l3 = r.get_list_from_dict()
    #
    # print(l)
    # print(l2)
    # print(l3)
    # print()
    #
    # l[0] = 'test'
    # print(l)
    # print(l2)
    # print(l3)
    # print()
    #
    # l2[1] = 'asdf'
    # print(l)
    # print(l2)
    # print(l3)
    # print()
    #
    # l3[2] = 'blah'
    # print(l)
    # print(l2)
    # print(l3)
    # print()

    terrainlist = r.get_list('Terrain')

    battle_map = MapInator(terrainlist)

    # tile = battle_map.get_tile(0, 0)
    # print(tile.get_terrain_type())

    battle_map.print_map()

    # battle_map.set_unit(5, 0, 2)
    # battle_map.set_unit(6, 11, 1)
    #
    # battle_map.print_map()

    place_unit(battle_map)

    while keep_playing:
        battle_map.print_map()
        keep_playing = continue_playing(keep_playing)


def continue_playing(value):
    v = True
    value = input("Keep Playing? 1 or 0: ")
    print('')
    if value != '1':
        v = False
    return v


def place_unit(battle_map):
    x_place = int(input('Enter a value 0 to 11 for X: '))
    while x_place < 0 or x_place > 11:
        print(x_place, 'is invalid for X')
        x_place = int(input('Enter a value 0 to 11 for X: '))
    y_place = int(input('Enter a value 0 to 11 for Y: '))
    while y_place < 0 or y_place > 11:
        print(y_place, 'is invalid for Y')
        y_place = int(input('Enter a value 0 to 11 for Y: '))
    battle_map.set_unit(x_place, y_place, 1)


if __name__ == "__main__":
    main()
