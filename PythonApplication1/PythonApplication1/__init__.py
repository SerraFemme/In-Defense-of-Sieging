from BattleMap import MapInator
from ReadGameData import *


def main():
    # Call MasterListManager()

    # keep_playing = True
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

    battle_map.set_unit(5, 0, 1)
    battle_map.set_unit(6, 11, 1)

    battle_map.print_map()

    # while keep_playing:
    #     battle_map.print_map()
    #
    #     value = input("Keep Playing? Y or N")
    #     if value != 'Y':
    #         keep_playing = False


if __name__ == "__main__":
    main()
