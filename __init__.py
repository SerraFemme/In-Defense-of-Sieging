from ReadGameData import *
from BattleMap import MapInator, Movement
from GamePhases import BattlePhase
from PlayerPhase import PlayerTurn
from TeamPopulator import TeamMaker


def main():
    """
    Runs the Game.
    Battle Map only for now.
    """

    print('IN DEFENSE OF SIEGING')
    print('By: Russell Buckner')
    print('')

    r = MasterListManager()
    terrain_list = r.get_list('Terrain')
    class_list = r.get_list('Class')
    equipment_list = r.get_list('Equipment')
    battle_map = MapInator(terrain_list)
    movement = Movement(battle_map)

    t = TeamMaker(class_list, equipment_list)
    player_team = t.team_init()
    # enemy_team = []

    player_phase = PlayerTurn(player_team, battle_map, movement)

    movement.place_enemy()

    player_phase.setup_players()

    b = BattlePhase(player_phase)
    b.loop()


if __name__ == "__main__":
    main()
