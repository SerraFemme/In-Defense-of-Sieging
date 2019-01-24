from random import randrange
from BattleMap import MapInator, Movement
from ReadGameData import *


def main():
    """
    Runs the Game.  Battle Map only for now.
    """

    keep_playing = True

    r = MasterListManager()

    terrainlist = r.get_list('Terrain')

    battle_map = MapInator(terrainlist)
    movement = Movement(battle_map)

    movement.place_enemy()

    battle_map.print_map()

    player_position = movement.place_starting_unit()

    while keep_playing:
        battle_map.print_map()
        if movement.can_move(player_position):
            player_position = movement.move_unit(player_position)
        else:
            print('Player is trapped.')
        battle_map.print_map()
        keep_playing = continue_playing()


def continue_playing():
    v = True
    value = input("Keep Playing? 1 or 0: ")
    print('')
    if value != '1':
        v = False
    return v


if __name__ == "__main__":
    main()
