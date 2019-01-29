from ReadGameData import *
from BattleMap import MapInator, Movement
from GamePhases import BattlePhase
from PlayerPhase import PlayerTurn
from TeamPopulator import TeamMaker
from Equipment import *


def main():
    """
    Copyright 2019, Russell Buckner, All rights reserved.
    Runs the Game.
    Battle Map only for now.
    """

    print('IN DEFENSE OF SIEGING')
    print('By: Russell Buckner' + '\n')

    r = MasterListManager()
    terrain_list = r.get_list('Terrain')
    class_list = r.get_list('Class')
    equipment_list = r.get_list('Equipment')
    starting_equipment = r.get_list('Starting Equipment')
    battle_map = MapInator(terrain_list)
    movement = Movement(battle_map)

    # armory = Armory(equipment_list)

    t = TeamMaker(class_list, starting_equipment, equipment_list)
    player_team = t.team_init()
    # enemy_team = []

    player_phase = PlayerTurn(player_team, battle_map, movement)

    movement.place_enemy()

    player_phase.setup_players()

    b = BattlePhase(player_phase)
    b.loop()


if __name__ == "__main__":
    main()
