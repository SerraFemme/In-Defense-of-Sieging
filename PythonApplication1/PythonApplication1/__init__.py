from BattleMap import MapInator


def main():
    battle_map = MapInator()

    tile = battle_map.get_tile(0, 0)
    print(tile.get_terrain_type())


if __name__ == "__main__":
    main()
