from ReadGameData import *
from BattleMap import MapInator, Movement
from Player import Player
from PlayerPhase import PlayerTurn


def main():
    """
    Runs the Game.  Battle Map only for now.
    """
    global keep_playing
    keep_playing = True

    r = MasterListManager()
    terrainlist = r.get_list('Terrain')
    classlist = r.get_list('Class')
    equipmentlist = r.get_list('Equipment')
    battle_map = MapInator(terrainlist)
    movement = Movement(battle_map)

    player_team = []
    # enemy_team = []

    player_1 = Player(classlist, 'Paladin')
    # give player starting equipment
    # give player starting deck

    player_team.append(player_1)

    playerphase = PlayerTurn(player_team, battle_map, movement)

    movement.place_enemy()

    playerphase.setup_players()

    while keep_playing:
        keep_playing = playerphase.player_turn_loop()
        if keep_playing is False:
            break

        print('')
        print('Enemy Turn: N/A')
        print('')


if __name__ == "__main__":
    main()
