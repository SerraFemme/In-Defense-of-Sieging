"""
Module for all of the primary phases of the game
Reward and Hub Town phases to be added later on
"""
# from ObserveEvents import Observable
from src.TeamPhases import PlayerTurn, EnemyTurn


class BattlePhase(object):
    """
    Controls the Battle Phase
    """
    def __init__(self, player_team, enemy_team, battle_map, movement):
        # Observable Class initiator
        self.player_phase = PlayerTurn(player_team, battle_map, movement)
        self.player_phase.setup_players()
        self.enemy_phase = EnemyTurn(enemy_team, battle_map, movement,
                                     player_team)

    def loop(self):  # optimize?
        global i  # turn counter
        i = 1
        # while keep_playing:
        while True:
            print('\n' + 'Turn', i, '\n' + 'Player Phase')
            keep_playing = self.player_phase.player_turn_loop()
            if keep_playing is False:
                break

            print('\n' + 'Turn', i, '\n' + 'Enemy Phase')
            self.enemy_phase.enemy_turn_loop()

            i += 1
