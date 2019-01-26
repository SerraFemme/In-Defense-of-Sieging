from ReadGameData import *
from BattleMap import MapInator, Movement
from Player import Player
from PlayerPhase import PlayerTurn
from TeamPopulator import TeamMaker


def main():
    """
    Runs the Game.  Battle Map only for now.
    """
    global keep_playing
    keep_playing = True

    r = MasterListManager()
    terrain_list = r.get_list('Terrain')
    class_list = r.get_list('Class')
    equipment_list = r.get_list('Equipment')
    battle_map = MapInator(terrain_list)
    movement = Movement(battle_map)
    t = TeamMaker(class_list, equipment_list)

    player_team = []
    # player_team = t.team_init()
    # enemy_team = []

    player_1 = Player(class_list, 'Paladin')

    player_team.append(player_1)

    player_phase = PlayerTurn(player_team, battle_map, movement)

    movement.place_enemy()

    player_phase.setup_players()

    while keep_playing:
        keep_playing = player_phase.player_turn_loop()
        if keep_playing is False:
            break

        print('')
        print('Enemy Turn: N/A')
        print('')


if __name__ == "__main__":
    main()
