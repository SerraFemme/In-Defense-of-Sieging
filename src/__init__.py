from src.ReadGameData import *
from src.BattleMap import MapInator, Movement
from src.GamePhases import BattlePhase
from src.PlayerPhase import TeamMaker
from src.HordePhase import HordeMaker


def main():
    """
    Copyright 2019, Russell Buckner, All rights reserved.
    Runs the Game.
    Battle Map only for now.
    """

    print('IN DEFENSE OF SIEGING')
    print('By: Russell Buckner' + '\n')

    # Move into new class?
    r = MasterListManager()
    terrain_list = r.get_list('Terrain')
    class_list = r.get_list('Class')
    equipment_list = r.get_list('Equipment')
    starting_equipment = r.get_list('Starting Equipment')
    starting_deck = r.get_list('Starting Deck')
    card_library = r.get_list('Card')
    encounter_list = r.get_list('Encounter')
    races = r.get_list('Enemy Race')
    roles = r.get_list('Enemy Role')
    battle_map = MapInator(terrain_list)
    movement = Movement(battle_map)

    # Create Module/Class that creates and keeps track of teams
    t = TeamMaker(class_list, starting_equipment, equipment_list,
                  starting_deck, card_library)
    player_team = t.team_init()

    horde = HordeMaker(battle_map, movement, encounter_list, races, roles,
                       equipment_list, len(player_team))
    enemy_team = horde.create_enemy_horde()

    b = BattlePhase(player_team, enemy_team, battle_map, movement)
    b.loop()


if __name__ == "__main__":
    main()
