from ReadGameData import *
from BattleMap import MapInator, Movement
from GamePhases import BattlePhase
from PlayerPhase import TeamMaker, PlayerTurn
from HordePhase import HordeMaker, EnemyTurn


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
    encounter_list = r.get_list('Encounter')
    races = r.get_list('Enemy Race')
    roles = r.get_list('Enemy Role')
    battle_map = MapInator(terrain_list)
    movement = Movement(battle_map)

    t = TeamMaker(class_list, starting_equipment, equipment_list)
    player_team = t.team_init()

    horde = HordeMaker(battle_map, movement, encounter_list, races, roles, equipment_list, len(player_team))
    enemy_team = horde.create_enemy_horde()

    player_phase = PlayerTurn(player_team, battle_map, movement)

    # enemy_phase = EnemyTurn(enemy_team, battle_map, movement)


    player_phase.setup_players()

    b = BattlePhase(player_phase)
    b.loop()


if __name__ == "__main__":
    main()
