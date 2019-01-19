from BattleMap import MapInator
from ReadJSONList import ReadJSONList


def main():
    r = ReadJSONList('MapTerrain.json')

    l = r.TEST_LIST_1
    l2 = r.get_list()
    l3 = r.get_list_from_dict()

    print(l)
    print(l2)
    print(l3)
    print()

    l[0] = 'test'
    print(l)
    print(l2)
    print(l3)
    print()

    l2[1] = 'asdf'
    print(l)
    print(l2)
    print(l3)
    print()

    l3[2] = 'blah'
    print(l)
    print(l2)
    print(l3)
    print()



    battle_map = MapInator()

    tile = battle_map.get_tile(0, 0)
    print(tile.get_terrain_type())


if __name__ == "__main__":
    main()
